import streamlit as st
from moviepy.editor import *
import os, time, datetime
from base64 import b64encode
import platform, shutil

import cv2
from streamlit_image_comparison import image_comparison

from streamlit_option_menu import option_menu  # Ver0_4 (8/15/2023)
# # Ver0_4 (8/15-16/2023)
from st_JY_stackVideos0_4_Home0 import home_page
from st_JY_stackVideos0_4_Clip0 import clip_page
from st_JY_stackVideos0_4_FrameIndex0 import frameIndex_page
from st_JY_stackVideos0_4_Stack0 import stack_page

# # # venv: stvenv # # # 

# # # latest main code (Ver0_4) (8/17/2023) # # #

##### REQUIREMENT ######################################################################################## 
# 'avc1' requires 'openh264-1.8.0-win64.dll' to be placed in the same folder as this python code is.
# Note that "MP4V" does not play in web browswers. 
##########################################################################################################

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # # List of Functions:
# # 8/07-08/2023
# (1) path_input_expander_local()
# (2) time_stamp_string()
# (3) _change_callback()
# (4) videoDisplay_adjustibleWidth()
# (5) clip_video()
# (6) subclip_video1(), subclip_video2()
# (7) save_clip1(), save_clip2()
# (8) stack_videos()
# (9) create_download_link()
# (10) cv2_putText_fontSize() - 8/09/2023
# (11) cv2_putText_fontCoord() - 8/09/2023
# (12) cv2_videoPlay() - 8/09/2023
# (13) cv2_videoPlaySave() - 8/09/2023
# (14) create_temp_folder() - 8/10/2023
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# ---------------------------------------------------------------------------------------------------------------------------
# st_JY_stackingVideosSameTime0_4_streamlitIO.py - Ver0_4 (9/22/2023)
# - A version of code that is deployed to streamlit cloud server by commenting out some code lines.


# ---------------------------------------------------------------------------------------------------------------------------
# st_JY_stackingVideosSameTime0_4.py - Ver0_4 (8/15/2023)
# - Update
# (1) Create multi pages to separate each tool: Clip, Print frame numbers, and Stack video files side-by-side;


# ---------------------------------------------------------------------------------------------------------------------------
# st_JY_stackingVideosSameTime0_3.py - Ver0_3 (8/08-10/2023)
# - Updates:
# (1) By using st.empty.container() and "from streamlit_image_comparison import image_comparison",
# compare each frame of two videos side-by-side;
#    (1-1) Able to pause video play in image_comparison(); 
# (2) Display video frame size and fps in the side panel when videos are uploaded (8/09/2023);
# (3) Show frame numbers on video frames -> cv2_videoPlay() (8/09/2023)
#    (3-1) Option to save them into a new  video file -> cv2_videoPlaySave() (8/09/2023)

# - New:
# (1) cv2_putText_fontSize() - 8/09/2023
# (2) cv2_putText_fontCoord() - 8/09/2023
# (3) cv2_videoPlay() - 8/09/2023
# (4) cv2_videoPlaySave() - 8/09/2023
# (5) create_temp_folder() - 8/10/2023


# ---------------------------------------------------------------------------------------------------------------------------
# st_JY_stackingVideosSameTime0_2.py - Ver0_2 (8/07-08/2023)
# - Updates:
# (1) Implemented three buttons:
#      (i) Clip videos;
#      (ii) Play the clipped videos;
#      (iii) Stack the clipped videos and save the final video via a download link;
#    Need to carefully use st.form() to avoid refreshing the whole page of the streamlit app
#    when the sizes of video files are large;
# (2) Two methods of playing the clipped videos:
#    (2-1) st.video()
#    (2-2) st.empty() and while() => Play speed is adjustable with a slider;
# (3) Input video files are located in a sub-directory "StackVdos/media";
# (4) Download links for clipped videos and the final stacked video;
# 
# - Shortcomings:
# (1) I want to implement three buttons:
#      (i) Clip videos;
#      (ii) Play the clipped videos;
#      (iii) Stack the clipped videos and save the final video via a download link;
#    => Using st.session_state() and st.form(), make parameters outside st.form():
       # https://gist.github.com/asehmi/f3c76dae68a877138cf9b7307ddebdf7
       # https://discuss.streamlit.io/t/session-state-update-inside-and-outside-function/34645/2

