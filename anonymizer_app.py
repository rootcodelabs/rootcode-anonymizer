import streamlit as st
import pandas as pd
import csv
import codecs
import time
import zipfile
from io import BytesIO
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
    st.success("File downloaded successfully!")
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
                modified_rows, error_log = process_controller.process_sentence_list(rows, my_bar)

                total_rows = len(rows)
                successful_rows = total_rows - len(error_log)
                error_rows = len(error_log)

                if error_log:
                    st.warning(f"CSV file preprocessed and processed with {error_rows} errors.")
                    st.write(f"{successful_rows} rows successfully anonymized.")
                    st.write(f"{error_rows} rows ignored due to errors.")

                    with open('error_log.txt', 'w') as f:
                        f.write('\n'.join(error_log))

                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                        zip_file.write('error_log.txt')
                        zip_file.writestr('processed_data.csv', pd.DataFrame(modified_rows).to_csv(index=False).encode('windows-1252'))

                    zip_buffer.seek(0)

                    st.download_button(
                        label="Download Errors and Processed Data",
                        data=zip_buffer,
                        file_name='processed_data_and_errors.zip',
                        mime='application/zip',
                        on_click=downloaded
                    )

                else:
                    st.success("CSV file preprocessed and processed successfully!")
                    st.write(f"{successful_rows} rows successfully anonymized.")

                    csv_file = pd.DataFrame(modified_rows).to_csv(index=False).encode('windows-1252')
                    st.download_button(
                        label="Download Processed Data",
                        data=csv_file,
                        file_name='processed_data.csv',
                        mime='text/csv',
                        on_click=downloaded
                    )

if __name__ == "__main__":
    main()
