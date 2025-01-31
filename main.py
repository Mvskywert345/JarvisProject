import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai

newsapi = ""  # API key
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key="",
)
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  
    messages=[              
        {"role": "system", "content": "You are a helpful assistant."},  # System message (optional, sets context)
        {"role": "user", "content": "Hello, how are you?"},           # User message
        {"role": "assistant", "content": "I'm doing great, thank you!"}  # Assistant response
    ]
)


response = completion.choices[0].message['content']

print(response)

def processCommand(command):
    """Process recognized commands to perform actions."""
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        if song in musicLibrary.music:
            speak(f"Playing {song}")
            webbrowser.open(musicLibrary.music[song])
        else:
            speak(f"Sorry, I couldn't find {song} in your music library.")
    elif "news" in command or "tell me news" in command:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data['articles']
                for article in articles:
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            speak(f"An error occurred: {e}")

    else:
        output = aiProcess(command)
        speak(output)

def listen_for_command():
    """Listen and return recognized text."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    return recognizer.recognize_google(audio).lower()

if __name__ == "__main__":
    speak("Initializing jarvis....")
    while True:
        try:
            print("Listening for the wake word...")
            word = listen_for_command()  # Listen for the wake word
            print(f"Recognized: {word}")

            if word.lower() == "jarvis":  # If wake word is recognized
                speak("Yes, how can I assist you?")
                
                # Listen for the actual command after recognizing the wake word
                command = listen_for_command()
                print(f"Command received: {command}")

                # Process the command
                processCommand(command)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")
