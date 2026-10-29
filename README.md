# Local OCR & Text Refiner

A lightweight, privacy-focused Python application that extracts text from images using OCR (Optical Character Recognition) and uses a local Large Language Model (LLM) to correct transcription errors and typos.

## ✨ Features
* **Dual-Language OCR:** Supports both English and Estonian text recognition.
* **AI-Powered Refinement:** Uses a local LLM to fix "hallucinated" characters (e.g., converting `0` to `O` or `1` to `l`) based on linguistic context.
* **100% Private & Local:** No images or text are ever sent to the cloud. All processing happens on your own machine.
* **Low Hardware Requirement:** Optimized to run on standard consumer laptops using lightweight models.

---

## 🛠️ Prerequisites

Before running the application, you must have the following installed on your system:

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
   pip install easyocr ollama opencv-python
   ```

---

## 📖 Usage

1. **Prepare your image:** Place the image you want to transcribe in the project folder (e.g., `my_document.jpg`).
2. **Configure the script:** Open `transcribe.py` in a text editor and change the `my_image` variable to match your filename:
   ```python
   my_image = "my_document.jpg"
   ```
3. **Run the application:**
   ```bash
   python transcribe.py
   ```

### Expected Output
The terminal will display:
1. **Raw OCR Output:** The initial (potentially messy) text extracted from the pixels.
2. **Refined Output:** The cleaned, corrected version provided by the AI.

---

## ⚙️ Configuration & Customization

### Changing Languages
If you need to add or remove languages, edit the `reader` line in `transcribe.py`:
```python
# For English and Estonian
reader = easyocr.Reader(['en', 'et']) 

# For English and German only
reader = easyocr.Reader(['en', 'de']) 
```

### Changing the AI Model
If you have a powerful GPU and want better accuracy, you can use a larger model (like `llama3` or `mistral`).
1. Download the model via terminal: `ollama pull llama3`
2. Update the `ollama.chat` call in `transcribe.py`:
   ```python
   response = ollama.chat(model='llama3', ...)
   ```

---

## 🔍 How It Works
This application uses a two-stage pipeline:
1. **Stage 1 (Vision):** `EasyOCR` uses deep learning to detect character shapes in the image and convert them into a raw string.
2. **Stage 2 (Intelligence):** The raw string is passed to `Gemma` via `Ollama`. The AI analyzes the sentence structure and uses its knowledge of grammar and spelling to "repair" the text, acting as a highly intelligent spell-checker.

## ⚖️ License
[Specify your license, e.g., MIT]