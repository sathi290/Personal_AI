import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    if not text:
        text = "Sorry, I couldn't generate a response."

    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print("You (voice):", text)
            return text.lower()

        except:
            print("Couldn't understand")
            return ""