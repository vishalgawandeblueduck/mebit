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
    FontSize = data["FontSize"]
    Color = data["Color"]

    input_video_clip = VideoFileClip(input_video)
    txt_clip = TextClip(text, fontsize=FontSize, color=Color)
    txt_clip = txt_clip.set_pos('bottom').set_duration(2)
    video = CompositeVideoClip([input_video_clip, txt_clip])
    video.write_videofile(output_path, fps=24)

    return None
@app.route("/video_over_video", methods=["POST"])
def video_over_video():
    """
    Overlay a foreground video on a background video.

    Args:
        background_video_path (str): The path to the background video file.
        foreground_video_path (str): The path to the foreground video file.
        output_path (str): The path to the output video file.
        end (int): The end time of the output video.
        start (int, optional): The start time of the output video. Defaults to 0.

    Returns:
        None
    """

    data = flask.request.get_json()
    background_video_path = data["background_video"]
    foreground_video_path = data["foreground_video"]
    output_path = data["output_path"]
    end = data["end"]
    start = data["start"]

    background_video = VideoFileClip(background_video_path, audio=False).subclip(start, end)
    w, h = moviesize = background_video.size

    foreground_video = VideoFileClip(foreground_video_path).subclip(start, end).resize((w / 1.5, h))
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
        # concat_clip.write_videofile("create_video.mp4", fps=24)

            #clip = VideoFileClip(input_video)
            txt_clip = TextClip(text, fontsize = 70, color = 'white')
            txt_clip = txt_clip.set_pos('bottom').set_duration(2)
            video = CompositeVideoClip([concat_clip, txt_clip])
            video.write_videofile(output_path, fps=24)  
            return output_path

if __name__ == "__main__":
    app.run(debug=True)
