from gtts import gTTS
import speech_recognition as sr
import pygame as pg
import threading
import os
import time

# ============================================
# Initialize Pygame Mixer
# ============================================

pg.mixer.init()

# ============================================
# NLLB -> gTTS Language Mapping
# ============================================

LANGUAGE_MAP = {
    "eng_Latn": "en",
    "hin_Deva": "hi",
    "urd_Arab": "ur",
    "fra_Latn": "fr",
    "deu_Latn": "de",
    "spa_Latn": "es",
    "ita_Latn": "it",
    "jpn_Jpan": "ja",
    "kor_Hang": "ko",
    "zho_Hans": "zh-CN",
    "arb_Arab": "ar",
    "rus_Cyrl": "ru",
    "ben_Beng": "bn",
    "pan_Guru": "pa",
    "tam_Taml": "ta",
    "tel_Telu": "te",
    "guj_Gujr": "gu",
    "mar_Deva": "mr"
}


# ============================================
# Text To Speech
# ============================================

def speak(text, lang):

    try:

        if not text.strip():
            return

        lang = LANGUAGE_MAP.get(lang, "en")

        voice_path = "voice_output.mp3"

        tts = gTTS(
            text=text,
            lang=lang
        )

        tts.save(voice_path)

        pg.mixer.music.load(voice_path)
        pg.mixer.music.play()

        while pg.mixer.music.get_busy():
            time.sleep(0.1)

        pg.mixer.music.unload()

        if os.path.exists(voice_path):
            os.remove(voice_path)

    except Exception as e:

        print(f"[TTS ERROR] {e}")


# ============================================
# Background Speaker
# ============================================

def speak_async(text, lang):

    threading.Thread(
        target=speak,
        args=(text, lang),
        daemon=True
    ).start()


# ============================================
# Speech To Text
# ============================================

def listen_command():

    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.5
    recognizer.operation_timeout = 5

    with sr.Microphone() as source:

        try:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.3
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=7
            )

            text = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You said:", text)

            return text

        except sr.UnknownValueError:

            print("Could not understand audio.")

            return ""

        except sr.RequestError:

            print("Google Speech API unavailable.")

            return ""

        except Exception as e:

            print(f"[Speech Error] {e}")

            return ""