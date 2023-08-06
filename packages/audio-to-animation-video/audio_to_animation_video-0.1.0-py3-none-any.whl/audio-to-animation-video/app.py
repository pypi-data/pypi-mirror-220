import soundfile as sf
import numpy as np
import cv2
import tempfile
import random
from moviepy.editor import VideoFileClip, AudioFileClip


class AudioLipSyncVideo:
    def __init__(self, images_directory, image_filepath, audio_file, output_video_path, output_path, frame_sz, background):
        self.isColor = True
        self.character = self.get_characters(images_directory, image_filepath)
        self.images_directory = images_directory
        self.audio_file = audio_file
        self.output_path = output_path
        self.output_video_path = tempfile.mktemp(suffix=".mp4")
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.fps = 10
        self.interval_ms = 100
        self.frame_size = frame_sz
        if ".jpg" in background:
            self.background_image = cv2.imread(background)
            self.isColor = False
        else:
            self.background_color = background  # (252, 246, 215)  # Background color
            self.isColor = True

    def load_and_resize_image(self, image_path):
        frame = cv2.imread(image_path)
        frame_aspect_ratio = frame.shape[1] / frame.shape[0]  # Width / Height
        target_aspect_ratio = self.frame_size[0] / self.frame_size[1]  # Width / Height

        if frame_aspect_ratio > target_aspect_ratio:
            # Image is wider, adjust height
            target_height = int(self.frame_size[0] / frame_aspect_ratio)
            frame = cv2.resize(frame, (self.frame_size[0], target_height))
            top_padding = (self.frame_size[1] - target_height) // 2
            bottom_padding = self.frame_size[1] - target_height - top_padding
            frame = cv2.copyMakeBorder(frame, top_padding, bottom_padding, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        else:
            # Image is taller, adjust width
            target_width = int(self.frame_size[1] * frame_aspect_ratio)
            frame = cv2.resize(frame, (target_width, self.frame_size[1]))
            left_padding = (self.frame_size[0] - target_width) // 2
            right_padding = self.frame_size[0] - target_width - left_padding
            frame = cv2.copyMakeBorder(frame, 0, 0, left_padding, right_padding, cv2.BORDER_CONSTANT, value=(0, 0, 0))

        return frame

    def get_characters(self, character_type, character_variable):
        self.character = {
            'pic_list': [f'{character_type}/{character_variable}_A.png', f'{character_type}/{character_variable}_B.png',
                         f'{character_type}/{character_variable}_C.png',
                         f'{character_type}/{character_variable}_D.png', f'{character_type}/{character_variable}_E.png',
                         f'{character_type}/{character_variable}_F.png'],
            'other': {'eye_open_silent': f'{character_type}/{character_variable}_EOSL.png',
                      'eye_close_silent': f'{character_type}/{character_variable}_ECSL.png',
                      'close_eye_talk': f'{character_type}/{character_variable}_ECTK.png',
                      }}
        return self.character

    def generate_video(self):
        video_writer = cv2.VideoWriter(self.output_video_path, self.fourcc, self.fps, self.frame_size)
        amplitudes = self.get_amplitude()
        self.process_amplitudes(amplitudes, video_writer)
        video_writer.release()
        self.merge_audio_with_video()

    def get_amplitude(self):
        audio, sr = sf.read(self.audio_file)
        samples_per_interval = int(sr * self.interval_ms / 1000)
        amplitudes = []
        for i in range(0, len(audio), samples_per_interval):
            interval_audio = audio[i:i + samples_per_interval]
            rms = np.sqrt(np.median(interval_audio ** 2))
            amplitudes.append(rms)
        return amplitudes

    def process_amplitudes(self, amplitudes, video_writer):
        for i, amplitude in enumerate(amplitudes):
            time = (i + 1) * 0.1
            print(f"Amplitude at {time:.1f} seconds: {round(amplitude, 1)}")
            print(round(amplitude, 5))
            if round(amplitude, 2) > 0:
                self.process_positive_amplitude(i, video_writer)
            else:
                self.process_negative_amplitude(i, video_writer)

    def add_background_color(self, frame):
        frame[np.all(frame == [0, 0, 0], axis=-1)] = self.background_color
        return frame

    def add_background_image(self, frame):
        resized_background = cv2.resize(self.background_image, self.frame_size)
        # Ensure the frame and background have the same size
        frame = cv2.resize(frame, self.frame_size)

        # Create a mask from the frame
        _, frame_mask = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1, 255, cv2.THRESH_BINARY_INV)
        frame_mask = cv2.cvtColor(frame_mask, cv2.COLOR_GRAY2BGR)

        # Bitwise operations to overlay the frame on top of the background
        combined_frame = cv2.bitwise_and(resized_background, frame_mask)
        combined_frame = cv2.bitwise_or(combined_frame, frame)

        return combined_frame

    def process_positive_amplitude(self, i, video_writer):
        print("Talking ...")
        speakers = self.character

        if i % 21 == 0:
            print("Eye Close and Talking ...")
            frame = self.load_and_resize_image(speakers.get('other').get('eye_close_silent'))
        else:
            frame = self.load_and_resize_image(random.choice(speakers.get('pic_list')))

        frame = cv2.resize(frame, self.frame_size)
        if self.isColor:
            frame = self.add_background_color(frame)
        else:
            frame = self.add_background_image(frame)
        video_writer.write(frame)

    def process_negative_amplitude(self, i, video_writer):
        speakers = self.character
        if i % 21 == 0:
            print("Eye Close and Silent ...")
            frame = self.load_and_resize_image(speakers.get('other').get('close_eye_talk'))
        else:
            print("Eye Open and Silent ...")
            frame = self.load_and_resize_image(speakers.get('other').get('eye_open_silent'))
        frame = cv2.resize(frame, self.frame_size)
        if self.isColor:
            frame = self.add_background_color(frame)
        else:
            frame = self.add_background_image(frame)
        video_writer.write(frame)

    def merge_audio_with_video(self):
        video_clip = VideoFileClip(self.output_video_path)
        audio_clip = AudioFileClip(self.audio_file)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(self.output_path, codec='libx264', audio_codec='aac')
        print("Video with merged audio saved successfully!")


# Example usage
frame_sz = (720, 500)
images_directory = 'image/girl1'
image_filename = 'girl'  # file should be girl_A.png or jpg
audio_file = "../audio/audio1.mp3"
output_video_path = 'video.mp4'
output_path = '../video_with_audio3.mp4'
background = (255,255,255)  # "image/bg/bg1.jpg" #(255, 255, 255)


generator = AudioLipSyncVideo(images_directory, image_filename, audio_file, output_video_path, output_path, frame_sz, background)

generator.generate_video()