# - New:
# (1) path_input_expander_local()
# (2) time_stamp_string()
# (3) _change_callback()
# (4) videoDisplay_adjustibleWidth()
# (5) clip_video()
# (6) subclip_video1(), subclip_video2()
# (7) save_clip1(), save_clip2()
# (8) stack_videos()
# (9) create_download_link()


# ---------------------------------------------------------------------------------------------------------------------------
# st_JY_stackingVideosSameTime0_1_NG.py (NO GOOD) - Ver0_1 (8/07/2023)
# - Shortcomings:
# (1) I want to implement three buttons:
#      (i) Clip videos;
#      (ii) Play the clipped videos;
#      (iii) Stack the clipped videos and save the final video via a download link;
#    Need to carefully use st.form() to avoid refreshing the whole page of the streamlit app
#    when the sizes of video files are large => The features are available in Ver0_2;
# - Updates:
# (1) Added st.file_uploader();

# ---------------------------------------------------------------------------------------------------------------------------
# st_JY_stackingVideosSameTime0.py - Ver0 (8/07/2023)
# - Converted from Ex_st_tackingVideosSameTime0.py;

# ---------------------------------------------------------------------------------------------------------------------------
# Ex_st_stackingVideosSameTime0.py - Ver0 (8/05/2023)
# - Stack multiple video files and play them simultaneously;
# - Add margin to the video;
# - Video clips are allowed to have different lengths. Shorter videos would show black screens.
# - Output file is automatically saved as "__temp__.mp4"
# https://www.geeksforgeeks.org/moviepy-stacking-multiple-video-files/#
# ---------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------
# # prep_folder() - 12/31/2021 -> st_JY_webcam0_4_1.py
# - Source: \JY_pyTools\vdoimgtools\st_JY_vdoToImgs0_1_Lib.py
# # - Verify if a folder exists and create one if it does not yet exist;
# # - Input Paramter:
# # (1) cache:<str> default folder name;
# # - Return Parameter: nothing
# ** Copied and pasted from JY_stlib.py;
# ----------------------------------------------------------------------------------------------------------
def prep_folder(cache):
    if os.path.isdir(cache):
        # st.info('cache folder exists')
        pass
    else:
        os.makedirs(cache)  # Use os.makedirs() to create subfolders recursively, instead of os.mkdir() - Ver0_4_1 (01/01/2022)
        # st.info('Create a cache folder')
# ------------------------------  END of prep_folder()  --------------------------------------------------


# # FUNCTION DEFINITION: path_input_expander_local() (7/01/2021)
# # Source code: st_JY_videoPlay4_2.py in py_strm;
# - Input:
# (1) cwd: <str> obtained by os.getcwd(), i.e., cwd=os.getcwd();
# (1) detectedOS: <str> detectedOS=platform.system();
def path_input_expander_local(cwd, detectedOS):
       path=cwd
#     st.write(f'Current work directory: {cwd}')
#     path_info=st.text_input('Path',key='textinput1')
#     if not path_info:
#         st.warning('Please input a path to change.   \nOtherwise, the current path will be used.')
#         # path = cwd
#     else:
       if detectedOS == 'Windows':
              # path = path_info.replace('C:','')  # split(':')[1] is probably better to use as shown below (5/22/2021)
              # path = cwd.replace('C:','')  # split(':')[1] is probably better to use as shown below (5/22/2021)
              # path = path_info.split(':')[1]
              path = cwd.split(':')[1]
       elif detectedOS == 'Darwin' or 'Linux':  # MacOS
              # path = path_info  # For MacOS
              path = cwd  # For MacOS
       # elif detectedOS == 'Linux':
       #        st.warning('You are using Linux OS,\n   and the code is not compatible with Linux.Sorry.')

       else:
              st.warning('Your operating platform is not know.')
       # st.success(f'Path selected: "{path}"')
       return path
