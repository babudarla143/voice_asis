import tkinter as tk
from tkinter import ttk
import pyttsx3 as py
import speech_recognition as sr
import webbrowser as web
import datetime
import os
import pyjokes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.generativeai import GenerativeModel, configure
import time

save = None

def listening():
    recognizer = sr.Recognizer()
    with sr.Microphone() as data:
        recognizer.adjust_for_ambient_noise(data)
        try:
            global text
            audio = recognizer.listen(data, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            textbox.insert(tk.END, f"You said: {text}\n")
            process_command(text.lower())
        except sr.UnknownValueError:
            textbox.insert(tk.END, f"Sorry, I couldn't understand what you are saying.\n")
            speak("Sorry, I couldn't understand what you are saying.")
        except sr.WaitTimeoutError:
            textbox.insert(tk.END, f'Listening time out, no speech detected\n')
            speak('Listening time out, no speech detected')
        except sr.RequestError as e:
            textbox.insert(tk.END, f"Please check the internet connection\n")
            speak("Please check the internet connection")

def process_command(command):
    if "hello" in command or "siri" in command or "hey siri" in command:
        textbox.insert(tk.END, f"Hi, how are you sir!\n")
        speak("Hi, how are you sir!")
    elif "time" in command:
        tell_time()
    elif "open" in command:
        names = command.replace("open", "").strip()
        speak('opening')
        opening(names)
    elif "what is your name" in command or "what's your name" in command:
        speak("My name is Mawa, sir. I'm here to assist you.")
    elif "what's up" in command:
        speak("Nothing much, just chilling.")
    elif "i love you" in command:
        speak("I love you too.")
    elif "fuck off" in command or "fuck you" in command:
        speak("Sorry, sir, if I did any mistake.")
    elif "how are you" in command:
        speak("I am good, sir. How about you?")
    elif "tell me a joke" in command or "tell me joke" in command or "joke" in command:
        tell_joke()
    elif "tell me" in command or "tell me about" in command:
        search = command
        open_website(search)
    elif "go to" in command or "move to" in command:
        paths = command.replace("go to", "").strip()
        go(paths)
    elif any(kw in command for kw in ["what", "who", "which", "where", "do", "did", "how", "is", "could", "shall", "will", "when", "should"]):
        chat_responses = chatgpt(command)
        print_text(f"MyGPT: {chat_responses}", textbox) or speak(chat_responses)
    elif "sendmail" in command or "send mail" in command:
        send_mail()
    elif "remember" in command:
        speak("okay")
        remember(command)
    elif "bye" in command or "exit" in command:
        speak("Goodbye, sir! Thank you.")
        root.destroy()
    else:
        speak("Sorry, I don't understand")

def speak(text):
    engine = py.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 146)
    engine.say(text)
    engine.runAndWait()

def tell_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if 0 <= hour < 12:
        greeting = "AM"
        d = "good morning"
    else:
        greeting = "PM"
        d = "good evening"

    current_time = f"{hour}:{minute} {greeting}"
    speak(d)
    speak(f"the current time is {current_time}")

def opening(app):
    os.startfile(app)

def open_website(website):
    web.open(f"https://{website}")

def tell_joke():
    myjoke = pyjokes.get_joke(language='en', category='neutral')
    speak(myjoke)
    textbox.insert(tk.END, f"Joke: {myjoke}\n")

def send_mail():
    speak("Tell me the from email")
    sender_mail = listening()
    speak("Tell me the to email")
    receiver_mail = listening()
    speak("Tell me the subject")
    subject = listening()
    speak("Tell me the body")
    body = listening()

    msg = MIMEMultipart()
    msg["From"] = sender_mail
    msg["To"] = receiver_mail
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, 'your_password')
    server.sendmail(sender_mail, receiver_mail, msg.as_string())
    server.quit()
    speak("Message sent successfully")

def go(item):
    os.startfile(item)

def remember(use):
    global save
    save = use
    speak("Got it")

def enable_speaker():
    speak("Speaker is enabled.")

def disable_speaker():
    speak('Speaker is disabled.')
    speak("What can I do for you?")

def send_message():
    user = entry.get("1.0", tk.END).strip()
    textbox.config(state=tk.NORMAL)
    textbox.insert(tk.END, f"User: {user}\n")
    entry.delete("1.0", tk.END)
    chat_response = chatgpt(user)
    print_text(f"MyGPT: {chat_response}", textbox)  
    textbox.config(state=tk.DISABLED)

def chatgpt(prompt):
    try:
        configure(api_key="AIzaSyCxEQNlPK2dQnWpGOy_wXWuyOE_aqPz_LY")
        model = GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def print_text(output_text, textbox):
    for char in output_text:
        textbox.insert(tk.END, char)
        textbox.update_idletasks() 
        time.sleep(0.02)  
    textbox.insert(tk.END, '\n')
    textbox.yview(tk.END)
    textbox.config(state=tk.DISABLED)

def keys_event(event):
    key = event.keysym
    if key == 'Return' and event.state & 0x1:
        listening()
    elif key == 'Return':
        send_message()

root = tk.Tk()
root.title("Chat Application")

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

new = ttk.Style()
new.configure("Rounded.TButton", borderwidth=50, relief="flat", padding=(10, 10))

speaker_button = ttk.Button(frame, text="Click me", style="Rounded.TButton", command=disable_speaker)
speaker_button.bind("<Button-1>", lambda event: enable_speaker())
speaker_button.place(x=20, y=20)

textbox = tk.Text(frame, width=65, height=35, wrap=tk.WORD, bg='black', fg='white', font=('calibre', 12, 'bold'))
textbox.pack(expand=True, fill='both', padx=20, pady=20)

microphone_button = tk.Button(frame, text='Voice', bg='white', padx=10, pady=10, command=listening)
microphone_button.pack(side='right', pady=5)

entry = tk.Text(frame, width=45, height=4)
entry.pack(side='left', padx=20, pady=6, expand=True)

button = tk.Button(frame, text='Send', command=send_message)
button.pack(side='left', pady=5, padx=4, ipady=4, ipadx=4)

root.bind('<Key>', keys_event)
root.mainloop()

