"""
File: main.py
Author: Eser Inan Arslan
Email: eserinanarslan@gmail.com
Description: Description: This file contains the code for serving predictions about the hotel pricing for Mews.
"""

import pandas as pd
import configparser
import json
import warnings
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request

warnings.filterwarnings("ignore")
pd.set_option('display.float_format', '{:.4f}'.format)

config = configparser.ConfigParser()

# Create a 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG
logger = logging.getLogger(__name__)  # Create a logger instance for this module

# Add a file handler to save logs to a file
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

try:
    config.read('config.ini')
except Exception as e:
    print(f"Error reading config file: {e}")
    # Handle the error as needed, e.g., exit the program or set default values

nb_predictions_string = config.get("Settings", "nb_pred_path")
rf_predictions_string = config.get("Settings", "rf_pred_path")


# Read dataset
try:
    nb_predictions_df = pd.read_csv(nb_predictions_string)
    nb_predictions_df['agent'] = nb_predictions_df['agent'].str.strip()
    nb_predictions_df['company'] = nb_predictions_df['company'].str.strip()


except pd.errors.ParserError as e:
    print(f'Error while parsing CSV file: {e}')
try:
    rf_predictions_df = pd.read_csv(rf_predictions_string)
    rf_predictions_df['agent'] = rf_predictions_df['agent'].str.strip()
    rf_predictions_df['company'] = rf_predictions_df['company'].str.strip()
except pd.errors.ParserError as e:
    print(f'Error while parsing CSV file: {e}')

# Merge the dataframes on common columns
results_df = pd.merge(nb_predictions_df, rf_predictions_df, on=['company', 'agent', 'arrivaldate', 'adr'])

# Rename column names
results_df.columns = ['company', 'agent', 'arrivaldate', 'adr', 'naive_bias_pred',
              'isotonic_naive_bias_pred', 'sigmoid_naive_bias_pred', 'random_forest_pred']

# Display the merged dataframe
print(results_df.shape)

# Convert DataFrame to JSON
try:
    df = results_df.sample(n=50, random_state=42)  # Return the merged DataFrame
    df = df.to_json(orient="records")
    df = json.loads(df)

except Exception as e:
    print(f"Error converting DataFrame to JSON: {e}")
    # Handle the error as needed, e.g., exit the program or set default values

app = Flask(__name__)
app.config["DEBUG"] = True

class PostService:
    def __init__(self, config):
        self.users = {config["User1"]["username"]: config["User1"]["password"],
                      config["User2"]["username"]: config["User2"]["password"]}

    def authenticate(self, username, password):
        return username in self.users and self.users[username] == password

    def get_post_response(self, username):
        #sample_data = results_df.sample(n=50, random_state=42)  # Return the merged DataFrame
        #json_response = sample_data.to_json(orient="records")  # Convert dataframe to JSON
        return df  # Return JSON

# Initialize PostService with config
post_service = PostService(config)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if post_service.authenticate(username, password):
            return post_service.get_post_response(username)
        else:
            logger.warning("Authentication failed for username: %s", username)  # Log authentication failure
            return "Username or Password are not correct or matched each other. Please try again !!"
    return "Please Log in ."

# Run the Flask app
try:
    app.run(host=config["Service"]["Host"], port=int(config["Service"]["Port"]), debug=True)
except Exception as e:
    logger.error("Error running Flask app: %s", e)  # Log the error
    # Handle the error as needed, e.g., exit the program or set default values

