import easyocr
import ollama
import cv2

def run_pipeline(image_path):
    # --- STEP 1: OCR (The Eyes) ---
    print(f"--- Starting OCR on {image_path} ---")
    # 'en' for English, 'et' for Estonian.
    # EasyOCR will download the models automatically the first time.
    reader = easyocr.Reader(['en', 'et'])

    # detail=0 returns just the text strings without coordinates
    raw_results = reader.readtext(image_path, detail=0)
    raw_text = " ".join(raw_results)

    print(f"Raw OCR Output: {raw_text}")
    print("-" * 30)

    # --- STEP 2: REFINEMENT (The Brain) ---
    print("--- Refining text with local LLM ---")

    # This is the prompt that tells the AI how to behave
    prompt = f"""
    The following text was extracted from an image using OCR.
    It likely contains typos, misread characters (like '0' instead of 'O'),
    or weird spacing.

    Please clean it up and provide the most logical, corrected version.
    Keep the original language. Do not add any commentary, just the corrected text.

    OCR Text: {raw_text}
    """

    # Using Ollama to talk to the local Gemma model
    response = ollama.chat(model='gemma:2b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    clean_text = response['message']['content'].strip()

    print(f"Refined Output: {clean_text}")
    print("-" * 30)
    return raw_text, clean_text

if __name__ == "__main__":
    # Put the name of your image file here!
    my_image = "test_image.jpg"

    try:
        raw, clean = run_pipeline(my_image)
        print("\nSUCCESS!")
        print(f"Original: {raw}")
        print(f"Cleaned:  {clean}")
    except Exception as e:
        print(f"An error occurred: {e}")