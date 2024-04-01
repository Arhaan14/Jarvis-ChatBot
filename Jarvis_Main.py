import pyttsx3 
import speech_recognition as sr 
import datetime 
import wikipedia
import webbrowser 
import os 
import smtplib 
from googletrans import Translator
import requests 
from bs4 import BeautifulSoup
import mysql.connector


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Establish connection to MySQL database
db_connection = mysql.connector.connect(
    host='localhost',  # or your MySQL server address
    user='root',   # your MySQL username root@localhost
    password='Popatlal@786',  # your MySQL password
    database='Jarvis'  # your database name
)

# Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

def save_to_database(timestamp, query, response):
    sql = "INSERT INTO chatter (timestamp, query, response) VALUES (%s, %s, %s)"
    values = (timestamp, query, response)
    cursor.execute(sql, values)
    db_connection.commit()

def get_response_from_database(query):
    sql = "SELECT response FROM chatter WHERE query LIKE %s"
    value = ('%' + query + '%',)
    cursor.execute(sql, value)
    result = cursor.fetchone()
    if result:
        return result[0]
    # else:
    #     return "Sorry, I don't have a response for that."

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon Sir!")   
    else:
        speak("Good Evening Sir!")
    speak("Jarvis Here. How may I help you")       


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return "None"

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
     speak("Sure, Here are the results of your query.")
     webbrowser.open(search_url)

def fetch_joke():
    try:
        # Fetch a joke from a website (replace the URL with the actual joke website)
        url = 'https://icanhazdadjoke.com/'
        headers = {'Accept': 'text/plain'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse the HTML content of the joke website
            soup = BeautifulSoup(response.text, 'html.parser')
            joke_text = soup.get_text().strip()
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
    # Ask the user for the target language
    speak("Which language would you like to translate to?")
    target_language = input("Enter target language (e.g., 'fr' for French): ")
    return target_language




if __name__ == "__main__":
    wishMe()
    while True:
    #if 1:
        query = takeCommand().lower()

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],["stackoverflow", "https://www.stackoverflow.com"], ["whatsapp", "https://www.web.whatsapp.com"], ["flipkart","https://www.flipkart.com"], ["amazon","https://www.Amazon.in"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])



        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'history' in query:
            cursor.execute("SELECT * FROM chatter")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Chat history is empty.")
        else:
            try:
                bot_response = get_response_from_database(query)
                if bot_response == "Sorry, I don't have a response for that.":
                    speak("I don't have a response for that.")
                else:
                    speak(bot_response)
                # Save the conversation to the database
                save_to_database(timestamp, query, bot_response)
            except Exception as e:
                print(f"Error in database query: {e}")




        if 'weather in' in query:
            speak("Sure, please tell me the city name.")
            city = takeCommand()
            if city == "none":
                continue
            elif city.lower() == "exit":
                speak("Goodbye!")
                break
            else:
                weather_info = get_weather(city)
                speak(weather_info)
    

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        
        if 'tell me a joke' in query:
            joke = fetch_joke()
            speak(joke)
            speak("Goodbye!")
            break
            
        elif 'translate this' in query:
            speak('Sure, please tell me the text you want to translate.')
            text_to_translate = takeCommand()
            if text_to_translate == 'none' or text_to_translate == 'exit':
                continue
            target_language = ask_language()
            translated_text = translate_text(text_to_translate, target_language)
            speak(f"The translated text is: {translated_text}")
            speak("Do you want to translate more text? Say 'exit' to quit.")
    

        elif 'open the way of tears' in query:
            webbrowser.open("youtube.com/watch?v=YiSQ_db-Dcw")          

        elif 'play some music' in query:
            music_dir = "C:\\Users\\elvis\\OneDrive\\Desktop\\Music"
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))


        elif 'the time' in query:
             strTime = datetime.datetime.now().strftime("%H:%M:%S")    
             speak(f"Sir, the time is {strTime}")
 
            
        #elif "the time" in query:
            # musicPath = "C:\\Users\\elvis\\OneDrive\\Desktop\\Music\\Clock Sound"
            # songs = os.listdir(musicPath)
            # print(songs)    
            # os.startfile(os.path.join(musicPath, songs[0]))
            # hour = datetime.datetime.now().strftime("%H")
            # min = datetime.datetime.now().strftime("%M")
            # speak(f"Sir, the time is {hour} and {min} minutes")

        elif 'open code' in query:
            codePath = "C:\\Users\\elvis\\OneDrive\\Desktop\\Visual Studio Code"
            os.startfile(codePath)

        elif 'open quotation' in query:
            quote = "C:\\Users\\elvis\\OneDrive\\Desktop\\Quotation.webp"
            os.startfile(quote)       

        elif 'how are you' in query:
             speak('I am fine Sir, Thanks For Asking')    

        elif 'pagal hai kya' in query:
             speak('get Lost Idiot') 

        elif 'i want to marry someone' in query:
             speak('Then what are you waiting for idiot. I am a bot and why are you telling me all this stuf')          
               
        # elif 'who made you' or 'who created you' in query:
        #       created = "C:\\Users\\elvis\\OneDrive\\Desktop\\All Photos\Bikaner Thar Recent Pics\\2024_02_28_18_27_IMG_2262.JPG"
        #       os.startfile(created)
        #       speak('Arhaan Khan')  


        elif "Jarvis Quit" in query:
            speak('Thanks For Using Me')
        
        else:
            searchGoogle(query) 

    # Close the database connection
    cursor.close()
    db_connection.close()          
     
             
                  









