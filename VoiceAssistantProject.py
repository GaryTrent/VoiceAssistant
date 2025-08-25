from tkinter import *
from PIL import Image, ImageTk  # Import image for opening file 
import pyttsx3  # Python Text to Speech conversion library to make a program speak a given text aloud
import speech_recognition as sr  # Library to listen for voice commands, will implement take command to capture the speech and convert it to text
import datetime
import webbrowser

class assitance_gui:
    def __init__(self, root):  # Used for assigning the values once the object is created
        self.root = root
        self.root.title("Voice Assistant")  # Giving the title
        self.root.geometry('600x600')  # Giving the dimensions of the GUI

        # Code to display the background image
        self.bg = ImageTk.PhotoImage(Image.open('C:/Users/Garima/Desktop/background.png'))
        l2 = Label(self.root, image=self.bg)
        l2.place(x=0, y=0)

        # Code of the front image display
        self.center = ImageTk.PhotoImage(Image.open('C:/Users/Garima/Desktop/frame_image.jpg'))
        l1 = Label(self.root, image=self.center)
        l1.place(x=100, y=100, width=400, height=400)  # Unless we don't use place parameter the image will not be displayed

        start_button = Button(self.root, text="START", font=('times new roman', 14), command=self.start_option)
        start_button.place(x=150, y=520)

        close_button = Button(self.root, text="CLOSE", font=('times new roman', 14), command=self.close_option)
        close_button.place(x=350, y=520)

    def speak(self, text):
        """Speak the provided text using TTS."""
        engine = pyttsx3.init()  # Initialises the text-to-speech engine. Responsible for converting text into speech
        engine.say(text)  # Tells the engine to queue the specified text for speech
        engine.runAndWait()  # Processes the speech queue and makes the engine speak the text passed earlier

    def take_command(self):  # This function listens to voice command through microphone and converts it to text
        try:
            listener = sr.Recognizer()  # Create an object of class Recognizer
            with sr.Microphone() as data_taker:  # Use the microphone for listening, opens the microphone as input source for capturing audio
                print("Listening...")  # With ensures proper handling of microphone resource (opened and closed)
                listener.adjust_for_ambient_noise(data_taker)  # Adjusts for ambient noise to improve recognition
                voice = listener.listen(data_taker, timeout=5)  # Capture audio with a timeout
                instruction = listener.recognize_google(voice)
                # The recognize_google method converts the captured audio (voice) into text using Google's WebSpeech API
                # Requires an active internet connection to process the audio
                instruction = instruction.lower()  # To make sure uniformity in text
                print(f"Recognized Command: {instruction}")  # Debugging
                return instruction
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand. Please try again.")
            return None
        except sr.RequestError:
            self.speak("There seems to be an internet issue.")
            return None
        except Exception as ex:
            print("Error:", ex)
            return None

    def run_command(self):
        """Process the recognized command."""
        instruction = self.take_command()
        if instruction is None:
            return False

        print(instruction)  # Display the instruction in console
        try:
            if "who are you" in instruction:
                self.speak("I am your voice assistant.")  # Speak the response
            elif "what can you do for me" in instruction:
                self.speak("I can do everything.")  # Speak the response
            elif "open google" in instruction:
                self.speak("Opening Google.")  # Speak the response
                webbrowser.open("https://google.com")  # Open Google in the default browser
            elif "open youtube" in instruction:
                self.speak("Opening YouTube.")  # Speak the response
                webbrowser.open("https://youtube.com")  # Open YouTube in the default browser
            elif "exit" in instruction or "quit" in instruction:
                self.speak("Goodbye!")  # Speak the response before exiting
                return True  # Indicate to exit the loop
            else:
                self.speak("I didn't understand. Can you repeat?")  # Ask user to repeat
        except Exception as ex:
            print("Error while processing command:", ex)
            self.speak("There was an error processing your command.")  # Handle any exception gracefully
            return False
        return False

    def start(self):
        """Greet the user and provide an initial prompt."""
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            wish = "Good Morning"
        elif 12 <= hour < 18:
            wish = "Good Afternoon"
        else:
            wish = "Good Evening"

        self.speak(f"Hello Sir. {wish}. How may I assist you?")  # Speak the greeting

    def start_option(self):
        """Start the assistant in continuous listening mode."""
        self.start()  # Greet the user
        self.run_assistant()  # Start continuous listening

    def run_assistant(self):
        """Continuously listens and processes voice commands."""
        while True:
            exit_loop = self.run_command()  # Run the command and check if the loop should exit
            if exit_loop:
                break  # Exit the loop when instructed
     
    def close_option(self):
        self.root.destroy()
        


# Initialize and run the GUI
root = Tk()
obj = assitance_gui(root)
root.mainloop()
