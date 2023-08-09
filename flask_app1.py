import flask
from moviepy.editor import *

app = flask.Flask(__name__)

@app.route("/create_video", methods=["POST"])
def create_video():
   

    data = flask.request.get_json()
    folder_path = data["folder_path"]
    output_path = data["output_path"]
    output_width = data["output_width"]
    output_height = data["output_height"]

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return ""

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
    print('create video')
    return output_path

@app.route("/add_text", methods=["POST"])
def add_text():
   

    data = flask.request.get_json()
    input_video = data["input_video"]
    text = data["text"]
    output_path = data["output_path"]
    

    input_video_clip = VideoFileClip(input_video)
    txt_clip = TextClip(text, fontsize=50, color='white')
    txt_clip = txt_clip.set_pos('bottom').set_duration(2)
    video = CompositeVideoClip([input_video_clip, txt_clip])
    video.write_videofile(output_path, fps=24)

    return output_path
@app.route("/video_over_video", methods=["POST"])
def video_over_video():
    

    data = flask.request.get_json()
    background_video_path = data["background_video"]
    foreground_video_path = data["foreground_video"]
    output_path = data["output_path"]
    
    background_video = VideoFileClip(background_video_path, audio=False).subclip(0, 5)
    w, h = moviesize = background_video.size

    foreground_video = VideoFileClip(foreground_video_path).subclip(0, 5).resize((w / 1.5, h))
    final = CompositeVideoClip([background_video.set_position('center'), foreground_video.set_position('center')])
    final.write_videofile(output_path, fps=24, codec='libx264')
    return output_path

@app.route("/create_add_text", methods=["POST"])
def create_add_text():
            
            data = flask.request.get_json()
            folder_path = data["folder_path"]
            output_path = data["output_path"]
            text = data["text"]
            output_width = data["output_width"]
            output_height = data["output_height"]

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

            txt_clip = TextClip(text, fontsize = 70, color = 'white')
            txt_clip = txt_clip.set_pos('bottom').set_duration(2)
            video = CompositeVideoClip([concat_clip, txt_clip])
            video.write_videofile(output_path, fps=24)  
            return output_path

@app.route("/final_video", methods=["POST"])
def final_video():
            data = flask.request.get_json()
            folder_path = data["folder_path"]
            output_path = data["output_path"]
            text = data["text"]
            foreground_video_path = data["foreground_video_path"]
            output_width = data["output_width"]
            output_height = data["output_height"]

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

            #clip = VideoFileClip(input_video)
            txt_clip = TextClip(text, fontsize = 70, color = 'white')
            txt_clip = txt_clip.set_pos('bottom').set_duration(2)
            video1 = CompositeVideoClip([concat_clip, txt_clip])

            #background_video = VideoFileClip(video1).subclip(0,5)
            w, h = moviesize = video1.size

            foreground_video = VideoFileClip(foreground_video_path).subclip(0, 5).resize((w/2,h))
            video2 = CompositeVideoClip([ video1.set_position('center'),foreground_video.set_position('center')])
            final = concatenate_videoclips([video1, video2])
            final.write_videofile(output_path, fps=24)
            return output_path
if __name__ == "__main__":
    app.run(debug=True, port=3045)
