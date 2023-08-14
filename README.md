# Mebit-Video Editing
## Using Flask web-app
## Installation and Usage:
#### flask_app.py contains the API for video editing.<br>
clone the repository using :

      git clone https://github.com/vishalgawandeblueduck/mebit.git

#### All the dependecies are listed in the requirements file.<br>
run this command: 

    pip install -r requirements.txt

#### Run the flask application:

    python flask_app.py

#### API List:
All the supported API's are:
1) create_merge: creates video using images, adds text over video and merges another video.<br>
   (video is atomatically downloaded in the downloads folder)

2) create_image_video : creates video using provided images collection.

3) add_text : addes text to any pre-existing video



## Using Python Script
#### video_editing_pipelin.py contains the python functions for video editing.


#### Create video from images
      VideoEditor.create_video("image folder path", "output video path with extension")

#### Add text over video file
      VideoEditor.add_text('video path',text","output video path","fontsize:default 70","text color:default white")

#### Add background to video
      VideoEditor.video_over_video('backgrounf video path','foreground video path','output video path)


