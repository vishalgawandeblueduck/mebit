from moviepy.editor import *
import os
import cv2
class VideoEditor:
    def create_video(folder_path, output_path, output_width = 1280, output_height=720):
        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist.")
            return

        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))
                        and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        image_files.sort()

        clips = []
        for m in image_files:
            image_path = os.path.join(folder_path, m)
            image_clip = ImageClip(image_path).set_duration(1)
            image_clip = image_clip.resize((output_width, output_height))
            clips.append(image_clip)

        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile(output_path, fps=24)
        return output_path


    def add_text(input_video,text,output_path,FontSize=70,Color = 'white'):
        clip = VideoFileClip(input_video)
        txt_clip = TextClip(text, fontsize = FontSize, color = Color)
        txt_clip = txt_clip.set_pos('bottom').set_duration(2)
        video = CompositeVideoClip([clip, txt_clip])
        video.write_videofile(output_path, fps=24)

    def video_over_video(background_video_path,foreground_video_path,output_path,end,start=0):
        background_video = VideoFileClip(background_video_path, audio=False).subclip(start,end)
        w, h = moviesize = background_video.size

        foreground_video = VideoFileClip(foreground_video_path).subclip(start, end).resize((w/2,h))
        final = CompositeVideoClip([ background_video.set_position('center'),foreground_video.set_position('center')])
        final.write_videofile(output_path, fps=24, codec='libx264')
        #display(final.ipython_display(fps=final.fps, autoplay=True))

  


VideoEditor.create_video("resized", "output_video/create_video.mp4")
#VideoEditor.add_text('output_video/create_video.mp4',"helllooo","output_video/add_text.mp4")
#VideoEditor.video_over_video('output_video/create_video.mp4','video.mp4','output_video/video_over_video_op.mp4',5)

