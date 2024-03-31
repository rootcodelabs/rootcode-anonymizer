import streamlit as st
import anonymizer_app as anonymizer_app
import regex_pattern_app as regex_pattern_app
import immutable_words_app as immutable_words_app

sidebar_enabled = True

def main():

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", ['Anonimizer', 'Regex', 'Immutable Words'])

    if selection == 'Anonimizer':
        with st.spinner('Loading Anonimizer...'):
            anonymizer_app.main()

    elif selection == 'Regex':
            regex_pattern_app.main()

    elif selection == 'Immutable Words':
            immutable_words_app.main()

if __name__ == "__main__":
    main()
