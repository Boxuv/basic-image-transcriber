import streamlit as st
import easyocr
import ollama
from PIL import Image
import numpy as np

# --- CONFIGURATION & CACHING ---
st.set_page_config(page_title="AI OCR Refiner", layout="wide")

@st.cache_resource
def load_ocr_reader():
    """Loads the OCR reader once and keeps it in memory."""
    # Supports English and Estonian
    return easyocr.Reader(['en', 'et'])

reader = load_ocr_reader()

def refine_text_with_ai(raw_text):
    """Sends the messy text to local Ollama/Gemma."""
    prompt = f"""
    The following text was extracted from an image via OCR. 
    It likely contains typos, misread characters, or weird spacing.
    Please clean it up and provide the most logical, corrected version.
    Keep the original language. Do not add any commentary, just the corrected text.

    OCR Text: {raw_text}
    """
    try:
        response = ollama.chat(model='gemma:2b', messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

# --- UI LAYOUT ---
st.title("🖼️ Local AI OCR & Refiner")
st.markdown("Drag and drop an image below to extract and clean text using local AI.")

# Drag and Drop Area
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Create two columns: one for the image, one for the text
    col1, col2 = st.columns([1, 1])

    # Load and display image
    image = Image.open(uploaded_file)
    img_array = np.array(image) # Convert to numpy array for EasyOCR
    
    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with col2:
        with st.spinner("Running OCR..."):
            # Step 1: OCR
            raw_results = reader.readtext(img_array, detail=0)
            raw_text = " ".join(raw_results)

        with st.spinner("Refining with AI..."):
            # Step 2: AI Refinement
            clean_text = refine_text_with_ai(raw_text)

        # Display Results
        st.subheader("Results")
        
        st.markdown("**Raw OCR Output:**")
        st.text_area("Raw Text", raw_text, height=150, key="raw")

        st.markdown("**✨ AI Refined Output:**")
        st.text_area("Cleaned Text", clean_text, height=150, key="clean")
        
        # Add a download button for the clean text
        st.download_button(
            label="Download Cleaned Text",
            data=clean_text,
            file_name="transcription.txt",
            mime="text/plain"
        )

else:
    st.info("Please upload an image file to begin.")
    st.image("https://via.placeholder.com/800x400.png?text=Upload+an+image+to+see+results", use_container_width=True)

# --- FOOTER ---
st.sidebar.title("Status")
st.sidebar.success("Ollama Connection: Ready (if running)")
st.sidebar.info("Model: Gemma:2b")