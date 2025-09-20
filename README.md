 Flight Price Tracker

Flight Price Tracker
====================

A Python script that tracks flight prices using the Amadeus API and sends weekly email reports via Gmail when flights meet your criteria.

Features
--------

*   Searches for flights between a specified origin and destination.
*   Filters flights by a maximum price.
*   Generates a 4-week outlook of available flights for selected days of the week.
*   Sends an email report with flight details and direct Google Flights booking links.
*   Logs all activity in `flight.log` for tracking.

Requirements
------------

*   Python 3.10+
*   [Amadeus for Developers](https://developers.amadeus.com/) account
*   Gmail API credentials (`credentials.json` and `token.json`)
*   Required Python packages:

    pip install amadeus google-auth google-auth-oauthlib google-api-python-client

Setup
-----

1.  Clone this repository:
    
        git clone git@github.com:YOUR_USERNAME/flight-tracker.git
        cd flight-tracker
    
2.  Create a virtual environment and activate it:
    
        python3 -m venv venv
        source venv/bin/activate  # macOS/Linux
    
3.  Install dependencies:
    
        pip install -r requirements.txt
    
4.  Create a `secret.py` file based on `secret.example.py`:
    
        AMADEUS_API_KEY = "YOUR_AMADEUS_KEY"
        AMADEUS_API_SECRET = "YOUR_AMADEUS_SECRET"
        GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        ORIGIN = "SFO"
        DESTINATION = "JFK"
        MAX_PRICE = 300
        DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday"]
        MY_EMAIL = "your_email@gmail.com"
    
5.  Set up Gmail API credentials:
    *   Download `credentials.json` from your Google Cloud project.
    *   Run the authentication flow to generate `token.json`.

Usage
-----

Run the script manually:

    python flight.py

The script will:

*   Search for flights in the next 30 days for the specified days of the week.
*   Generate a report of flights below the specified price.
*   Send the report to your Gmail address with clickable Google Flights links.
*   Log all activity in `flight.log`.

Scheduling Weekly Runs (Optional)
---------------------------------

You can schedule the script to run automatically once a week using `cron` on macOS:

    crontab -e

Example to run every Monday at 9 AM:

    0 9 * * 1 /path/to/venv/bin/python3 /path/to/flight.py >> /path/to/flight.log 2>&1

Security Notes
--------------

*   **Do not commit** `secret.py`, `token.json`, or `credentials.json` to GitHub.
*   Use `.gitignore` to exclude sensitive files:
    
        secret.py
        token.json
        credentials.json
        flight.log
        venv/
        __pycache__/
    

License
-------

This project is open-source and available under the MIT License.
