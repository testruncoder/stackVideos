import streamlit as st
from moviepy.editor import *
import os, time, datetime
from base64 import b64encode
import platform, shutil

import cv2
from streamlit_image_comparison import image_comparison

from streamlit_option_menu import option_menu  # Ver0_4 (8/15/2023)

# # # venv: stvenv # # # 

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
# st_JY_stackingVideosSameTime0_4_Home0.py - Ver0_4 (8/15/2023)
# # Converted from st_JY_stackingVideosSameTime0_4.py for "Home" page as one of sub codes in support of 
# main code "st_JY_stackingVideosSameTime0_4.py";
# - Equivalent to st_JY_stackingVideosSameTime0_3.py;


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
       time.sleep(1)
       timeStampStr=time_stamp_string()
       # clip1_filename='clip1_'+timeStampStr+'.mp4'
       clip1_filename='clip1_'+vdo_filename1.split('.')[0]+f'_{timeStampStr}.mp4'
       os.rename(DEFAULT_TEMPFILE,clip1_filename)
       return clip1_filename

@st.cache_data(show_spinner=False)
def save_clip2(_clip2,vdo_filename2,finalVideo_width,DEFAULT_TEMPFILE):
       _clip2.ipython_display(width=finalVideo_width)  # default width=480;
       time.sleep(1)
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
# (1) _clip: <moviepy.editor.VideoFileClip> e.g., clip=VideoFileClip(video_file).subclip(startTime2,endTime2).margin(margin2)  # Take a subclip betwween 0 and 3 seconds;
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

# APP_TITLE='Stack Videos Side-by-Side'
# CODE_TITLE='st_JY_stackingVideosSameTime0_4'
# CODE_VER='v 0.4'

def home_page():
       # st.title(APP_TITLE)
       # st.caption(CODE_VER)
       # st.caption('Play videos side-by-side')

