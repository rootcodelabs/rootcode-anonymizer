import streamlit as st
import pandas as pd
import csv
from process_controller import NERProcessorController
import codecs


class SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def preprocess_bytes(content):
    try:
        decoded_content = content.decode('windows-1252').splitlines()
        return decoded_content
    except UnicodeDecodeError:
        print("Unicode replacement")
        return codecs.decode(content, 'windows-1252', 'ignore').splitlines()

def main():
    st.title('Rootcode Anonymizer')

    # Retrieve the current session state
    session_state = SessionState()

    # If this is a new session, set sidebar_enabled to True
    if not hasattr(session_state, 'sidebar_enabled'):
        session_state.sidebar_enabled = True

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        session_state.sidebar_enabled = False
        st.write("Uploaded file details:")
        st.write(uploaded_file.name)
        st.write("Preprocessing CSV file...")

        content = uploaded_file.getvalue()

        preprocessed_content = preprocess_bytes(content)

        process_controller = NERProcessorController()

        reader = csv.reader(preprocessed_content)
        rows = [row for row in reader]
        modified_rows = process_controller.process_sentence_list(rows)

        st.success("CSV file preprocessed and processed successfully!")
        session_state.sidebar_enabled = True

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
