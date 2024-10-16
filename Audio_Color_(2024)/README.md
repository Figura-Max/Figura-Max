# Audio Color
This project did not and still does not have a definite goal, but the intent was to devise a method by which an audio track could dictate the appearance of video. Of particular interest was some manner of color filtering, such that different aspects of an audio track could be mapped to different colors. Eventually, this could be used for artistic purposes, in creating a "visualiser" video for a piece of music.

The eventual result was an FFmpeg routine which could apply a number of filters to a video and update the arguments throughout the video according to one or more .cmd files. This file is itself produced by a python script, which creates an envelope of a given audio file and assigns the magnitude of that envelope at each time as the filter's argument value.

"drumtest" was created with a test card and a drum pattern which I have written. "cruxclip2" and the sample files which contributed to its construction are based on <a href="https://www.youtube.com/watch?v=kWvc5jMxdlU">"Crux of Night"</a>, used with permission. Red, green, and blue are associated with the pads, drums, and arpeggiated synth, respectively.

NOTE: Produced video may contain flashing colors; viewer discretion is advised
