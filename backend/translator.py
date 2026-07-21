from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# ============================================
# Model Configuration
# ============================================

MODEL_NAME = "facebook/nllb-200-distilled-600M"

print("Loading NLLB Model... Please wait.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

print(f"Model Loaded Successfully ({device})")


# ============================================
# Supported Languages
# ============================================

LANGUAGES = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "Urdu": "urd_Arab",
    "French": "fra_Latn",
    "German": "deu_Latn",
    "Spanish": "spa_Latn",
    "Italian": "ita_Latn",
    "Japanese": "jpn_Jpan",
    "Korean": "kor_Hang",
    "Chinese": "zho_Hans",
    "Arabic": "arb_Arab",
    "Russian": "rus_Cyrl",
    "Bengali": "ben_Beng",
    "Punjabi": "pan_Guru",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Gujarati": "guj_Gujr",
    "Marathi": "mar_Deva"
}


# ============================================
# Translation Function
# ============================================

def translator(text, src_lang, target_lang):
    """
    Translate text using Facebook NLLB-200.
    """

    try:

        if not text.strip():
            return ""

        if src_lang not in LANGUAGES.values():
            return "Invalid source language."

        if target_lang not in LANGUAGES.values():
            return "Invalid target language."

        tokenizer.src_lang = src_lang

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True
        ).to(device)

        forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_lang)

        with torch.no_grad():

            outputs = model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=256
            )

        translation = tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )[0]

        return translation

    except Exception as e:

        print(f"[Translation Error] {e}")
        return "Translation failed."