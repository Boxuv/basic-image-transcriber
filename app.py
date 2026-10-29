import streamlit as st
import easyocr
import ollama
from PIL import Image
import numpy as np
import re

# --- CONFIGURATION & CACHING ---
st.set_page_config(page_title="AI OCR Refiner", layout="wide")

OCR_LANGUAGES = {
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Italian": "it",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Polish": "pl",
    "Swedish": "sv",
    "Russian": "ru",
}

EFFORT_LEVELS = {
    # label: (ollama "think" flag, generation options)
    "Low (fastest)":   (False, {"temperature": 0.0, "num_predict": 1024}),
    "Medium":          (False, {"temperature": 0.2, "num_predict": 2048}),
    "High (thinking)": (True,  {"temperature": 0.2, "num_predict": 4096}),
}


@st.cache_resource
def load_ocr_reader(lang_codes):
    """Loads one OCR reader per language combination and keeps it in memory."""
    return easyocr.Reader(list(lang_codes))

GEMMA_PULL_HINT = "ollama pull gemma3:4b   (or the lighter: ollama pull gemma:2b)"


def _model_name(m):
    """Works with both new ollama clients (objects) and old ones (dicts)."""
    if isinstance(m, dict):
        return m.get("model") or m.get("name") or ""
    return getattr(m, "model", None) or getattr(m, "name", "") or ""


def _model_strength(m):
    """Sort key: parameter count (e.g. '7.8B', 'e4b') first, download size as tie-break."""
    details = m.get("details", {}) if isinstance(m, dict) else getattr(m, "details", None)
    param = (details.get("parameter_size") if isinstance(details, dict)
             else getattr(details, "parameter_size", "")) or ""
    match = re.search(r"(\d+(?:\.\d+)?)\s*[bB]", param)
    params = float(match.group(1)) if match else 0.0
    size = m.get("size", 0) if isinstance(m, dict) else getattr(m, "size", 0)
    return (params, size or 0)


def get_available_ollama_models():
    """Returns (gemma_models, other_models). Gemma models are sorted strongest first."""
    try:
        response = ollama.list()
        models = response["models"] if isinstance(response, dict) else response.models
    except Exception as e:
        st.error(f"Could not connect to Ollama: {e}")
        return [], []

    gemma = [m for m in models if _model_name(m).lower().startswith("gemma")]
    gemma.sort(key=_model_strength, reverse=True)
    others = [m for m in models if m not in gemma]
    return [_model_name(m) for m in gemma], [_model_name(m) for m in others]

def refine_text_with_ai(raw_text, model_name, effort, languages):
    """Sends the messy text to the user-selected local LLM."""
    think, options = EFFORT_LEVELS[effort]
    lang_hint = ", ".join(languages) if languages else "the original language"
    prompt = f"""
    The following text was extracted from an image via OCR.
    It likely contains typos, misread characters (like '0' instead of 'O'),
    or weird spacing. The text is written in: {lang_hint}.

    Please clean it up and provide the most logical, corrected version.
    Keep the original language. Do not add any commentary, just the corrected text.

    OCR Text: {raw_text}
    """
    messages = [{'role': 'user', 'content': prompt}]
    try:
        try:
            response = ollama.chat(model=model_name, messages=messages, think=think, options=options)
        except ollama.ResponseError as e:
            # Older Gemma models do not support the "think" switch; retry without it.
            if "think" not in str(e).lower():
                raise
            response = ollama.chat(model=model_name, messages=messages, options=options)
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error during AI refinement: {e}"

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings")

# Fetch models from Ollama (strongest Gemma model is preselected)
gemma_models, other_models = get_available_ollama_models()

if gemma_models:
    selected_model = st.sidebar.selectbox("Select Gemma model", gemma_models, index=0)
    st.sidebar.info(f"Using: `{selected_model}`")
elif other_models:
    selected_model = None
    st.sidebar.error(
        "No Gemma model found (only non-Gemma models are installed). "
        f"Download one with:\n\n`{GEMMA_PULL_HINT}`"
    )
else:
    selected_model = None
    st.sidebar.error(
        "No models found! Make sure Ollama is running, then download a Gemma model with:"
        f"\n\n`{GEMMA_PULL_HINT}`"
    )

selected_effort = st.sidebar.selectbox(
    "Model effort",
    list(EFFORT_LEVELS.keys()),
    index=1,
    help="High enables the model's thinking mode (slower, more careful corrections).",
)

selected_languages = st.sidebar.multiselect(
    "Input image language(s)",
    list(OCR_LANGUAGES.keys()),
    default=["English", "Estonian"],
    help="Languages present in the image. Russian can only be combined with English.",
)
if not selected_languages:
    st.sidebar.warning("Select at least one language. Falling back to English.")
    selected_languages = ["English"]

st.sidebar.markdown("---")
st.sidebar.write("Developed with Streamlit & Ollama")

# Load the OCR reader for the chosen languages (cached per combination)
try:
    reader = load_ocr_reader(tuple(OCR_LANGUAGES[l] for l in selected_languages))
except Exception as e:
    st.sidebar.error(f"Could not load OCR for this language combination: {e}")
    reader = None

# --- MAIN UI LAYOUT ---
st.title("🖼️ Local AI OCR & Refiner")
st.markdown("Drag and drop an image below to extract and clean text using your local models.")

# Drag and Drop Area
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    if selected_model is None:
        st.warning("Please ensure Ollama is running and a model is selected.")
    elif reader is None:
        st.warning("Pick a supported language combination in the sidebar.")
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
                clean_text = refine_text_with_ai(raw_text, selected_model, selected_effort, selected_languages)

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