import os  # Import os 
import requests
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
from dotenv import load_dotenv  

#  from .env file
load_dotenv()

#get from .env file
GIF_API_KEY = os.getenv('GIF_API_KEY')  
API_KEY = os.getenv('API_KEY') 
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS') 
EMAIL_PSWRD = os.getenv('EMAIL_PASSWORD')  
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')  
LOCATION = os.getenv('LOCATION')  

def get_weather_data(api_key, location):
   # get weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)  # Send a GET request to the weather API
    return response.json()  

def generate_alert(weather_data):
   # generate weather alert
    weather_condition = weather_data['weather'][0]['main'] 
    temperature = weather_data['main']['temp']  
    wind_speed = weather_data['wind']['speed']  

    # Create the alert message 
    alert_message = f"Weather update for Toronto: \n"
    alert_message += f"Current temperature: {temperature}°C\n"
    alert_message += f"Condition: {weather_condition.capitalize()}\n"
    alert_message += f"Wind speed: {wind_speed} m/s\n"

    # Append specific alerts based on weather conditions
    if 'rain' in weather_condition.lower() or 'drizzle' in weather_condition.lower():
        alert_message += "Alert: It's raining, wear a rain jacket\n"
    elif 'clear' in weather_condition.lower():
        alert_message += "It's a clear day. It's going to be nice today\n"
    if temperature < 10:
        alert_message += "It's going to be cold. Wear layers today\n"
    elif temperature > 25:
        alert_message += "It's going to be hot outside. Enjoy that sun!\n"
    return alert_message  # Return the composed alert message

def get_random_gif(api_key=GIF_API_KEY, tag="weather"):
    #fetch a random GIF from Giphy 
    gif_url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g"  # Giphy API URL
    response = requests.get(gif_url)  # Send a GET request to fetch the GIF
    gif_data = response.json() 
    return gif_data['data']['images']['original']['url']  

def send_email(subject, message, gif_url):
  #  sends an email with the specified subject, message, and GIF
    msg = MIMEMultipart()  
    msg['From'] = EMAIL_ADDRESS  
    msg['To'] = RECIPIENT_EMAIL 
    msg['Subject'] = subject  
    msg.attach(MIMEText(message, 'plain')) 

    # Fetch the GIF image data
    gif_response = requests.get(gif_url)  
    if gif_response.status_code == 200:  # Check if the GIF was retrieved successfully
        gif_image = MIMEImage(gif_response.content)  # Create a MIMEImage object with the GIF content
        gif_image.add_header('Content-ID', '<gif>')  
        msg.attach(gif_image)  

    # Set up the SMTP server for sending the email
    server = SMTP('smtp.gmail.com', 587)  # Create an SMTP server object
    server.starttls()  
    server.login(EMAIL_ADDRESS, EMAIL_PSWRD)  
    server.send_message(msg)  
    server.quit()  # Close the server connection

# Main logic
weather_data = get_weather_data(API_KEY, LOCATION)  # Fetch the current weather data
email_body = generate_alert(weather_data)  # Generate the weather alert message
gif_url = get_random_gif()  # Get a random GIF based on the specified tag
send_email("Today's Weather Alert", email_body, gif_url)  # Send the email with the weather alert and GIF
