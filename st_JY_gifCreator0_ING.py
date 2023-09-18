import streamlit as st
from moviepy.editor import *
from base64 import b64encode
import platform, os, datetime, time


# # # venv: stvenv # # # 

# -----------------------------------------------------------------------------------------------------------------

# st_JY_gifCreator0.py - Ver0 (8/09/2023)
# - Create a gif file from a given video file by using moviepy
# - Input panels were inspried by JY_pytools\st_JY_stackingVideosSameTime0_3.py;
# -  New:
# (1) path_input_expander_local()
# (2) time_stamp_string()
# (3) create_donwload_link()


# -----------------------------------------------------------------------------------------------------------------
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
# create_donwload_link()
# - Input:
# (1) final_filename: <str> video file name with its full folder path
# - Return: Nothing
@st.cache_data(show_spinner=False)
def create_download_link(final_filename):
       # # Create a download link of the final video;
       # # Source code: st_JY_videoPlay4_2.py;
    #    from base64 import b64encode

       vid=open(final_filename, 'rb')
       base64_data=b64encode(vid.read())
       base64_string=base64_data.decode('utf-8')
       # href = f'<a href="data:file/video;base64,{b64}" download={temp_filename}>Download Audio File</a> (click to save in {audio_file_ext} format)'  # https://discuss.streamlit.io/t/module-to-download-csv-file-is-there-anything-better-than-this-hack/3757
       href = f'<a href="data:video/mp4;base64,{base64_string}" download={final_filename}>Download a Video File</a> (click to save)'  # https://discuss.streamlit.io/t/module-to-download-csv-file-is-there-anything-better-than-this-hack/3757
       st.markdown(href,unsafe_allow_html=True)
# ------------------------------- END OF create_download_link() ----------------------------------------------


APP_TITLE='Gif Creator_ING'
CODE_TITLE='st_JY_gifCreator0'
CODE_VER='v 0.0'


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
            st.write(CODE_TITLE)
    # ----------------------------------------------------------------------------------------------------

    vdos=[]  # len(imgs)=0
    vdo_formats=['avi','mov','mp4','mpeg']  # ['jpg','jpeg','png']
    DEFAULT_TEMPFILE='__temp__.mp4'  # Default output video file from moviepy;

    cwd=os.getcwd()
    # Detect OS system (6/17/2021)
    detectedOS=platform.system()
    curr_dir=path_input_expander_local(cwd,detectedOS)
    # media_dir=curr_dir+'\media'
    media_dir=curr_dir
    
    # # SIDEBAR: st.file_uploader() for multiple image files
    with st.sidebar:
        vdo_file=st.file_uploader('Upload a video file', type=vdo_formats, accept_multiple_files=False,
                                  key='vdos_fileuploader77')
        tmp_info=st.empty()
        tmp_info.info('Place an input video file in the current folder as shown below.')
        if vdo_file is not None:
                tmp_info.empty()
        folder_path1=st.text_input('Enter a folder path for video #1',value=media_dir,key='folderpath1_textinput')

    if vdo_file is not None:
        vdo=os.path.join(folder_path1, vdo_file.name)
        # # Gather fps and frame size
        clip1=VideoFileClip(vdo)
        with st.sidebar.expander('Selected images',expanded=True):
            st.video(vdo)
            st.caption(f'#1: {vdo_file.name}')
            st.caption(f'size: {clip1.size}, fps: {clip1.fps}')
            clip1.close()
        with st.sidebar.expander('Selected paths',expanded=False):
                st.markdown(f'#1: {vdo}')
        for i in range(10):
                st.sidebar.markdown('')
    # ---------------------------------- END OF side panel ----------------------------------------

        with st.form('Create Gif'):
                Gif_form_btn=st.form_submit_button('Create Gif')

        if vdo is not None and Gif_form_btn:
                # # Create a final file name
                timeStampStr=time_stamp_string()
                clip1_gif='gif_'+vdo_file.name.split('.')[0]+'_'+timeStampStr+'.gif'

                # # Create a gif using ImageMagick or ffmpeg
                clip1.write_gif(clip1_gif)
                # clip1.to_gif('test_gif.gif')
                # # Play a gif at a slower speed, e.g., 50%
                # clip1.speedx(0.5).to_gif(clip1_gif)


                with st.spinner('Creating a gif file...'):
                        gif=VideoFileClip(clip1_gif)
                        gif.ipython_display()
                        time.sleep(1)
                        os.rename(DEFAULT_TEMPFILE,clip1_gif)
                        
                st.video(clip1_gif)

                # # # Create a downlink of the final video file;
                # with st.spinner('Creating a donwlink of the final video file...'):
                #         create_download_link(clip1_gif)
                # st.success(f'Successfully saved  \n'+clip1_gif)
                clip1.close()
                if st.button('Refresh Page'):
                      pass

    else:  # # vdo_file is None:
          st.info('To start, choose a video file.')
    # --------------------------------- END OF main() ------------------------------------------------

if __name__ == '__main__':
    # # set page config
    st.set_page_config(
          page_title='Gif Creator',
          layout='centered',
    )
    main()
    for i in range(18):
        st.markdown('')
    for i in range(28):
        st.sidebar.markdown('')
# ------------------------------------------ END OF CODE ----------------------------------------

