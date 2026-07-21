from flask import Flask, request, jsonify
from flask_cors import CORS

from translator import translator, LANGUAGES
from voice_model import speak_async, listen_command

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# Store latest translation
translated_output = ""
translated_lang = "eng_Latn"


# =====================================================
# Health Check
# =====================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "Backend Running",
        "message": "AI Language Translator API"
    })


# =====================================================
# Supported Languages
# =====================================================

@app.route("/languages", methods=["GET"])
def languages():

    return jsonify(LANGUAGES)


# =====================================================
# Translate API
# =====================================================

@app.route("/translate", methods=["POST"])
def translate():

    global translated_output
    global translated_lang

    data = request.get_json()

    text = data.get("text", "").strip()
    src_lang = data.get("src_lang", "eng_Latn")
    target_lang = data.get("target_lang", "hin_Deva")

    if text == "":
        return jsonify({
            "success": False,
            "message": "Text cannot be empty."
        }), 400

    translated_output = translator(
        text,
        src_lang,
        target_lang
    )

    translated_lang = target_lang

    return jsonify({

        "success": True,

        "translation": translated_output,

        "target_language": translated_lang

    })


# =====================================================
# Speech To Text API
# =====================================================

@app.route("/listen", methods=["GET"])
def listen():

    text = listen_command()

    return jsonify({

        "success": True,

        "text": text

    })


# =====================================================
# Text To Speech API
# =====================================================

@app.route("/speak", methods=["POST"])
def speaker():

    data = request.get_json()

    text = data.get("text", translated_output)

    lang = data.get("lang", translated_lang)

    speak_async(text, lang)

    return jsonify({

        "success": True,

        "message": "Speech started."

    })


# =====================================================
# Run Server
# =====================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )