import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary   # make sure this file exists
import time

def speak(text):
    """Speak out loud and also print text for debugging."""
    print("Jarvis:", text)
    engine = pyttsx3.init()       # re-init every time to avoid queue lock
    engine.setProperty("rate", 170)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)   # change to [1] for female voice
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def processCommand(c):
    c = c.lower()  # convert to lowercase for easy matching

    # --- Website Shortcuts ---
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    # --- Music Library ---
    elif c.startswith("play "):
        song = c.split(" ", 1)[1].strip().lower()
        link = musicLibrary.music.get(song)

        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song in your library.")
            print("Available songs:", list(musicLibrary.music.keys()))

    elif c in musicLibrary.music:  # allow direct song name
        link = musicLibrary.music[c]
        speak(f"Playing {c}")
        webbrowser.open(link)    

    else:
        #Let Open Ai handle the request
        pass


# --- MAIN LOOP ---
if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    recognizer = sr.Recognizer()

    while True:
        print("\nListening for wake word...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)
            print("Heard (wake word):", word)

            if "jarvis" in word.lower():   # wake word detection
                print("Wake word detected!")
                speak("YES")
                time.sleep(0.5)   # small pause for natural speech
                speak("Jarvis activated")

                # Listen for actual command
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("Jarvis active... waiting for your command")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except sr.UnknownValueError:
            print("Didn't catch that, waiting again...")
        except Exception as e:
            print("Error:", e)








  


