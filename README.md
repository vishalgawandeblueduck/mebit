# mebit
##flask_app.py contains the API for video editing

##video_editing_pipeline.py 
contains the python functions for video editing

1)Create video from images
VideoEditor.create_video("image folder path", "output video path with extension")

2)Add text over video file
VideoEditor.add_text('video path',text","output video path","fontsize:default 70","text color:default white")

3)Add background to video
VideoEditor.video_over_video('backgrounf video path','foreground video path','output video path)


