import os  # Import os module for environment variables
import requests
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
from dotenv import load_dotenv  # Import load_dotenv from python-dotenv

# Load environment variables from .env file
load_dotenv()

# Constants needed
GIF_API_KEY = os.getenv('GIF_API_KEY')  # Get Giphy API key from environment variable
API_KEY = os.getenv('API_KEY')  # Get OpenWeatherMap API key from environment variable
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Get sender's email address from environment variable
EMAIL_PSWRD = os.getenv('EMAIL_PASSWORD')  # Get sender's email password from environment variable
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')  # Get recipient's email address from environment variable
LOCATION = os.getenv('LOCATION')  # Get location for weather data from environment variable

def get_weather_data(api_key, location):
   # """Fetches the current weather data for the specified location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)  # Send a GET request to the weather API
    return response.json()  # Return the response as a JSON object

def generate_alert(weather_data):
   # """Generates a weather alert message based on the weather data."""
    weather_condition = weather_data['weather'][0]['main']  # Get the main weather condition
    temperature = weather_data['main']['temp']  # Get the current temperature
    wind_speed = weather_data['wind']['speed']  # Get the wind speed

    # Create the alert message with the weather details
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
    #"""Fetches a random GIF from Giphy based on a specified tag."""
    gif_url = f"https://api.giphy.com/v1/gifs/random?api_key={api_key}&tag={tag}&rating=g"  # Giphy API URL
    response = requests.get(gif_url)  # Send a GET request to fetch the GIF
    gif_data = response.json()  # Parse the JSON response
    return gif_data['data']['images']['original']['url']  # Return the original URL of the GIF

def send_email(subject, message, gif_url):
  #  """Sends an email with the specified subject, message, and GIF."""
    msg = MIMEMultipart()  # Create a multipart email message
    msg['From'] = EMAIL_ADDRESS  # Set the sender's email address
    msg['To'] = RECIPIENT_EMAIL  # Set the recipient's email address
    msg['Subject'] = subject  # Set the email subject
    msg.attach(MIMEText(message, 'plain'))  # Attach the message text

    # Fetch the GIF image data
    gif_response = requests.get(gif_url)  # Send a GET request to fetch the GIF
    if gif_response.status_code == 200:  # Check if the GIF was retrieved successfully
        gif_image = MIMEImage(gif_response.content)  # Create a MIMEImage object with the GIF content
        gif_image.add_header('Content-ID', '<gif>')  # Add a header for the GIF
        msg.attach(gif_image)  # Attach the GIF to the email message

    # Set up the SMTP server for sending the email
    server = SMTP('smtp.gmail.com', 587)  # Create an SMTP server object
    server.starttls()  # Start TLS for secure communication
    server.login(EMAIL_ADDRESS, EMAIL_PSWRD)  # Log in to the email account
    server.send_message(msg)  # Send the email message
    server.quit()  # Close the server connection

# Main logic
weather_data = get_weather_data(API_KEY, LOCATION)  # Fetch the current weather data
email_body = generate_alert(weather_data)  # Generate the weather alert message
gif_url = get_random_gif()  # Get a random GIF based on the specified tag
send_email("Today's Weather Alert", email_body, gif_url)  # Send the email with the weather alert and GIF
