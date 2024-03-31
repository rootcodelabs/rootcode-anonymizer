import streamlit as st
import anonymizer_app
import regex_pattern_app
import immutable_words_app

def main():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f6ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", ['Anonimizer', 'Regex', 'Immutable Words'])

    if selection == 'Anonimizer':
        anonymizer_app.main()

    elif selection == 'Regex':
        regex_pattern_app.main()

    elif selection == 'Immutable Words':
        immutable_words_app.main()

if __name__ == "__main__":
    main()
