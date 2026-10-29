# 🖼️ Local AI OCR & Text Refiner

A privacy-first, web-based application that extracts text from images using OCR and uses your local Large Language Models (LLMs) to clean, fix, and verify the transcription.

## ✨ Features

* **🌐 Modern Web UI:** A beautiful, easy-to-use interface built with **Streamlit**.
* **🖱️ Drag-and-Drop:** Simply drop your images into the browser to begin processing.
* **🤖 Dynamic Model Selection:** Automatically detects all models installed in your **Ollama** library. Switch between `gemma`, `llama3`, `mistral`, or any other model via the sidebar.
* **🔍 AI-Powered Refinement:** Uses linguistic intelligence to fix "hallucinated" characters (e.g., turning `0` back into `O`) and spelling errors.
* **🇪🇪 Dual-Language OCR:** Optimized for both **English** and **Estonian** text recognition.
* **🔒 100% Private:** No data ever leaves your machine. Processing is entirely local.
* **📥 Export Ready:** Download your cleaned and verified text as a `.txt` file.

---

## 🛠️ Prerequisites

Before running the application, you must have the following installed:

1. **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
2. **Ollama** (The engine that runs your local AI)
   * Download from [ollama.com](https://ollama.com/)
   * **Important:** Ensure you have downloaded at least one model. Open your terminal and run:
     ```bash
     ollama pull gemma:2b
     ```

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
   A new tab will automatically open in your default web browser (usually at `http://localhost:8501`).
3. **Select your AI Model:**
   In the **sidebar** on the left, use the dropdown menu to choose which Ollama model you want to use for the refinement step.
4. **Process an Image:**
   * Drag and drop an image (`.jpg`, `.jpeg`, or `.png`) into the upload box.
   * The app will first run the OCR, then pass the text to your chosen AI model for cleaning.
5. **Review and Download:**
   * Compare the **Raw OCR Output** with the **AI Refined Output**.
   * Click **"Download Cleaned Text"** to save your result.

---

## 📂 Project Structure

```text
.
├── app.py              # The main application (Streamlit UI + OCR + AI Logic)
└── README.md           # Project documentation
```

---

## ⚙️ How It Works

This application utilizes a two-stage intelligent pipeline:

1. **Stage 1 (Extraction):** The `EasyOCR` engine scans the image pixels to detect shapes and convert them into a raw string of text. This stage may occasionally misread characters due to lighting or font styles.
2. **Stage 2 (Intelligence):** The raw text is sent to your locally running LLM (selected via the sidebar). The AI analyzes the sentence structure and context to "repair" the text, acting as a highly advanced, context-aware spell-checker.

## 🔍 Troubleshooting

* **"No models found":** Ensure Ollama is running in your system tray and that you have pulled a model using `ollama pull <model_name>`.
* **Slow Processing:** The speed of the refinement depends on your computer's hardware (CPU/GPU) and the size of the model selected. For faster results on older hardware, use smaller models like `gemma:2b` or `phi3`.
* **Ollama Connection Error:** Ensure the Ollama service is active before starting the Streamlit app.