#     # ----------------------------------------------------------------------------------------------------
#     # SIDEBAR: DISPLAY THE CODE TITLE
#        FYEO=True
#        if FYEO==True: 
#               my_sidebar_expander00=st.sidebar.expander('Code Title:',expanded=False)
#        with my_sidebar_expander00:
#               st.write(CODE_TITLE)
#     # ----------------------------------------------------------------------------------------------------

       # # # UNIVERSAL CONSTANTS AND INITIALIZATION
       vdos=[]  # len(imgs)=0
       vdo_formats=['avi','mov','mp4','mpeg']  # ['jpg','jpeg','png']
       two_vdos_selected=False
       two_vdos_chkbox=False
       DEFAULT_TEMPFILE='__temp__.mp4'  # Default output video file from moviepy;
       DEFAULT_WIDTH=100
       frame_num=0
       CACHE_FOLDER='_tmp_stackvdos'

       # vfileName1, vfileName2=None, None # video file names whose video frames show frame numbers;
       
       cwd=os.getcwd()
       # Detect OS system (6/17/2021)
       detectedOS=platform.system()
       curr_dir=path_input_expander_local(cwd,detectedOS)
       full_cache_folder_path=curr_dir + r"\\"+CACHE_FOLDER  # Ver0_4 (8/11/2023)
       media_dir=curr_dir+'\media'
       # --------------------------- END OF UNIVERSAL CONSTANTS AND INITIALIZATION -------------------------------


       # # Use st.session_state() to use parameters outside st.form();
       # https://gist.github.com/asehmi/f3c76dae68a877138cf9b7307ddebdf7
       # https://discuss.streamlit.io/t/session-state-update-inside-and-outside-function/34645/2
       state=st.session_state
       if 'is_modified' not in state:
              state['is_modified'] = False

       def _change_callback():
              settings=[state.clip_setting,state.frame_numbers_setting,
                        state.play_clipped_setting,state.stack_setting]
              is_modified=True in settings
              state.is_modified=is_modified
       
       # if 'vfiles' not in state:
       #        state['vfileName_generated']=False
       # def _change_vfiles_callback():
       #        settings=[state.vfileName1_name, state.vfileName2_nam]
       if 'vfileName1_name' not in state:
              state['vfileName1_name']=None
       if 'vfileName2_name' not in state:
              state['vfileName2_name']=None

       # # SIDEBAR: st.file_uploader() for multiple image files
       with st.sidebar:
              vdos=st.file_uploader('Upload two video files', type=vdo_formats, accept_multiple_files=True,
                                          help="""Select two files in the popup window by pressing and holding "Shift" key""")            
              tmp_info=st.empty()
              tmp_info.info('Place input video files in the current folder as shown below.')
              if len(vdos) == 1:
                     st.warning('Choose one more image.')
              elif len(vdos) > 2:
                     st.warning(f'Should choose two images. {len(vdos)} have been selected.')
              elif len(vdos) == 2:
                     two_vdos_selected=True
                     tmp_info.empty()
              folder_path1=st.text_input('Enter a folder path for video #1',
                                         value=media_dir,
                                         key='folderpath1_textinput')
              folder_path2=st.text_input('Enter a folder path for video #2',
                                         value=media_dir,
                                         key='folderpath2_textinput')
              with st.expander('Current Path:',expanded=True):
                    st.markdown(f'Path for Video #1:   \n{folder_path1}')
                    st.markdown(f'Path for Video #2:   \n{folder_path2}')

       if two_vdos_selected:
              two_vdos_chkbox=st.sidebar.checkbox('Use these video files')

       if two_vdos_chkbox:             
              vdo1=os.path.join(folder_path1,vdos[0].name)
              vdo2=os.path.join(folder_path2,vdos[1].name)

              # # Gather fps and frame size
              _clip1, _clip2=VideoFileClip(vdo1), VideoFileClip(vdo2)

                                                        # # # Find the total number of frames per video file
                                                        # num_frames1=len(list(clip1.iter_frames()))
                                                        # num_frames2=len(list(clip2.iter_frames()))

                                                        # # Alternatively,
                                                        # https://stackoverflow.com/questions/37622544/get-number-of-frames-in-clip-with-moviepy
                                                        # num_frames1=_clip1.reader.nframes
              with st.sidebar.expander('Selected images',expanded=True):
                     st.video(vdos[0])
                     st.caption(f'#1: {vdos[0].name}')
                     st.caption(f'size: {_clip1.size}, fps: {round(_clip1.fps)}, length: {_clip1.duration:.2f} sec')
                     st.video(vdos[1])
                     st.caption(f'#2: {vdos[1].name}')
                     st.caption(f'size: {_clip2.size}, fps: {round(_clip2.fps)}, length: {_clip2.duration:.2f} sec')
                     _clip1.close()
                     _clip2.close()
              with st.sidebar.expander('Selected paths',expanded=False):
                     st.markdown(f'#1: {vdo1}')
                     st.markdown(f'#2: {vdo2}')
              for i in range(14):
                     st.sidebar.markdown('')
       # ---------------------------------- END OF side panel ----------------------------------------

       # # Input Panel on Main Page;
       col1,_,col2=st.columns((4,1,4))
       col1.markdown('### Video #1')
       col2.markdown('### Video #2')
       subc1_1,subc1_2=col1.columns(2)
       subc2_1,subc2_2=col2.columns(2)

       # st.markdown('')

       with st.form('Clip video files'):
              col1,_,col2=st.columns((4,1,4))
              subc1_1,subc1_2=col1.columns(2)
              subc2_1,subc2_2=col2.columns(2)
              startTime_vdo1=subc1_1.number_input('Start time:', min_value=0.0, 
                                                 value=0.0, key='subc1start_numinput')
              endTime_vdo1=subc1_2.number_input('End time:', min_value=0.0, 
                                                 value=3.0, key='subc1end_numinput')
              startTime_vdo2=subc2_1.number_input('Start Frame #:',min_value=0.0, 
                                                 value=0.0, key='subc2input_numinput')
              endTime_vdo2=subc2_2.number_input('End Frame #:',min_value=0.0, 
                                                 value=4.0, key='subc2_endnuminput')                
              col1.checkbox('Clip Videos',key='clip_setting')
              col1.checkbox('Play/Save Clipped Videos',key='play_clipped_setting')
              col2.checkbox('Save Frame Numbers',
                     help='Use with the "Play/Save Clipped Video" box.   \nThe process may take a while.', 
                     key='frame_numbers_setting')
              col1.checkbox('Stack Videos and Save',key='stack_setting')
              st.form_submit_button('Apply settings', on_click=_change_callback)

       with st.expander('Stacked Video Form',expanded=False):
              st.caption('Works only if the "Stack Videos and Save" box is checked.')
              c1,c2,c3=st.columns((4,2,4))
              margin1=c1.number_input('Margin:',
                                          min_value=0, value=10, key='margin1_numinput')
              margin2=c3.number_input('Margin:',
                                          min_value=0, value=10, key='margin2_numinput')
              finalVideo_width=c1.number_input('Video Width:',
                                                 min_value=0, value=480, key='vdoWidth_numinput')

       param_dic= {
              'folder_path1': folder_path1,
              'folder_path2':folder_path2,
              'startTime1': startTime_vdo1,
              'startTime2': startTime_vdo2,
              'endTime1': endTime_vdo1,
              'endTime2': endTime_vdo2,
              'margin1': margin1,
              'margin2': margin2,
              }
       # -------------------------------- END OF Input Panel on Main Page -------------------------------------- 
       
       if not two_vdos_selected and not two_vdos_chkbox:
              st.warning("""Instruction:                                                      
                         Select two video files and then check the "Use these video files" box in the side panel.""")
       elif two_vdos_selected and not two_vdos_chkbox:
              st.warning("""Instruction:                                      
                         To start, check the "Use these video files" box in the side panel.""")
       elif two_vdos_chkbox:             
              # # Loading video
              # # Getting subclip as video is large
              # # Adding margin to the video
              # # 
              if state.is_modified:
                     # # # Create a temporary folder to move the images into; Ver0_3 (8/10/2023)
                     # create_temp_folder(full_cache_folder_path)

                     if state.clip_setting:
                            with st.spinner('Clippping videos... (It may take a while.)'):
                                                 # clip1=VideoFileClip(vdo1).subclip(startTime_vdo1,endTime_vdo1).margin(margin1)  # Take a subclip betwween 0 and 3 seconds;
                                                 # clip2=VideoFileClip(vdo2).subclip(startTime_vdo2,endTime_vdo2).margin(margin2) 
                                   clip1 = subclip_video1(vdo1,param_dic)
                                   clip2 = subclip_video2(vdo2,param_dic)
                            st.info('Ready to stack videos side-by-side')

                            if state.play_clipped_setting:
                                   c1,_,c2=st.columns((5,2,5))
                                   msg_empty=st.empty()
                                   with st.spinner('Getting ready to show clipped video file #1...'):
                                          # clip1.ipython_display(width=finalVideo_width)  # default width=480;
                                          # timeStampStr=time_stamp_string()
                                          # clip1_filename='clip1_'+timeStampStr+'_.mp4'
                                          # time.sleep(1)
                                          # os.rename(DEFAULT_TEMPFILE,clip1_filename)
                                          vdo_name=vdos[0].name.split('.')[0] + '.mp4'
                                          clip1_filename=save_clip1(clip1,vdo_name,finalVideo_width,DEFAULT_TEMPFILE)
                                      
                                          # # Create a downlink of the clip1 video file;
                                          with c1:
                                                 st.markdown('Download Link for Clipped Video #1:')
                                                 create_download_link(clip1_filename)

                                   msg_empty.info('Clipped video #1 successfully')

                                   with st.spinner('Getting ready to show clipped video file #2...'):
                                          vdo_name=vdos[1].name.split('.')[0] + '.mp4'
                                          clip2_filename=save_clip2(clip2,vdo_name,finalVideo_width,DEFAULT_TEMPFILE)

                                          # # Create a downlink of the clip1 video file;
                                          with c2:
                                                 st.markdown('Download Link for Clipped Video #2:')
                                                 create_download_link(clip2_filename)
                                   msg_empty.empty()
                                   # st.success('New mp4 file saved.')

                                   st.subheader('Play Video')
                                   # # Option 1: Play a video by st.video()
                                   with st.expander('Expand to view videos in small screen',expanded=False):
                                          col1,_,col2=st.columns((8,1,8))
                                          col1.video(clip1_filename)
                                          col1.caption(clip1_filename)
                                          col2.video(clip2_filename)
                                          col2.caption(clip2_filename)
                                   st.markdown('')

                                   st.markdown('**Frame numbers are displayed on image frames.**')
                                   # # Option 2: Play a video by using cv2 and st.empty() - Ver0_3 (8/08-09/2023)
                                   # # (1) Frame number is printed on each video frame. (8/09/2023)
                                   # # (2) Save into a video file (.avi) frames with frame numbers shown. (8/09/2023)
                                   cl1,_,cl01,_,cl2=st.columns((3,1,3,1,5))  # Position for "st.button('Play Video)";
                                   c1,_,c2=st.columns((5,2,5))  # Position for displaying download links;
                                   stop_play=cl01.checkbox('Stop/Clear Video',key='stopclearvideo438')
                                   play_speed=cl2.slider('Delay Frames in Sec (Default=0.01)',
                                                               min_value=0.0, max_value=2.0, 
                                                               value=0.01, step=0.01,
                                                               help='Default value=0.01',
                                                               key='playspeed_slider')
                                   
                                   if cl1.button('Play Video #1'):
                                          time.sleep(0.5)
                                          # st.button('Clear Video Player',key='clearvideoplayer455)
                                          if state.frame_numbers_setting:
                                                 st.info('Play and then save the video with frame numbers displayed...')
                                                 out1,vfileName1=cv2_videoPlaySave(clip1,clip1_filename,stop_play,play_speed)
                                                 state.vfileName1_name=vfileName1
                                                 out1.release()
                                                 st.success(f'Successfully saved as   \n'+f'"{vfileName1}"')

                                                 # # # Create a download link of the final video file that shows frame numbers on the video frames;
                                                 # with st.spinner('Creating a download link of the final video file...'):
                                                 #        # with c1:
                                                 #        st.markdown('Download Link for Video #1 with frame numbers:')
                                                 #        create_download_link(vfileName1)
                                          else:  # Not checked the "Save Frame Numbers" box;
                                                 cv2_videoPlay(clip1,clip1_filename,stop_play,play_speed)

                                   if cl1.button('Play Video #2'):
                                          time.sleep(0.5)
                                          if state.frame_numbers_setting:
                                                 out2,vfileName2=cv2_videoPlaySave(clip2,clip2_filename,stop_play,play_speed)
                                                 state.vfileName2_name=vfileName2
                                                 out2.release()
                                                 st.success(f'Successfully saved as   \n'+f'"{vfileName2}"')

                                                 # # # Create a download link of the final video file that shows frame numbers on the video frames;
                                                 # with st.spinner('Creating a download link of the final video file...'):
                                                 #        # with c2:
                                                 #        st.markdown('Download Link for Video #2 with frame numbers:')
                                                 #        create_download_link(vfileName2)
                                          else:  # Not checked the "Save Frame Numbers" box;
                                                 cv2_videoPlay(clip2,clip2_filename,stop_play,play_speed)
                     
                            # # # Move the video file to the temp folder (Ver0_3) (8/10/2023)
                            # # shutil.move(curr_dir+"\\"+"__temp0__Copy.mp4", full_cache_folder_path+"\\"+"__temp0__Copy.mp4")
                            # shutil.move(curr_dir+"\\"+clip1_filename, full_cache_folder_path+"\\"+clip1_filename)
                            # shutil.move(curr_dir+"\\"+clip2_filename, full_cache_folder_path+"\\"+clip2_filename)
                     # ------------------------- END OF if state.clip_setting: -------------------------------------

              
                     if state.stack_setting and state.clip_setting:
                            # # Compare each video frame side-by-side: Ver0_3 (8/08/2023)
                            # # by using from streamlit_image_comparison import image_comparison;
                            st.markdown('')
                            with st.expander('Parameters:',expanded=True):
                                   col3,col4 = st.columns(2)
                                   start_position=col3.slider('Starting position of the slider: (default=50)',
                                                        min_value=0,max_value=100,value=50,
                                                        key='start_position_slider')
                                   component_width=col4.slider('Component width: (default=700)',
                                                        min_value=400,max_value=1000,value=700,
                                                        key='component_width_slider')
                                   
                                   col5,col6,col7,col8,col9,col10=st.columns((1,5,1,5,1,5))
                                   show_labels=col6.checkbox("Show Labels",value=True, key='show_labels_chekbox')
                                   make_responsive=col8.checkbox("Make responsive",value=True,key='make_responsive_checkbox')
                                   in_memory=col10.checkbox("In memory",value=True,key='in_memory_checkbox')     
                                   st.markdown('')
                                   play_speed_stacked=st.slider('Delay Frames in Sec (Default=0.01)',
                                                               min_value=0.0, max_value=5.0, 
                                                               value=0.5, step=0.1,
                                                               help='Default value=0.5',
                                                               key='playspeedstacked_slider')

                            c1,c2,c3=st.columns((5,4,4))
                            # c2.button('Clear Video Player',key='clearvideoplayer490')
                            compare_button=c1.button('Compare Side-by-Side',key='compareSidebySide499')
                            pause_player=c2.checkbox('Pause Video',key='pauseplayer500')
                            clear_player=c3.checkbox('Clear Video Player',key='clearvideoplayer501')
                            if pause_player:
                                   st.info('Pause the video for 10 minutes.')
                            if compare_button and clear_player:
                                   st.warning('Uncheck the "Clear Video Player" box to play the video.')
                            elif compare_button:
                                   video1 = cv2.VideoCapture(clip1_filename)
                                   video2 = cv2.VideoCapture(clip2_filename)
                                   video1.set(cv2.CAP_PROP_FPS,25)
                                   video2.set(cv2.CAP_PROP_FPS,25)

                                   _placeholder=st.empty()
                                   while True and not clear_player:
                                          frame_num += 1
                                          success1,image1=video1.read()
                                          success2,image2=video2.read()
                                          if not success1 and not success2:
                                                 break
                                          with _placeholder.container():
                                                 image_comparison(
                                                        img1=image1,
                                                        img2=image2,
                                                        label1=f'video 1 - #{frame_num}',
                                                        label2=f'video 2 - #{frame_num}',
                                                        width=component_width,
                                                        starting_position=start_position,
                                                        show_labels=show_labels,
                                                        make_responsive=make_responsive,
                                                        in_memory=in_memory
                                                 )
                                          if pause_player:
                                                 time.sleep(600)
                                          time.sleep(play_speed_stacked)  # Default play_speed_stacked=0.1
                                   # st.button('Clear Video Player',key='clearvideo522')
                                   # state['frameNum']=0
                            # --------------------------- END OF VER0_3 (8/08/2023) -------------------------------

                            st.subheader('Stack Videos')     
                            col1,_,col2=st.columns((5,1,10))
                            col1.markdown('')
                            stack_videos_button=col1.button('Stack Videos',key='stackvideosbutton503')
                            file_radio=col2.radio('Choose', options=['Clipped Videos','Frame Numbers Included'],
                                                 index=1, horizontal=True,
                                                 help='"Clipped Videos" will save videos without frame numbers shown',
                                                 key='file_radio835')
                            
                            if stack_videos_button:
                                   if file_radio=='Frame Numbers Included':
                                          with st.spinner('Clipping videos with frame numbers shown...'):
                                                 clip1=subclip_video1(state.vfileName1_name,param_dic)
                                                 # clip2=subclip_video1(vfileName2,param_dic)
                                                 clip2=subclip_video1(state.vfileName2_name,param_dic)
                                          st.info(f'Ready to stack two files:   \n{state.vfileName1_name}   \n{state.vfileName2_name}')
                                   else:
                                          st.info(f"""Ready to stack two files:   \n
                                                 {clip1_filename}   \n
                                                 {clip2_filename}
                                          """)

                                   # # # Saving the final clip as "__temp__.mp4" and Showing final clip
                                   with st.spinner('Stacking videos...'):
                                          # # Clips list
                                          clips=[[clip1,clip2]]
                                                                                    # clips=[[clip1_1,clip2], [clip3,clip4]]                                                                             
                                          # # # Stacking clips
                                          # final=clips_array(clips)

                                          # # # Saving a final video
                                          # final.ipython_display(width=finalVideo_width)  # default width=480;
                                          # timeStampStr=time_stamp_string()
                                          # final_filename='stacked_'+timeStampStr+'_.mp4'
                                          # time.sleep(1)
                                          # os.rename(DEFAULT_TEMPFILE,final_filename)
                                          final_filename=stack_videos(clips,finalVideo_width,DEFAULT_TEMPFILE)
                                   clip1.close()
                                   clip2.close()
                                   st.success(f'Successfully saved as \n'+f'"{final_filename}"')

                                   # # Play the final video with a adjustable width;
                                   _,c1,_=st.columns((1,5,1))
                                   width=90  # Out of 100 in full scale;
                                                                             # width=c1.slider(
                                                                             #        label="Width of Video Player's Frame",
                                                                             #        min_value=0,max_value=100,
                                                                             #        value=DEFAULT_WIDTH, format="%d%%"
                                                                             # )
                                   videoDisplay_adjustibleWidth(final_filename, width)  # Turned off the adjustable width - Ver0_3 (8/08/2023)

                                   # # # Create a downlink of the final video file;
                                   # with st.spinner('Creating a download link of the final video file...'):
                                   #        create_download_link(final_filename)

                            elif state.stack_setting and not state.clip_setting:
                                   st.warning('Check "Clip Videos" button along with "Stack" Videos" button.')

                     # ------------------------- END OF state.stack_setting and state.clip_setting: -------------------------------------
       
       # ------------------------------------------- END OF if two_vdos_chkbox: ---------------------------------------------

