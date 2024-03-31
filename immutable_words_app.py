import streamlit as st
import json

def load_words():
    try:
        with open('immutable_words.json', 'r') as f:
            data = json.load(f)
            return data['words']
    except FileNotFoundError:
        # If file not found, return an empty list
        return []

def save_words(words):
    with open('immutable_words.json', 'w') as f:
        json.dump({"words": words}, f)

def main():
    st.title("Manage Immutable Words")

    words = load_words()

    st.markdown("---")
    st.subheader("Add New Word")
    new_word = st.text_input("Enter New Word:")
    if st.button("Add"):
        if new_word.strip() != "":
            words.append(new_word)
            save_words(words)
            st.success("Word added successfully.")
        else:
            st.error("Please enter a valid word.")

    st.markdown("---")
    st.subheader("Update or Delete Existing Words")
    if not words:
        st.write("No words added yet.")
    else:
        selected_word = st.selectbox("Select Word:", words)
        new_word = st.text_input("If Updating, Update here:", value=selected_word)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete"):
                words.remove(selected_word)
                save_words(words)
                st.success("Word deleted successfully.")
        with col2:
            if st.button("Update"):
                if new_word.strip() != "":
                    index = words.index(selected_word)
                    words[index] = new_word
                    save_words(words)
                    st.success("Word updated successfully.")
                else:
                    st.error("Please enter a valid word.")

    st.markdown("---")
    st.write("Current Words:", words)

if __name__ == "__main__":
    main()
