# mebit

## Installation and Usage:
#### flask_app.py contains the API for video editing.<br>
clone the repository using :

      git clone https://github.com/vishalgawandeblueduck/mebit.git

#### All the dependecies are listed in the requirements file.<br>
run this command: 

    pip install -r requirements.txt

#### Run the flask application:

    python flask_app.py

####
  



## video_editing_pipeline.py 
contains the python functions for video editing

1)Create video from images
VideoEditor.create_video("image folder path", "output video path with extension")

2)Add text over video file
VideoEditor.add_text('video path',text","output video path","fontsize:default 70","text color:default white")

3)Add background to video
VideoEditor.video_over_video('backgrounf video path','foreground video path','output video path)


