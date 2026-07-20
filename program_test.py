import speech_recognition as sr
import whisper
import webbrowser
import ollama
import datetime
import sys
import os
import warnings


warnings.filterwarnings("ignore")

recognizer = sr.Recognizer()

# Whisper model
model = whisper.load_model("base")


def speak(text):

    print(f"\nJarvis : {text}")

    # Remove characters that may cause problems
    text = text.replace('"', "")
    text = text.replace("'", "")

    # Female voice on macOS
    os.system(f'say -v Samantha "{text}"')


def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5
        )

    # Save audio temporarily
    with open("command.wav", "wb") as file:
        file.write(audio.get_wav_data())

    print("Processing...")

    # Speech to Text using Whisper
    result = model.transcribe("command.wav")

    text = result["text"].strip().lower()

    return text

def ask_ai(question):

    try:

        response = ollama.chat(

            model="gemma:2b",

            messages=[

                {
                    "role": "system",
                    "content": """
                    You are Jarvis.

                    You are an intelligent and friendly AI voice assistant.

                    You were created by Tejaswini Shirfule.

                    Keep your answers short, clear and under 50 words.
                    """
                },

                {
                    "role": "user",
                    "content": question
                }

            ]

        )

        return response["message"]["content"]

    except Exception:

        return "Sorry. My AI engine is currently unavailable."


def execute_command(command):

    # OPEN YOUTUBE
    if "youtube" in command:

        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")


    # OPEN GOOGLE
    elif "google" in command:

        speak("Opening Google.")
        webbrowser.open("https://www.google.com")


    # TIME
    elif "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"The time is {current_time}.")


    # DATE
    elif "date" in command:

        today = datetime.datetime.now().strftime("%d %B %Y")

        speak(f"Today's date is {today}.")


    # WHO ARE YOU
    elif "who are you" in command:

        speak(
            "I am Jarvis, your personal AI assistant created by Tejaswini."
        )


    # THANK YOU
    elif "thank you" in command or "thanks" in command:

        speak("You are most welcome.")


    # HOW ARE YOU
    elif "how are you" in command:

        speak("I am functioning perfectly. Thank you for asking.")


    # GOOD MORNING
    elif "good morning" in command:

        speak("Good morning. I hope you have a productive day.")


    # GOOD NIGHT
    elif "good night" in command:

        speak("Good night. Have a pleasant sleep.")


    # EXIT COMMANDS
    elif ("exit" in command or
          "quit" in command or
          "shutdown" in command or
          "stop" in command or
          "bye" in command):

        speak("Goodbye. Have a wonderful day.")

        sys.exit()


    # AI CONVERSATION
    else:

        speak("Thinking.")

        response = ask_ai(command)

        print("\nAI Response :")
        print(response)

        speak(response)


if __name__ == "__main__":

    speak("Initializing Jarvis.")
    speak("All systems are online.")
    speak("Jarvis is ready and waiting for your command.")

    while True:

        try:

            # Listen for a command
            command = listen()

            print("\nYou said :", command)

            # Ignore empty responses
            if command == "":
                continue

            # Execute the command
            execute_command(command)


        except sr.WaitTimeoutError:

            print("\nNo speech detected.")


        except KeyboardInterrupt:

            speak("Shutting down Jarvis.")
            break


        except Exception as e:

            print("\nError :", e)