# --------------------------------------  END of path_input_expander_local()  --------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# create_temp_folder() - Ver0 (8/30/2022)
# - Source code: C:\Users\email\OneDrive\DesktopSP7\JY_pyTools\BingImgsGrab\st_JY_BingImgsGrab_lib0.py
# - Input:
# (1) CACHE_FOLDER: <str const> folder for temporary files
# - Return: nothing
# -----------------------------------------------------------------------------------------------------------------
def create_temp_folder(CACHE_FOLDER):
    # # Remove any previous vidoe output files - Ver0_3 (8/24/2022)
    filenames=None    
    if os.path.isdir(CACHE_FOLDER):
        if filenames:
            for element in filenames:
                os.remove(os.path.join(CACHE_FOLDER,element))
        else:
            filelist=[file for file in os.listdir(CACHE_FOLDER)]
            for file in filelist:
                os.remove(os.path.join(CACHE_FOLDER,file))
    else:
        os.mkdir(CACHE_FOLDER)
#     now0=datetime.datetime.now()
#     timestamp0=str(now0.strftime('%Y/%m/%d %I:%M:%S %p'))
#     st.write(f'Started at {timestamp0}')
# ---------------------------------------  END OF create_temp_folder()  -----------------------------------------


# -----------------------------------------------------------------------------------------------------------------
# def time_stamp_string() - 10/01/2022
# Inspired from C:\Users\email\OneDrive\DesktopSP7\JY_pyTools\MetaDataVdo\st_JY_metadatavdo0_1.py;
# - Generate the present time in a string format;
# - Input: Nothing
# - Return:
# (1) time_measured:<str>
# -----------------------------------------------------------------------------------------------------------------
def time_stamp_string():
#     import datetime

    now0=datetime.datetime.now()
    timestamp0=str(now0.strftime('%Y%m%d_%H%M%S'))
    return timestamp0  # timestamp0=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    # Or, timestamp0=datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M%S")
# ----------------------------------  END OF time_stamp_string()  --------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# def adjust_width_videoDisplay():
# - Using a slider, adjust the width of st.video()
# https://discuss.streamlit.io/t/changing-the-display-size-of-st-video/20559/5
@st.cache_data(show_spinner=False)
def videoDisplay_adjustibleWidth(video_file, width):
#       width=st.slider(
#             label='width',min_value=0,max_value=100,
#             value=DEFAULT_WIDTH, format="%d%%"
#       )
      max_width=max(width,0.01)
      side=max((100-width) / 2, 0.01)

      _,container,_=st.columns([side,max_width,side])
      container.video(data=video_file)
# ----------------------------------  END OF videoDisplay_adjustibleWidth() ----------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def clip_video(video_file,startTime_vdo,endTime_vdo,margin):
       clippedVideo=VideoFileClip(video_file).subclip(startTime_vdo,endTime_vdo).margin(margin)  # Take a subclip betwween 0 and 3 seconds;
       # clip2=VideoFileClip(vdo2).subclip(startTime_vdo2,endTime_vdo2).margin(margin2)  # Take a subclip betwween 0 and 3 seconds;
       return clippedVideo

# ----------------------------------  END OF clip_video() -------------------------------------------------


