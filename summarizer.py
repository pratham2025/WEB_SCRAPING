# summarizer.py (Updated with a Paraphrasing Model)
from transformers import pipeline, logging as hf_logging
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Suppress the verbose warnings from the transformers library about max_length
hf_logging.set_verbosity_error()

# --- MODIFIED: Swapped the model to one specialized in paraphrasing ---
MODEL_NAME = "tuner007/pegasus_paraphrase"

try:
    # Initialize a text2text-generation pipeline. PEGASUS uses this.
    paraphraser = pipeline("text2text-generation", model=MODEL_NAME)
    logging.info(f"Paraphrasing pipeline loaded successfully with model: {MODEL_NAME}")
except Exception as e:
    logging.error(f"FATAL: Failed to load paraphrasing model. Error: {e}")
    paraphraser = None

def generate_summary(text: str) -> str:
    """
    Generates a paraphrase for the given text using the pre-loaded model.
    The function name is kept the same to avoid changes in worker.py.
    """
    if not paraphraser or not text or not text.strip():
        return text

    try:
        logging.info(f"Generating paraphrase for text: '{text[:80]}...'")
        
        # Generate paraphrases. num_return_sequences controls how many versions we get.
        # We'll just take the first and best one.
        paraphrase_output = paraphraser(
            text,
            num_beams=5,
            num_return_sequences=1,
            max_length=100 # Set a reasonable max length
        )
        
        paraphrased_text = paraphrase_output[0]['generated_text']
        logging.info(f"Successfully generated paraphrase: '{paraphrased_text[:80]}...'")
        return paraphrased_text
    except Exception as e:
        logging.error(f"Error during paraphrasing: {e}. Falling back to original text.")
        return text