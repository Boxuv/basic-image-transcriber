# 🖼️ Local AI OCR & Text Refiner (Web UI)

A private, browser-based application that allows you to drag and drop images to extract text and automatically fix transcription errors using local Large Language Models (LLMs).

## ✨ Features
* **Drag-and-Drop Interface:** A modern, web-based UI built with Streamlit.
* **Dual-Language OCR:** Supports both English and Estonian text recognition via EasyOCR.
* **AI-Powered Refinement:** Uses a local LLM (Gemma) to fix "hallucinated" characters and spelling errors based on linguistic context.
* **Side-by-Side Comparison:** View your original image and the extracted text simultaneously.
* **100% Private & Local:** No images or text ever leave your computer. All processing is done via your local CPU/GPU.
* **Export Ready:** Download your cleaned text directly as a `.txt` file.

---

## 🛠️ Prerequisites

Before running the application, you must have the following installed:

1. **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
2. **Ollama** (The engine that runs the local AI)
   * Download from [ollama.com](https://ollama.com/)
   * Once installed, open your terminal/command prompt and run:
     ```bash
     ollama run gemma:2b
     ```
     *(This ensures the lightweight Gemma model is downloaded and ready to use.)*

---

## 🚀 Installation

1. **Clone or download this repository** to your local machine.
2. **Open your Terminal or Command Prompt** in the project folder.
3. **Install the required Python libraries** by running:
   ```bash
   pip install streamlit easyocr ollama pillow numpy
   ```

---

## 📖 Usage

1. **Launch the Application:**
   In your terminal, run the following command:
   ```bash
   streamlit run app.py
   ```
2. **Open the Browser:**
   A new tab should automatically open in your default web browser (usually at `http://localhost:8501`).
3. **Process an Image:**
   * Drag an image file (`.jpg`, `.jpeg`, or `.png`) into the upload box.
   * Wait for the "Running OCR" and "Refining with AI" spinners to complete.
4. **Review and Download:**
   * Compare the **Raw OCR Output** with the **AI Refined Output**.
   * Click **"Download Cleaned Text"** to save your result.

---

## 📂 Project Structure

```text
.
├── app.py              # The main application (UI + Logic)
└── README.md           # Project documentation
```

---

## ⚙️ Configuration & Customization

### Changing Languages
To add or remove supported languages, edit the `load_ocr_reader` function in `app.py`:
```python
# For English and Estonian
reader = easyocr.Reader(['en', 'et']) 

# For English and German only
reader = easyocr.Reader(['en', 'de']) 
```

### Changing the AI Model
If you have a powerful GPU and want higher accuracy, you can use a larger model (like `llama3` or `mistral`).
1. Download the model via terminal: `ollama pull llama3`
2. Update the `refine_text_with_ai` function in `app.py`:
   ```python
   response = ollama.chat(model='llama3', ...)
   ```

## ⚖️ License
[Specify your license, e.g., MIT]