from flask import Flask, request, jsonify, render_template
import json
import os
import re
from datetime import datetime

app = Flask(__name__)

# Load entries from JSON file
def load_entries():
    if os.path.exists("entries.json"):
        with open("entries.json", "r") as file:
            return json.load(file).get('entries', [])
    return []

# Save entries to JSON file with sorting by "box_number" and "sl_of_meter"
def save_entries(entries):
    # Sort entries by box_number and sl_of_meter (both converted to integers for proper numeric sorting)
    entries.sort(key=lambda x: (int(x['box_number']), int(x['sl_of_meter'])))
    with open("entries.json", "w") as file:
        json.dump({"entries": entries}, file, indent=4)

# Format entries for display with reordered fields
def format_entries(entries):
    return "\n---\n".join([
        f"Box Number: {entry['box_number']}\nSl of Meter: {entry['sl_of_meter']}\nEntry: {entry['entry']}\nDate: {entry.get('date', 'N/A')}"
        for entry in entries
    ])

# Main route for displaying the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Route to add a new entry
@app.route('/add_entry', methods=['POST'])
def add_entry():
    data = request.json
    
    # Retrieve and process the entry details
    entry = data['entry'].replace("\n", " ").replace("-", " ").strip()
    entry = re.sub(r'\s+', ' ', entry)  # Replace multiple spaces with a single space
    entry = ', '.join(entry.split())  # Add commas between each word in the entry
    
    box_number = data['box_number']
    sl_of_meter = data['sl_of_meter']
    date = data.get('date', '2000-01-01')  # Set default date if none is provided

    # Append new entry to the list and save it
    entries = load_entries()
    entries.append({
        "box_number": box_number,
        "sl_of_meter": sl_of_meter,
        "entry": entry,
        "date": date
    })
    save_entries(entries)
    return jsonify({"success": True})

# Route to get formatted entries
@app.route('/get_formatted_entries')
def get_formatted_entries():
    entries = load_entries()
    formatted_text = format_entries(entries)
    return jsonify({"formattedText": formatted_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
