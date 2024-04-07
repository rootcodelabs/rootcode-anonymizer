import streamlit as st
import pandas as pd
import csv
import codecs
import time
from process_controller import NERProcessorController

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

downloaded_time = -1
file_name = "init_0"

def preprocess_bytes(content):
    try:
        decoded_content = content.decode('windows-1252').splitlines()
        return decoded_content
    except UnicodeDecodeError:
        print("Unicode replacement")
        return codecs.decode(content, 'windows-1252', 'ignore').splitlines()

def progress_bar_handler(progress_bar, progress, progress_text):
    progress_bar.progress(progress, text=progress_text)

def downloaded():
    global downloaded_time
    st.success("CSV file downloaded successfully!")
    downloaded_time = int(time.time())
    return True

def main():
    global file_name
    global downloaded_time
    st.title('Rootcode Anonymizer')

    session_state = SessionState(uploaded_file_name=None)

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        file_name = uploaded_file.name + "_" + str(int(time.time()))
        file_name_list = file_name.split('_')
        file_name, file_time = (file_name_list[0]), int(file_name_list[-1])

        if file_time > downloaded_time:
            file_name = uploaded_file.name + "_" + str(int(time.time()))
            if session_state.uploaded_file_name != uploaded_file.name:
                st.write("Uploaded file details:")
                st.write(uploaded_file.name)
                st.write("Preprocessing CSV file...")

                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)

                content = uploaded_file.getvalue()
                preprocessed_content = preprocess_bytes(content)

                process_controller = NERProcessorController()

                reader = csv.reader(preprocessed_content)
                rows = [row for row in reader]
                modified_rows = process_controller.process_sentence_list(rows, my_bar)

                st.success("CSV file preprocessed and processed successfully!")

                df = pd.DataFrame(modified_rows)

                st.subheader("Download processed CSV file")
                csv_file = df.to_csv(index=False).encode('windows-1252')
                st.download_button(
                    label="Download",
                    data=csv_file,
                    file_name='processed_data.csv',
                    mime='text/csv',
                    on_click=downloaded
                )

if __name__ == "__main__":
    main()
