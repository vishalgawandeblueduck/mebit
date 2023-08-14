
from flask import *
import os
import tempfile
from moviepy.editor import ImageClip, concatenate_videoclips
from skimage.filters import gaussian
from moviepy.editor import *

app = Flask(__name__)

def final(image_files,text, output_path,portrait_video, output_width=1280, output_height=720):
    clips = []
    for image_file in image_files:
        image_clip = ImageClip(image_file).set_duration(1)
        image_clip = image_clip.resize((output_width, output_height))
        clips.append(image_clip)

    concat_clip = concatenate_videoclips(clips, method="compose")
    txt_clip = TextClip(text, fontsize = 70, color = 'white').set_duration(concat_clip.duration)
    txt_clip = txt_clip.set_pos('bottom')
    video1 = CompositeVideoClip([concat_clip, txt_clip])
    #video1.write_videofile(output_path, fps=24)
    foreground_video = VideoFileClip(portrait_video).subclip(0, 5)
    if foreground_video.w <=960:
        #background_video = VideoFileClip(video1).subclip(0,5)
        w, h = moviesize = video1.size

        foreground_video = foreground_video.resize((w/2,h))
        background_video =  foreground_video.set_duration(foreground_video.duration)
        video2 = CompositeVideoClip([ video1.set_position('center'),foreground_video.set_position('center')])
        final = concatenate_videoclips([video1, video2])
        final.write_videofile(output_path, fps=24)


@app.route('/')
def main():
    return render_template("default.html")
@app.route('/create_image_video', methods=['GET','POST'])
def create_image_video():
    if request.method == 'POST':
        files = request.files.getlist("file")
        video_length = request.form.get('video_length')
        video_width = request.form.get('video_width')
        image_files = []

        for file in files:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                image_files.append(temp_file.name)

        output_path = 'output.mp4'  # Temporary output path
        clips = []
        for image_file in image_files:
            image_clip = ImageClip(image_file).set_duration(1)
            image_clip = image_clip.resize((video_length, video_width))
            clips.append(image_clip)

        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile(output_path, fps=24)


    
        for image_file in image_files:
            os.remove(image_file)

        with open(output_path, 'rb') as video_file:
            video_data = video_file.read()
        #os.remove(output_path)  # Remove the temporary video file
        
        response = make_response(video_data)
        response.headers.set('Content-Type', 'video/mp4')
        response.headers.set('Content-Disposition', 'attachment', filename='output.mp4')
        return response

    return render_template("create_image_video.html")
@app.route('/add_text', methods=['GET','POST'])
def add_text():
    if request.method == 'POST':
        video = request.files['video'].filename
        text = request.form.get("text")

        output_path  = 'output.mp4'

        clip = VideoFileClip(video)
        txt_clip = TextClip(text, fontsize = 50, color = 'white')
        txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration)  
        #video.write_videofile(output_path, fps=24)

        video = CompositeVideoClip([clip, txt_clip])
        video.write_videofile(output_path, fps=24)


        with open(output_path, 'rb') as video_file:
            video_data = video_file.read()
        os.remove(output_path)  # Remove the temporary video file

        response = make_response(video_data)
        response.headers.set('Content-Type', 'video/mp4')
        response.headers.set('Content-Disposition', 'attachment', filename='output.mp4')
        return response
    
    return render_template("add_text.html")

@app.route('/create_merge', methods=['GET','POST'])
def create_video():
    if request.method == 'POST':
        files = request.files.getlist("file")
        text = request.form.get("text")
        portrait_video = request.files['portrait_video'].filename
        video_length = request.form.get('video_length')
        video_width = request.form.get('video_width')
        image_files = []
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                image_files.append(temp_file.name)

        output_path = 'output.mp4'  # Temporary output path
        final(image_files, text,output_path, portrait_video,video_length,video_width)

        for image_file in image_files:
            os.remove(image_file)

        with open(output_path, 'rb') as video_file:
            video_data = video_file.read()
        os.remove(output_path)  # Remove the temporary video file

        response = make_response(video_data)
        response.headers.set('Content-Type', 'video/mp4')
        response.headers.set('Content-Disposition', 'attachment', filename='output.mp4')
        return response
    
    return render_template("create_merge.html")

if __name__ == '__main__':
    app.run(debug=True,port=3044)
