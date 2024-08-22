from flask import Flask, render_template
from flask_cors import CORS
import os

# Web server configuration
# These environment variables are expected to be set with the necessary Web server details.
WEB_SERVER_HOST = os.environ['WEB_SERVER_HOST']
WEB_SERVER_PORT = os.environ['WEB_SERVER_PORT']

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

@app.route('/')
def home():
    """
    Handles the root URL ('/') request.

    This function renders the 'index.html' template and passes the
    web server host and port as variables to the template.

    Returns:
        str: Rendered HTML template with environment variables.
    """
    # Serve index.html
    return render_template('index.html', WEB_SERVER_HOST=WEB_SERVER_HOST, WEB_SERVER_PORT=WEB_SERVER_PORT)


if __name__ == '__main__':
    # Start the Flask web server
    app.run(debug=True, host='0.0.0.0', port=3000)  # Flask will run in debug mode