# # subclip_video1(vdo1,vdo2,param_dic)
# # - Inputs:
# (1, 2) vdo1, vdo2: <folder path to video file name in AVI, MOV, or MP4>
#        for example, "C:\Users\email\OneDrive\DesktopSP7\JY_pyTools\StackVideos\IMG_0128.MOV";
# (3) param_dic: <dic>
# {
#      'path1': <str> folder path for a video #1;
#      'path2': <str> folder path for a video #2;
#      'startTime1': <str> start time in a video #1;
#      'startTime2': <str> start time in a video #2;
#      'endTime1': <str> end time in a video #1;
#      'endTime2': <str> end time in a video #2;
#      'margin1': <str> margin in a video #1;
#      'margin2': <str> margin in a video #2;
# }
# @st.cache_resource(show_spinner=False)  # VideoFileClip() uses pickle() which requires to cache unserializable objects;
def subclip_video1(vdo1,param_dic):
       startTime1=param_dic['startTime1']
       # startTime2=param_dic['startTime2']
       endTime1=param_dic['endTime1']
       # endTime2=param_dic['endTime2']
       margin1=param_dic['margin1']  # default margin1 value=10;
       # margin2=param_dic['margin2']  # default margin2 value=10;

       # # Loading video
       # # Getting subclip as video is large
       # # Adding margin to the video
       clip1=VideoFileClip(vdo1).subclip(startTime1,endTime1).margin(margin1)  # Take a subclip betwween 0 and 3 seconds;
       # clip2=VideoFileClip(vdo2).subclip(startTime2,endTime2).margin(margin2)  # Take a subclip betwween 0 and 3 seconds;
       return clip1

# @st.cache_resource(show_spinner=False)  # VideoFileClip() uses pickle() which requires to cache unserializable objects;
def subclip_video2(vdo2,param_dic):
       # startTime1=param_dic['startTime1']
       startTime2=param_dic['startTime2']
       # endTime1=param_dic['endTime1']
       endTime2=param_dic['endTime2']
       # margin1=param_dic['margin1']  # default margin1 value=10;
       margin2=param_dic['margin2']  # default margin2 value=10;

       # # Loading video
       # # Getting subclip as video is large
       # # Adding margin to the video
       # clip1=VideoFileClip(vdo1).subclip(startTime1,endTime1).margin(margin1)  # Take a subclip betwween 0 and 3 seconds;
       clip2=VideoFileClip(vdo2).subclip(startTime2,endTime2).margin(margin2)  # Take a subclip betwween 0 and 3 seconds;
       return clip2
# ---------------------------------- END OF subclip_video1(), subclip_video2() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# save_clip():
#  - Input:
# (1) clip1: <VideoFileClip <moviepy>>
# (2) vdo_filename1, vdo_filename2: <str> file name;
# (3) finalVideo_width: <int> width of video play frame;
# (4) DEFAULT_TEMPFILE: <str> Set to "__temp__.mp4" by moviepy and clip1.ipython_display();
# - Output:
# (1) clip_filename:<str> output file name in mp4;
# -----------------------------------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def save_clip1(_clip1,vdo_filename1,finalVideo_width,DEFAULT_TEMPFILE):
       _clip1.ipython_display(width=finalVideo_width)  # default width=480;
       timeStampStr=time_stamp_string()
       # clip1_filename='clip1_'+timeStampStr+'.mp4'
       clip1_filename='clip1_'+vdo_filename1.split('.')[0]+f'_{timeStampStr}.mp4'
       time.sleep(1)
       os.rename(DEFAULT_TEMPFILE,clip1_filename)
       return clip1_filename

@st.cache_data(show_spinner=False)
def save_clip2(_clip2,vdo_filename2,finalVideo_width,DEFAULT_TEMPFILE):
       _clip2.ipython_display(width=finalVideo_width)  # default width=480;
       timeStampStr=time_stamp_string()
       # clip2_filename='clip2_'+timeStampStr+'.mp4'
       clip2_filename='clip2_'+vdo_filename2.split('.')[0]+f'_{timeStampStr}.mp4'
       time.sleep(1)
       os.rename(DEFAULT_TEMPFILE,clip2_filename)
       return clip2_filename
