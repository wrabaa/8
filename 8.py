import datetime
import time
import signal
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import Adafruit_DHT
import speedtest
import requests

# Replace 0x27 with the I2C address of your LCD module
lcd = CharLCD('PCF8574', 0x27)

# Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
API_KEY = 'e2692449d4657dd06c99cd150c33c675'
CITY = 'Beirut, Lebanon'  # Replace with your city and country

# Set up GPIO for LED backlight control
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize the LCD backlight
lcd.backlight_enabled = True  # Turn on backlight initially

target_date = datetime.datetime(2023, 11, 23, 18, 0, 0)

def display_time_date():
    # Get the current time and date
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    # Display the time and date on the LCD
    lcd.clear()
    lcd.write_string(f"Time: {current_time}")
    lcd.crlf()  # Move to the second line
    lcd.write_string(f"Date: {current_date}")

# Rest of your existing functions...

# Add the new countdown-related functions

# ... (remaining functions from the second code)

# ... (cleanup_handler function from the second code)

# Rest of your existing try-except block...

try:
    while True:
        # Display time and date for 20 seconds
        display_time_date()
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the backlight
        time.sleep(20)

        # Get the current temperature and humidity
        humidity, temperature = read_temp_humidity()

        # Display temperature and humidity for 20 seconds
        display_temp_humidity(temperature, humidity)
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the backlight
        time.sleep(20)

        # Measure internet speed
        download_speed, upload_speed = measure_internet_speed()

        # Display internet speed for 20 seconds
        display_internet_speed(download_speed, upload_speed)
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the backlight
        time.sleep(20)

        # Get weather data and display it
        weather_data = get_weather_data()
        if weather_data:
            temperature, humidity, weather_description = weather_data
            display_weather(temperature, humidity, weather_description)
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the backlight
            time.sleep(20)

        # Display countdown information for 20 seconds
        current_time = datetime.datetime.now()
        time_elapsed = current_time - target_date
        if time_elapsed.total_seconds() >= 0:
            lcd.clear()
            lcd.write_string("Countdown finished!")
            lcd.backlight_enabled = False  # Turn off backlight
            time.sleep(2)  # Wait for 2 seconds to display the message
            cleanup_handler(None, None)

        time_remaining = abs(time_elapsed)
        days, seconds = divmod(time_remaining.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        countdown_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Time remaining:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(countdown_str)
        lcd.backlight_enabled = True  # Turn on backlight
        time.sleep(1)

except KeyboardInterrupt:
    cleanup_handler(None, None)
