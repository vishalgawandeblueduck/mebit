from flask import Flask, request, render_template, send_file
from video_editing_pipeline import VideoEditor  # Replace with your function's filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_video():
    if request.method == 'POST':
        folder_path = request.form.get('folder_path')
        text = request.form.get('text')
        foreground_video_path = request.files['foreground_video'].filename
        output_width = int(request.form.get('output_width'))
        output_height = int(request.form.get('output_height'))

        output_path = 'generated_video.mp4'
        VideoEditor.final_video(folder_path, text, output_path, foreground_video_path, output_width, output_height)

        return send_file(output_path, as_attachment=True)

    return render_template('upload.html')  # Create an HTML form to submit the data

if __name__ == '__main__':
    app.run(debug=True)