# ------------------------------- END OF save_clip1(), save_clip2() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# cv2_putText_fontSize(size) - Ver0_3 (8/09/2023)
# - Adjust the text font size for cv2_putText() per the resolution of a video frame;
# - Input:
# (1) size: <list of integers> e.g., [1920, 1080] as x and y;
# - Return:
# (1) fontSize: <integer>
# -----------------------------------------------------------------------------------------------------------------
def cv2_putText_fontSize(size):
       x,y=size
       if x*y < 1920 * 1080:
              fontSize=1
       else:
              fontSize=2
       return fontSize
# ------------------------------- END OF cv2_putText_fontSize() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# cv2_putText_fontCoord(size) - Ver0_3 (8/09/2023)
# - Adjust the coordinates for the textfor cv2_putText() per the resolution of a video frame;
# - Input:
# (1) size: <list of integers> e.g., [1920, 1080] as x and y;
# - Return:
# (1) fontCoord: <tuple> e.g., (30,30) as a standard value;
# -----------------------------------------------------------------------------------------------------------------
def cv2_putText_fontCoord(size):
       x,y=size
       if x*y < 1920 * 1080:
              fontCoord=(30,30)  # (30,30), (30,40)
       else:
              fontCoord=(30,80)  # (30,80)
       return fontCoord
# ------------------------------- END OF cv2_putText_fontSize() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# st_videoPlaySave_cv2() - Ver0_3 (8/09/2023)
# - Insert a frame number to each video frame;
# - Play a video file by using cv2 and st.empty(); 
# - Final images are not saved;
# - Input:
# (1) clip: <moviepy.editor.VideoFileClip> e.g., clip=VideoFileClip(video_file).subclip(startTime2,endTime2).margin(margin2)  # Take a subclip betwween 0 and 3 seconds;
# (2) clip_filename: <str> file name in mp4, i.e., the return of clip.ipython_display(width=300) where from moviepy.editor import *;
#     e.g., "__temp__.mp4";
# (3) stop_play: <boolean> If False, video play does not stop. If True, video plays.
# (5) play_speed: <float> frame delay in seconds; Default=0.01;
# - Return: Nothing
# -----------------------------------------------------------------------------------------------------------------
def cv2_videoPlay(clip, clip_filename, stop_play, play_speed):
       frameNum = 0
       video = cv2.VideoCapture(clip_filename)
       video.set(cv2.CAP_PROP_FPS,25)

       fontSize=cv2_putText_fontSize(clip.size)
       fontCoord=cv2_putText_fontCoord(clip.size)
       image_placeholder=st.empty()

       # # # Create an output video file name
       # # timeStampStr=time_stamp_string()
       # vfileName1='frameNumbered_'+clip_filename
       # fourcc=cv2.VideoWriter_fourcc(*'avc1')  #  "MP4V" does not play in web browswers.
       #                             # 'acv1' requires 'openh264-1.8.0-win64.dll' to be placed in the same folder as this python code is.
       # out1=cv2.VideoWriter(vfileName1,fourcc,clip.fps,clip.size)  # clip1 

       while True and not stop_play:
              frameNum += 1
              success,image=video.read()
              if not success:
                     break
                                                        # cv2.putText(image, f'# {str(frameNum)}', (30,40), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
              cv2.putText(image, f'# {str(frameNum)}', fontCoord, cv2.FONT_HERSHEY_COMPLEX,
                            fontSize,(0,255,0),2)
              # out1.write(image)
              image_placeholder.image(image,channels='BGR',caption=clip_filename)  # openCV has image in BGR
              time.sleep(play_speed)  # Default play_speed=0.01
       # st.button('Clear Video Player',key='clearvideoplayer455)
       # out1.release()
       # return out1,vfileName1
