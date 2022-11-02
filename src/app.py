import json
from pathlib import Path

import streamlit as st

from pipeline import ResumeParser
from resume_text import ResumeText
from visualization.cloudwords import show_words
import os

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Resume Parser")
#st.image('images/header.png', width=800)
st.text("Using this to see how well your resume is read by Application Tracking Systems (ATS) when applying to jobs.")

with st.form(key="Form :", clear_on_submit=True):
    datafile = st.file_uploader(label="Upload resume", type=["pdf", "docx", "txt"])
    Submit = st.form_submit_button(label='Submit')

def save_uploadedfile(uploadedfile):
    # Save uploaded file to 'upload' folder.
    save_folder = 'upload/'
    save_path = Path(save_folder, uploadedfile.name)
    with open(save_path, mode='wb') as w:
        w.write(uploadedfile.getvalue())
        w.write(uploadedfile.getbuffer())
    return st.success(f"Saved File:{uploadedfile.name} to uploads")

if Submit:
    if datafile:
        # Create a text element and let the reader know the data is loading.
        data_load_state = st.info('Uploading Reseme')
        # save_uploadedfile(datafile)
        # file_details = {"FileName": datafile.name, "FileType": datafile.type}

        text = ResumeText(datafile, datafile.type).text
        data_load_state.success('Extracting text from reseme')

        col1, col2 = st.columns(2)
        with col1:
            information = ResumeParser(text).parse
            data_load_state.success('Parsing reseme text')

            json_string = json.dumps(information)
            st.json(json_string, expanded=True)
            st.download_button(
                label="Download JSON",
                file_name="reseme_data.json",
                mime="application/json",
                data=json_string,
            )
        with col2:
            # load show_words plot
            st.pyplot(show_words(text))
        data_load_state.success('Data is ready!')
