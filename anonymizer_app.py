# import streamlit as st
# import pandas as pd
# import csv
# from process_controller import NERProcessorController
# import codecs
# import time

# def preprocess_bytes(content):
#     try:
#         decoded_content = content.decode('windows-1252').splitlines()
#         return decoded_content
#     except UnicodeDecodeError:
#         print("Unicode replacement")
#         return codecs.decode(content, 'windows-1252', 'ignore').splitlines()

# def main():
#     st.title('Rootcode Anonymizer')
#     print("0")

#     uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
#     print("1")

#     file_name = ""
#     last_processed_file_name = None

#     if uploaded_file is not None:
#         file_name = uploaded_file.name+"_"+str(int(time.time()))
#         print("2")
#         st.write("Uploaded file details:")
#         st.write(uploaded_file.name)
#         st.write("Preprocessing CSV file...")
        
#         print("3")

#         content = uploaded_file.getvalue()

        
#         print("4")
#         preprocessed_content = preprocess_bytes(content)

#         process_controller = NERProcessorController()

#         reader = csv.reader(preprocessed_content)
#         rows = [row for row in reader]
#         modified_rows = process_controller.process_sentence_list(rows)
        
#         print("5")
#         st.success("CSV file preprocessed and processed successfully!")

#         print("6")
#         df = pd.DataFrame(modified_rows)

#         print("7")
#         st.subheader("Download processed CSV file")
#         csv_file = df.to_csv(index=False).encode('windows-1252')
#         st.download_button(
#             label="Download",
#             data=csv_file,
#             file_name='processed_data.csv',
#             mime='text/csv'
#         )
        
#         print("8")
#         last_processed_file_name = file_name

# if __name__ == "__main__":
#     main()


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

            content = uploaded_file.getvalue()
            preprocessed_content = preprocess_bytes(content)

            process_controller = NERProcessorController()

            reader = csv.reader(preprocessed_content)
            rows = [row for row in reader]
            modified_rows = process_controller.process_sentence_list(rows)

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

