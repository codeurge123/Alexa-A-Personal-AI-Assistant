import speech_recognition as sr
import pyttsx3
import webbrowser # Note : webbrowser is a built-in module.
import musiclibrary
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "8b223cf9019d4aa2c1250ad7b13034313"

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate',150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    # print(c)
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles',[])

            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAi handle the request : 
        pass
        # Modified in future...




if __name__ == "__main__":
    speak("Initializing Alexa.....")
    while True:
        # Listen for the wake word "Alex"
        r = sr.Recognizer()
        
        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=2,phrase_time_limit = 1)

            word = r.recognize_google(audio)
            if(word.lower() == "alexa"):
                speak("Hello, I am your personal assistant")
                # Listen for command
                with sr.Microphone() as source:
                    print("Alexa Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error: {0}".format(e))
