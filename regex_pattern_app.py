import streamlit as st
import json

# Load the regex patterns from the JSON file
@st.cache(allow_output_mutation=True)
def load_patterns():
    with open('regex_patterns.json', 'r') as f:
        data = json.load(f)
        return data['patterns']

def save_patterns_to_file(patterns):
    # Save the modified patterns back to the JSON file
    with open('regex_patterns.json', 'w') as f:
        json.dump({'patterns': patterns}, f, indent=4)

def delete_pattern(index):
    patterns = load_patterns()
    del patterns[index]
    save_patterns_to_file(patterns)

def add_pattern(pattern, replacement):
    patterns = load_patterns()
    patterns.append({'pattern': pattern, 'replacement': replacement})
    save_patterns_to_file(patterns)

def update_pattern(index, pattern, replacement):
    patterns = load_patterns()
    patterns[index] = {'pattern': pattern, 'replacement': replacement}
    save_patterns_to_file(patterns)

def main():
    st.title('Regex Patterns Editor')

    # Display existing patterns and provide options to modify, delete, or update them
    patterns = load_patterns()
    for i, pattern_data in enumerate(patterns):
        st.subheader(f'Pattern {i+1}')
        pattern = st.text_input('Pattern:', value=pattern_data['pattern'], key=f'pattern_{i}')
        replacement = st.text_input('Replacement:', value=pattern_data['replacement'], key=f'replacement_{i}')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('Delete', key=f'delete_{i}'):
                delete_pattern(i)
                st.info(f'Pattern {i+1} deleted.')
                st.rerun()  # Rerun the app to update the UI
        with col2:
            if st.button('Update', key=f'update_{i}'):
                update_pattern(i, pattern, replacement)
                st.success(f'Pattern {i+1} updated.')
                st.rerun()  # Rerun the app to update the UI
        with col3:
            pass

    # Provide option to add new pattern
    st.subheader('Add New Pattern')
    new_pattern = st.text_input('Pattern:')
    new_replacement = st.text_input('Replacement:')
    if st.button('Add Pattern'):
        add_pattern(new_pattern, new_replacement)
        st.success('New pattern added.')
        st.rerun()  # Rerun the app to update the UI

if __name__ == '__main__':
    main()