# ------------------------------- END OF cv2_videoPlay() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# st_videoPlaySave_cv2() - Ver0_3 (8/09/2023)
# - Insert a frame number to each video frame;
# - Play a video file by using cv2 and st.empty(); 
# - Save image streams into a video file in "avc1" format;
# - [MUST] # 'acv1' requires 'openh264-1.8.0-win64.dll' to be placed in the same folder as this python code is.
# - Input:
# (1) clip: <moviepy.editor.VideoFileClip> e.g., clip=VideoFileClip(video_file).subclip(startTime2,endTime2).margin(margin2)  # Take a subclip betwween 0 and 3 seconds;
# (2) _clip_filename: <str> file name in mp4, i.e., the return of clip.ipython_display(width=300) where from moviepy.editor import *;
#     e.g., "__temp__.mp4";
# """ [Note] UnhashableParamError: Cannot hash argument 'clip' (of type moviepy.video.io.VideoFileClip.VideoFileClip) in 'cv2_videoPlaySave'.
# To address this, you can tell Streamlit not to hash this argument by adding a leading underscore to the argument's name in the function signature:
# @st.cache_data
# def cv2_videoPlaySave(_clip, ...):
#     ...
# """
# (3) stop_play: <boolean> If False, video play does not stop. If True, video plays.
# (5) play_speed: <float> frame delay in seconds; Default=0.01;
# - Return:
# (1) out1: <cv2.VideoWriter()> I think this is <np array>;
# (2) vfileName1: <str> the name of the output video file;
# -----------------------------------------------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)  # VideoFileClip() uses pickle() which requires to cache unserializable objects;
def cv2_videoPlaySave(_clip, clip_filename, stop_play, play_speed):
       frameNum = 0
       video = cv2.VideoCapture(clip_filename)
       video.set(cv2.CAP_PROP_FPS,25)

       fontSize=cv2_putText_fontSize(_clip.size)
       fontCoord=cv2_putText_fontCoord(_clip.size)
       image_placeholder=st.empty()

       # # Create an output video file name
       # timeStampStr=time_stamp_string()
       vfileName1='frameNumbered_'+clip_filename
       fourcc=cv2.VideoWriter_fourcc(*'avc1')  #  "MP4V" does not play in web browswers.
                                   # 'acv1' requires 'openh264-1.8.0-win64.dll' to be placed in the same folder as this python code is.
       out1=cv2.VideoWriter(vfileName1,fourcc,_clip.fps,_clip.size)  # clip1 

       while True and not stop_play:
              frameNum += 1
              success,image=video.read()
              if not success:
                     break
                                                        # cv2.putText(image, f'# {str(frameNum)}', (30,40), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
              cv2.putText(image, f'# {str(frameNum)}', fontCoord, cv2.FONT_HERSHEY_COMPLEX,
                            fontSize,(0,255,0),2)
              out1.write(image)
              image_placeholder.image(image,channels='BGR',caption=clip_filename)  # openCV has image in BGR
              time.sleep(play_speed)  # Default play_speed=0.01
       # st.button('Clear Video Player',key='clearvideoplayer455)
       # out1.release()
       return out1,vfileName1
# ------------------------------- END OF cv2_videoPlaySave() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# @st.cache_data(show_spinner=False)
def stack_videos(_clips,finalVideo_width,DEFAULT_TEMPFILE):
       # # Stacking clips
       final=clips_array(_clips)

       # # Saving a final video
       final.ipython_display(width=finalVideo_width)  # default width=480;
       timeStampStr=time_stamp_string()
       final_filename='stacked_'+timeStampStr+'_.mp4'
       time.sleep(1)
       os.rename(DEFAULT_TEMPFILE,final_filename)
       return final_filename
