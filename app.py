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
    return easyocr.Reader(['en', 'et'])

def get_available_ollama_models():
    """Queries Ollama to get a list of all locally installed models."""
    try:
        response = ollama.list()
        # Extracting model names from the response
        return [m['name'] for m in response['models']]
    except Exception as e:
        st.error(f"Could not connect to Ollama: {e}")
        return []

reader = load_ocr_reader()

def refine_text_with_ai(raw_text, model_name):
    """Sends the messy text to the user-selected local LLM."""
    prompt = f"""
    The following text was extracted from an image via OCR.
    It likely contains typos, misread characters (like '0' instead of 'O'),
    or weird spacing.

    Please clean it up and provide the most logical, corrected version.
    Keep the original language. Do not add any commentary, just the corrected text.

    OCR Text: {raw_text}
    """
    try:
        response = ollama.chat(model=model_name, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error during AI refinement: {e}"

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings")

# Fetch models from Ollama
available_models = get_available_ollama_models()

if not available_models:
    st.sidebar.error("No models found! Run 'ollama pull gemma:2b' in your terminal.")
    selected_model = None
else:
    # Let user select the model from a dropdown
    selected_model = st.sidebar.selectbox("Select AI Model", available_models)
    st.sidebar.info(f"Using: `{selected_model}`")

st.sidebar.markdown("---")
st.sidebar.write("Developed with Streamlit & Ollama")

# --- MAIN UI LAYOUT ---
st.title("🖼️ Local AI OCR & Refiner")
st.markdown("Drag and drop an image below to extract and clean text using your local models.")

# Drag and Drop Area
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    if selected_model is None:
        st.warning("Please ensure Ollama is running and a model is selected.")
    else:
        col1, col2 = st.columns([1, 1])

        # Load and display image
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)

        with col2:
            with st.spinner(f"Running OCR..."):
                # Step 1: OCR
                raw_results = reader.readtext(img_array, detail=0)
                raw_text = " ".join(raw_results)

            with st.spinner(f"Refining with {selected_model}..."):
                # Step 2: AI Refinement
                clean_text = refine_text_with_ai(raw_text, selected_model)

            # Display Results
            st.subheader("Results")

            st.markdown("**Raw OCR Output:**")
            st.text_area("Raw Text", raw_text, height=150, key="raw")

            st.markdown("**✨ AI Refined Output:**")
            st.text_area("Cleaned Text", clean_text, height=150, key="clean")

            st.download_button(
                label="Download Cleaned Text",
                data=clean_text,
                file_name="transcription.txt",
                mime="text/plain"
            )

else:
    st.info("Please upload an image file to begin.")