from datetime import datetime
import json

# Get the current date and time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_data(who, text, first_text):
    # Open the file in append mode to keep adding new logs
    with open("memory_log.txt", "a") as file:
        # Write the text to the file
        if first_text and who != "System":
            file.write(f"\n[{timestamp}]\n{who}: {text}\n")
        else:
            file.write(f"{who}: {text}\n")

temporary_data = {}
PERSISTENT_FILE = "persistent_data.json"