# ------------------------------- END OF save_videos_sidebyside() ----------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# create_donwload_link()
# - Input:
# (1) final_filename: <str> video file name with its full folder path
# - Return: Nothing
# @st.cache_data(show_spinner=False)
def create_download_link(final_filename):
       # # Create a download link of the final video;
       # # Source code: st_JY_videoPlay4_2.py;
       # from base64 import b64encode

       vid=open(final_filename, 'rb')
       base64_data=b64encode(vid.read())
       base64_string=base64_data.decode('utf-8')
       # href = f'<a href="data:file/video;base64,{b64}" download={temp_filename}>Download Audio File</a> (click to save in {audio_file_ext} format)'  # https://discuss.streamlit.io/t/module-to-download-csv-file-is-there-anything-better-than-this-hack/3757
       href = f'<a href="data:video/mp4;base64,{base64_string}" download={final_filename}>Download a Video File</a> (click to save)'  # https://discuss.streamlit.io/t/module-to-download-csv-file-is-there-anything-better-than-this-hack/3757
       st.markdown(href,unsafe_allow_html=True)
# ------------------------------- END OF create_download_link() ----------------------------------------------

APP_TITLE='Stack Videos Side-by-Side'
CODE_TITLE='st_JY_stackingVideosSameTime0_4'
CODE_VER='v 0.4'


def main():
       st.title(APP_TITLE)
       st.caption(CODE_VER)
       st.caption('Play videos side-by-side')

    # ----------------------------------------------------------------------------------------------------
    # SIDEBAR: DISPLAY THE CODE TITLE
       FYEO=True
       if FYEO==True: 
              my_sidebar_expander00=st.sidebar.expander('Code Title:',expanded=False)
       with my_sidebar_expander00:
              # st.write(CODE_TITLE)
              st.write(APP_TITLE)
              st.caption(CODE_VER)
    # ----------------------------------------------------------------------------------------------------

                                                 # # # # UNIVERSAL CONSTANTS AND INITIALIZATION
                                                 # vdos=[]  # len(imgs)=0
                                                 # vdo_formats=['avi','mov','mp4','mpeg']  # ['jpg','jpeg','png']
                                                 # two_vdos_selected=False
                                                 # two_vdos_chkbox=False
                                                 # DEFAULT_TEMPFILE='__temp__.mp4'  # Default output video file from moviepy;
                                                 # DEFAULT_WIDTH=100
                                                 # frame_num=0
                                                 # CACHE_FOLDER='_tmp_stackvdos'

                                                 # # vfileName1, vfileName2=None, None # video file names whose video frames show frame numbers;
                                                 
                                                 # cwd=os.getcwd()
                                                 # # Detect OS system (6/17/2021)
                                                 # detectedOS=platform.system()
                                                 # curr_dir=path_input_expander_local(cwd,detectedOS)
                                                 # full_cache_folder_path=curr_dir + r"\\"+CACHE_FOLDER  # Ver0_4 (8/11/2023)
                                                 # media_dir=curr_dir+'\media'
       # --------------------------- END OF UNIVERSAL CONSTANTS AND INITIALIZATION -------------------------------

       # # Ver0_4 (8/15/2023) - Menu
       menuOptions=['Home', 'Clip', 'Frame Index', 'Stack']
       menu_page=option_menu(None, menuOptions,
                     icons=['camera-reels','card-image','film','stack'],  # 'film'
                     orientation='horizontal',
                     styles={
                            'nav-link': {
                                   # 'font-size': '20px',
                                   '--hover-color': '#eee',
                            },
                            'nav-link-selected': {'background-color': 'sky blue'},
                     }
              )

       if menu_page=='Home':
              home_page()
       elif menu_page=='Clip':
              clip_page()
       elif menu_page=='Frame Index':
              frameIndex_page()
       elif menu_page=='Stack':
              stack_page()
       # -------------------------------------- END OF main() ----------------------------------------


if __name__=='__main__':
    # # set page config
    st.set_page_config(
        page_title='Videos Side-by-Side Example',
        layout='centered',
    )
    main()
    for i in range(18):
          st.markdown('')


# ---------------------------------------- END OF CODE -----------------------------------------