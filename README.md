<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flight Price Tracker</title>
</head>
<body>
    <h1>Flight Price Tracker</h1>
    <p>A Python script that tracks flight prices using the Amadeus API and sends weekly email reports via Gmail when flights meet your criteria.</p>

    <h2>Features</h2>
    <ul>
        <li>Searches for flights between a specified origin and destination.</li>
        <li>Filters flights by a maximum price.</li>
        <li>Generates a 4-week outlook of available flights for selected days of the week.</li>
        <li>Sends an email report with flight details and direct Google Flights booking links.</li>
        <li>Logs all activity in <code>flight.log</code> for tracking.</li>
    </ul>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.10+</li>
        <li><a href="https://developers.amadeus.com/">Amadeus for Developers</a> account</li>
        <li>Gmail API credentials (<code>credentials.json</code> and <code>token.json</code>)</li>
        <li>Required Python packages:</li>
    </ul>
    <pre><code>pip install amadeus google-auth google-auth-oauthlib google-api-python-client</code></pre>

    <h2>Setup</h2>
    <ol>
        <li>Clone this repository:
            <pre><code>git clone git@github.com:YOUR_USERNAME/flight-tracker.git
cd flight-tracker</code></pre>
        </li>
        <li>Create a virtual environment and activate it:
            <pre><code>python3 -m venv venv
source venv/bin/activate  # macOS/Linux</code></pre>
        </li>
        <li>Install dependencies:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Create a <code>secret.py</code> file based on <code>secret.example.py</code>:
            <pre><code>AMADEUS_API_KEY = "YOUR_AMADEUS_KEY"
AMADEUS_API_SECRET = "YOUR_AMADEUS_SECRET"
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
ORIGIN = "SFO"
DESTINATION = "JFK"
MAX_PRICE = 300
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday"]
MY_EMAIL = "your_email@gmail.com"</code></pre>
        </li>
        <li>Set up Gmail API credentials:
            <ul>
                <li>Download <code>credentials.json</code> from your Google Cloud project.</li>
                <li>Run the authentication flow to generate <code>token.json</code>.</li>
            </ul>
        </li>
    </ol>

    <h2>Usage</h2>
    <p>Run the script manually:</p>
    <pre><code>python flight.py</code></pre>
    <p>The script will:</p>
    <ul>
        <li>Search for flights in the next 30 days for the specified days of the week.</li>
        <li>Generate a report of flights below the specified price.</li>
        <li>Send the report to your Gmail address with clickable Google Flights links.</li>
        <li>Log all activity in <code>flight.log</code>.</li>
    </ul>

    <h2>Scheduling Weekly Runs (Optional)</h2>
    <p>You can schedule the script to run automatically once a week using <code>cron</code> on macOS:</p>
    <pre><code>crontab -e</code></pre>
    <p>Example to run every Monday at 9 AM:</p>
    <pre><code>0 9 * * 1 /path/to/venv/bin/python3 /path/to/flight.py >> /path/to/flight.log 2>&1</code></pre>

    <h2>Security Notes</h2>
    <ul>
        <li><strong>Do not commit</strong> <code>secret.py</code>, <code>token.json</code>, or <code>credentials.json</code> to GitHub.</li>
        <li>Use <code>.gitignore</code> to exclude sensitive files:
            <pre><code>secret.py
token.json
credentials.json
flight.log
venv/
__pycache__/</code></pre>
        </li>
    </ul>

    <h2>License</h2>
    <p>This project is open-source and available under the MIT License.</p>
</body>
</html>
