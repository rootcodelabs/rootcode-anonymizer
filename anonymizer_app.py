import streamlit as st
import pandas as pd
import csv
from process_controller import NERProcessorController
import codecs
import time

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def preprocess_bytes(content):
    try:
        decoded_content = content.decode('windows-1252').splitlines()
        return decoded_content
    except UnicodeDecodeError:
        print("Unicode replacement")
        return codecs.decode(content, 'windows-1252', 'ignore').splitlines()

def progress_bar_handler(progress_bar, progress, progress_text):
    progress_bar.progress(progress, text=progress_text)

def main():
    st.title('Rootcode Anonymizer')

    session_state = SessionState(uploaded_file_name=None)

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        if session_state.uploaded_file_name != uploaded_file.name:
            session_state.uploaded_file_name = uploaded_file.name
            file_name = session_state.uploaded_file_name + "_" + str(int(time.time()))

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
                mime='text/csv'
            )

if __name__ == "__main__":
    main()

