import streamlit as st
import pyperclip

def toggle_case(text):
    return ''.join(c.upper() if c.islower() else c.lower() for c in text)

def sentence_case(text):
    sentences = text.split('. ')
    return '. '.join(sentence.capitalize() for sentence in sentences)

def main():
    # Set page title and header
    st.set_page_config(page_title="Text Case Converter", page_icon="🔄")
    st.title("Text Case Converter")
    st.write("Transform your text with multiple case conversion options!")

    # Text input
    text_input = st.text_area("Enter your text here:", height=150)

    # Text statistics
    if text_input:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(text_input))
        with col2:
            st.metric("Words", len(text_input.split()))
        with col3:
            st.metric("Lines", len(text_input.splitlines()))

    # Create columns for the buttons
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Convert to uppercase
    if col1.button("Convert to UPPERCASE"):
        if text_input:
            result = text_input.upper()
            st.text_area("Result:", result, height=150)
            if st.button("Copy to Clipboard", key="copy1"):
                pyperclip.copy(result)
                st.success("Copied to clipboard!")
        else:
            st.warning("Please enter some text first!")

    # Convert to lowercase
    if col2.button("Convert to lowercase"):
        if text_input:
            result = text_input.lower()
            st.text_area("Result:", result, height=150)
            if st.button("Copy to Clipboard", key="copy2"):
                pyperclip.copy(result)
                st.success("Copied to clipboard!")
        else:
            st.warning("Please enter some text first!")

    # Convert to Title Case
    if col3.button("Convert to Title Case"):
        if text_input:
            result = text_input.title()
            st.text_area("Result:", result, height=150)
            if st.button("Copy to Clipboard", key="copy3"):
                pyperclip.copy(result)
                st.success("Copied to clipboard!")
        else:
            st.warning("Please enter some text first!")

    # Convert to Sentence case
    if col4.button("Convert to Sentence case"):
        if text_input:
            result = sentence_case(text_input)
            st.text_area("Result:", result, height=150)
            if st.button("Copy to Clipboard", key="copy4"):
                pyperclip.copy(result)
                st.success("Copied to clipboard!")
        else:
            st.warning("Please enter some text first!")

    # Toggle case and Clear text buttons
    col5, col6 = st.columns(2)
    
    if col5.button("Toggle Case"):
        if text_input:
            result = toggle_case(text_input)
            st.text_area("Result:", result, height=150)
            if st.button("Copy to Clipboard", key="copy5"):
                pyperclip.copy(result)
                st.success("Copied to clipboard!")
        else:
            st.warning("Please enter some text first!")

    if col6.button("Clear Text"):
        st.experimental_rerun()

    # Add some information about the app
    st.markdown("---")
    st.markdown("""
    ### Features:
    - Convert text to UPPERCASE
    - Convert text to lowercase
    - Convert text to Title Case
    - Convert text to Sentence case
    - Toggle between upper and lowercase
    - Copy results to clipboard
    - View character, word, and line count
    - Clear text button
    
    ### How to use:
    1. Enter your text in the text area above
    2. Click any of the conversion buttons
    3. The converted text will appear below
    4. Use the "Copy to Clipboard" button to copy the result
    5. Use the "Clear Text" button to start over
    """)

if __name__ == "__main__":
    main() 