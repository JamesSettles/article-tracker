import subprocess
import webbrowser
import time

def open_flask_app():
    # Start the Flask app in a new subprocess
    subprocess.Popen(['python', 'app/app.py'])
    # Wait a few seconds to ensure the Flask app has started
    time.sleep(5)
    # Open the default web browser to the Flask app URL
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    open_flask_app()
