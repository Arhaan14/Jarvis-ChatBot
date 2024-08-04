import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
from googletrans import Translator
import requests
import json
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import nltk
from nltk.corpus import wordnet

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        update_ui("Morning Sir!")
        speak("Morning Sir!")
    elif hour >= 12 and hour < 16:
        update_ui("Good Afternoon Sir!")  
        speak("Good Afternoon Sir!")   
    else:
        update_ui("Good Evening Sir!")
        speak("Good Evening Sir!")
    update_ui("Jarvis Here. How may I help you")
    speak("Jarvis Here. How may I help you")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_ui("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        update_ui("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        update_ui(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        update_ui("Say that again please...")
        return "None"

def get_word_meaning(word):
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())

    if synonyms:
        meaning = f"Meaning of '{word}': {', '.join(set(synonyms))}"
        return meaning
    else:
        return f"Sorry, I couldn't find the meaning of '{word}'."    

def get_motivational_quote():
    try:
        url = 'https://zenquotes.io/api/random'
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            quote = data[0]['q'] + ' - ' + data[0]['a']
            return quote
        else:
            return "Sorry, I couldn't fetch a motivational quote at the moment."
    except Exception as e:
        return f"Error: {e}"

def suggest_vacation_spots():
    vacation_spots = [
        "1. Goa - Known for its beautiful beaches and vibrant nightlife.",
        "2. Jaipur - The Pink City, famous for its palaces and forts.",
        "3. Kerala - God's Own Country, known for its backwaters and scenic beauty.",
        "4. Ladakh - Famous for its stunning landscapes and monasteries.",
        "5. Rishikesh - The Yoga Capital of the World, great for adventure and spirituality.",
        "6. Agra - Home to the magnificent Taj Mahal.",
        "7. Andaman and Nicobar Islands - Perfect for a tropical getaway.",
        "8. Varanasi - One of the oldest cities in the world, known for its spiritual significance.",
        "9. Udaipur - The City of Lakes, known for its romantic setting and palaces.",
        "10. Manali - A beautiful hill station, ideal for trekking and adventure sports."
    ]
    vacation_message = "Here are some of the best places to visit in India:\n" + "\n".join(vacation_spots)
    update_ui(vacation_message)
    speak(vacation_message)

def get_weather(city):
    api_key = "2eeeb6e35d9bf3c274858cf5bfb398eb"  
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if response.status_code == 200:
        try:
            weather_info = data["main"]
            temperature = weather_info["temp"]
            humidity = weather_info["humidity"]
            weather_description = data["weather"][0]["description"]
            return f"The temperature in {city} is {temperature}°C with {humidity}% humidity. The weather is {weather_description}."
        except KeyError:
            return "Error: Weather information not available."
    else:
        return f"Error: Unable to retrieve weather data for {city}. Status code: {response.status_code}"

def searchGoogle(query):
    search_url = f"https://www.google.com/search?q={query}"
    speak("Searching, Right Away")
    webbrowser.open(search_url)

def fetch_joke():
    try:
        url = 'https://icanhazdadjoke.com/'
        headers = {'Accept': 'text/plain'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            joke_text = response.text.strip()
            return joke_text
        else:
            return "Sorry, I couldn't fetch a joke at the moment."
    except Exception as e:
        return f"Error: {e}"

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text    

def ask_language():
    speak("Which language would you like to translate to?")
    target_language = input("Enter target language (e.g., 'fr' for French): ")
    return target_language

def update_ui(text):
    output_text.configure(state='normal')
    output_text.insert(tk.END, text + '\n')
    output_text.configure(state='disabled')
    output_text.see(tk.END)

def handle_query():
    query = takeCommand().lower()

    if 'weather in' in query:
        speak("Sure, please tell me the city name.")
        city = takeCommand()
        if city == "none":
            return
        elif city.lower() == "exit":
            speak("Goodbye!")
            exit()
        else:
            weather_info = get_weather(city)
            update_ui(weather_info)
            speak(weather_info)    

    elif 'motivational quote' in query:
        quote = get_motivational_quote()
        update_ui(quote)
        speak("Sure!")
        speak(quote)

    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        update_ui("According to Wikipedia")
        update_ui(results)
        speak("According to Wikipedia")
        speak(results)

    elif 'tell me a joke' in query:
        joke = fetch_joke()
        update_ui(joke)
        speak("Sure!")
        speak(joke)

    elif 'meaning of' in query:
        word = query.split("meaning of ")[-1].strip()
        meaning = get_word_meaning(word)
        update_ui(meaning)
        speak(meaning)     
            
    elif 'i want to go on vacation' in query or 'suggest me some places to travel in India' in query or 'vacation' in query:
        suggest_vacation_spots()

    elif 'i want to hear music' in query or 'play music' in query:
        music_dir = "C:\\Users\\elvis\\OneDrive\\Desktop\\Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        update_ui("Playing music.")
        speak("Sure!")    

    elif 'translate this' in query:
        speak('Sure, please tell me the text you want to translate.')
        text_to_translate = takeCommand()
        if text_to_translate == 'none' or text_to_translate == 'exit':
            return
        target_language = ask_language()
        translated_text = translate_text(text_to_translate, target_language)
        update_ui(f"The translated text is: {translated_text}")
        speak(f"The translated text is: {translated_text}")
        speak("Danke!")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        update_ui(f"Sir, the time is {strTime}")
        speak(f"Sir, the time is {strTime}")

    elif 'open code' in query:
        codePath = "C:\\Users\\elvis\\OneDrive\\Desktop\\Visual Studio Code"
        os.startfile(codePath)
        update_ui("Opening Visual Studio Code.")
        speak("Opening Visual Studio Code.")

    elif 'open quotation' in query:
        quote = "C:\\Users\\elvis\\OneDrive\\Desktop\\Quotation.webp"
        os.startfile(quote)
        update_ui("Opening quotation.")
        speak("Opening quotation.")

    elif 'who made you' in query or 'who created you' in query:
        linkedin_url = "https://www.linkedin.com/in/arhaan-khan/"
        webbrowser.open(linkedin_url)
        update_ui('Arhaan Khan')
        speak('Arhaan Khan')

    elif 'how are you' in query:
        update_ui('I am fine Sir, Thanks For Asking')
        speak('I am fine Sir, Thanks For Asking, What can I do for you today')   

    elif 'pagal hai kya' in query:
        update_ui('get Lost Idiot')
        speak('get Lost Idiot')

    elif 'i want to marry someone' in query:
        update_ui('Then what are you waiting for idiot. I am a bot and why are you telling me all this stuff')
        speak('Then what are you waiting for idiot. I am a bot and why are you telling me all this stuff')

    elif "jarvis quit" in query:
        update_ui('Thanks For Using Me')
        speak('Thanks For Using Me')
        exit()

    else:
        sites = [["youtube", "https://www.youtube.com"], ["google", "https://www.google.com"],["stack overflow", "https://www.stackoverflow.com"], ["whatsapp", "https://www.web.whatsapp.com"], ["flipkart","https://www.flipkart.com"], ["twitter","https://x.com/nbcnews"] ,["amazon","https://www.amazon.in"]]
        for site in sites:
            if f"open {site[0]}" in query:
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                update_ui(f"Opening {site[0]} sir...")
                break
        else:
            searchGoogle(query)
            update_ui("Searching on Google!")    

def on_start_button_click():
    handle_query()

def on_exit_button_click():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

root = tk.Tk()
root.title("Jarvis")

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20, font=("Helvetica", 15))
output_text.pack(pady=10)

start_button = tk.Button(root, text="Start Listening", command=on_start_button_click, font=("Helvetica", 15))
start_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=on_exit_button_click, font=("Helvetica", 15))
exit_button.pack(pady=10)

wishMe()
root.mainloop()
