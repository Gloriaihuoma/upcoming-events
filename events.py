import requests
import sqlite3
import csv
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch API key from the .env file
api_key = os.getenv('TICKETMASTER_API_KEY')

def search_events(api_key, city, start_date, end_date):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'apikey': api_key,
        'city': city,
        'locale': 'en',
        'startDateTime': start_date,
        'endDateTime': end_date,
        'size': 20,  # Number of events per page
        'sort': 'date,asc',  # Sort by date in ascending order
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_database(events, city):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT,
            date TEXT,
            type TEXT,
            venue_name TEXT,
            event_location TEXT,
            url TEXT,
            city TEXT
        )
    ''')
    
    for event in events['_embedded']['events']:
        event_id = event['id']
        event_name = event['name']
        event_date = event['dates']['start']['localDate']
        
        event_type = 'Unknown'
        if 'classifications' in event:
            for classification in event['classifications']:
                if 'segment' in classification:
                    event_type = classification['segment']['name']
                    break
         
        venue_name = 'Venue name not available'
        event_location = 'Location not available'
        if '_embedded' in event and 'venues' in event['_embedded'] and len(event['_embedded']['venues']) > 0:
            venue = event['_embedded']['venues'][0]
            venue_name = venue.get('name', venue_name)
            event_location = venue.get('city', {}).get('name', event_location)
        
        event_url = event['url']
        
        cursor.execute('''
            INSERT OR REPLACE INTO events (id, name, date, type, venue_name, event_location, url, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_id, event_name, event_date, event_type, venue_name, event_location, event_url, city))
    
    conn.commit()
    conn.close()

def save_to_csv(events, city):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the CSV file path in the same folder
    csv_file_path = os.path.join(script_dir, 'events.csv')
    # Define the CSV file header
    csv_header = ['id', 'name', 'date', 'type', 'venue_name', 'event_location', 'url', 'city']
    
    # Open the CSV file in append mode
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header if it's a new file
        file_empty = file.tell() == 0
        if file_empty:
            writer.writerow(csv_header)
        
        # Write each event's data
        for event in events['_embedded']['events']:
            event_id = event['id']
            event_name = event['name']
            event_date = event['dates']['start']['localDate']
            
            event_type = 'Unknown'
            if 'classifications' in event:
                for classification in event['classifications']:
                    if 'segment' in classification:
                        event_type = classification['segment']['name']
                        break
            
            venue_name = 'Venue name not available'
            event_location = 'Location not available'
            if '_embedded' in event and 'venues' in event['_embedded'] and len(event['_embedded']['venues']) > 0:
                venue = event['_embedded']['venues'][0]
                venue_name = venue.get('name', venue_name)
                event_location = venue.get('city', {}).get('name', event_location)
            
            event_url = event['url']
            
            writer.writerow([event_id, event_name, event_date, event_type, venue_name, event_location, event_url, city])

# Main script
if not api_key:
    raise ValueError("API key is missing. Please set the TICKETMASTER_API_KEY in your .env file.")

cities = ['Leeds', 'Manchester', 'London']
start_date = '2024-01-01T00:00:00Z'
end_date = '2024-12-31T23:59:59Z'

for city in cities:
    print(f"\nSearching events in {city}...\n")
    events = search_events(api_key, city, start_date, end_date)
    
    if events and '_embedded' in events:
        save_to_database(events, city)
        save_to_csv(events, city)  # Save events to CSV
        print(f"Events saved for {city}.")
    else:
        print(f"No events found in {city}.")