# ------------------------------------------------------ END OF main() ----------------------------------------------------------
       if 1 == 0:
              input_video='IMG_1709_COPY.MOV'
              input_video='IMG_0128.MOV'
              input_video=r'C:\Users\email\OneDrive\DesktopSP7\JY_pyTools\StackVideos\IMG_0128.MOV'
              # input_video='IMG_0067_20210711_Cut_20211025_161153_.mp4'
              # input_video=r'C:\Users\email\OneDrive\DesktopSP7\py_strm\IMG_0067_20210711_Cut_20211025_161153_.mp4'

              # # Loading video
              # # Getting subclip as video is large
              # # Adding margin to the video
              clip1_1=VideoFileClip(input_video).subclip(0,4).margin(10)  # Take a subclip betwween 0 and 3 seconds;
              clip1=VideoFileClip(input_video).subclip(0,3).margin(10)  # Take a subclip betwween 0 and 3 seconds;

              # # Getting clip2 by mirroring over x axis
              clip2=clip1.fx(vfx.mirror_x)

              # # Getting clip3 by mirroring over y axis
              clip3=clip1.fx(vfx.mirror_y)

              # # Getting clip4 by resizing the clip
              clip4=clip1.resize(0.60)

              # # # Rotating clip1 by 90 degree to get the clip2
              # clip190=clip1.rotate(90)

              # # Reduce the audio volume (volume x 0.5)
              # clip = clip1.volumex(0.5)

              # # Clips list
              clips=[[clip1_1,clip2],
                     [clip3,clip4]
                     ]

              # # Stacking clips
              final=clips_array(clips)

              # # # Saving the final clip as "__temp__.mp4" and Showing final clip
              final.ipython_display(width=480)
       # -------------------------------------- END OF home_page() ----------------------------------------

# if __name__=='__main__':
#     # # set page config
#     st.set_page_config(
#         page_title='Videos Side-by-Side Example',
#         layout='centered',
#     )
#     main()
#     for i in range(18):
#           st.markdown('')
# #------------------------------------------ END OF CODE ----------------------------------------