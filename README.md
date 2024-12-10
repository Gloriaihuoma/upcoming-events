# Events Discovery Application

A Python-based project to discover and track upcoming events in your city! This application fetches event data from the Ticketmaster API, saves the information to a database and CSV file, and provides functionalities to view the stored events. Additionally, a dashboard is built to show details of upcoming events and locations of interest.

## Features

- **Event Search**: Search for events based on city and date range.
- **Save Events**: Store event details in an SQLite database and export to a CSV file.
- **View Events**: Read and display stored events from the database or CSV file.
- **City Options**: Supports multiple cities (e.g., Leeds, Manchester, London).

## How It Works

1. Fetches event data using the Ticketmaster API.
2. Saves event details (e.g., name, date, venue, and location) into:
   - SQLite database (`events.db`)
   - CSV file (`events.csv`)
3. Provides a user interface to view stored events.

## Prerequisites

- Python 3.7+
- API key from Ticketmaster.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Gloriaihuoma/upcoming-events.git
   cd upcoming-events
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Ticketmaster API key:
   Replace the value of `api_key` in the script with your Ticketmaster API key.

## Customization

- **Cities**: Add or modify the cities list in the script.
- **Date Range**: Adjust `start_date` and `end_date` to fetch events for specific periods.
- **File Paths**: Change file paths in the script to store data in custom locations.

## Dependencies

- `requests`: For making API calls to Ticketmaster.
- `sqlite3`: For database operations.
- `csv`: For CSV file handling.



## Contributing

Contributions are welcome! Feel free to:
- Submit bug reports and feature requests.
- Create pull requests for new features or fixes.

## Author

**Gloria**

## Acknowledgments

- [Ticketmaster API](https://developer.ticketmaster.com/) for event data.
- Python community for inspiration and libraries.

## Looker Studio Report

[View the dashboard](https://lookerstudio.google.com/reporting/71802849-dea4-4545-bc24-cb1bffdcd64d) for detailed insights into upcoming events.
```


