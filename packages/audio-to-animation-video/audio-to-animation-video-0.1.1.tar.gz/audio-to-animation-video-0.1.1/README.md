# Audio To Animation Video
### Installation
```
pip install audio-to-animation-video
```

### Get started
How to multiply one number by another with this lib:

```Python
# Example usage
frame_sz = (720, 500)
images_directory = 'image/girl1'
image_filename = 'girl'  # file should be girl_A.png or jpg
audio_file = "audio/audio1.mp3"
output_video_path = 'video.mp4'
output_path = 'video_with_audio3.mp4'
background = (255,255,255)  # "image/bg/bg1.jpg" #(255, 255, 255)


generator = AudioLipSyncVideo(images_directory, image_filename, audio_file, output_video_path, output_path, frame_sz, background)
generator.generate_video()
```