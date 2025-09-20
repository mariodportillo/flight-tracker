import datetime
import os
import logging
from amadeus import Client, ResponseError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from secret import AMADEUS_API_SECRET, AMADEUS_API_KEY, GMAIL_SCOPES, ORIGIN, DESTINATION, MAX_PRICE, DAYS_OF_WEEK, MY_EMAIL

# -------- PROJECT PATHS --------
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(PROJECT_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(PROJECT_DIR, "credentials.json")  # keep for reference if needed
LOG_FILE = os.path.join(PROJECT_DIR, "flight.log")

# -------- SETUP LOGGING --------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# -------- INIT AMADEUS --------
amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)

def get_flights(origin, destination, departure_date, max_price):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=1,
            currencyCode="USD",
            max=20
        )
        flights = response.data
        filtered = [f for f in flights if float(f["price"]["total"]) <= max_price]
        logging.info(f"Found {len(filtered)} flights for {origin} → {destination} on {departure_date}")
        return filtered
    except ResponseError as error:
        logging.error(f"Amadeus API error for {departure_date}: {error}")
        return []

def send_email(service, to, subject, body):
    message = MIMEMultipart("alternative")
    message["to"] = to
    message["subject"] = subject

    # Simple HTML formatting
    html_body = "<br>".join(body)
    msg = MIMEText(html_body, "html")
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    logging.info(f"Email sent to {to} with subject '{subject}'")

def main():
    today = datetime.date.today()
    report_lines = []

    # Look ahead 30 days for matching weekday flights
    for i in range(30):
        d = today + datetime.timedelta(days=i)
        if d.strftime("%A") in DAYS_OF_WEEK:
            flights = get_flights(ORIGIN, DESTINATION, d.isoformat(), MAX_PRICE)
            if flights:
                report_lines.append(f"<b>--- {d.strftime('%A %Y-%m-%d')} ---</b>")
                for f in flights:
                    dep = f['itineraries'][0]['segments'][0]['departure']['iataCode']
                    arr = f['itineraries'][0]['segments'][-1]['arrival']['iataCode']
                    price = f['price']['total']
                    date = f['itineraries'][0]['segments'][0]['departure']['at'].split("T")[0]

                    # Google Flights link
                    link = f"https://www.google.com/travel/flights?q={dep}.{arr}.{date}"

                    # Add to report
                    report_lines.append(f"{dep} → {arr} | Price: ${price} | <a href='{link}'>Book here</a>")
                report_lines.append("")  # blank line between days

    # Only send if flights were found
    if report_lines:
        if not os.path.exists(TOKEN_PATH):
            logging.error(f"token.json not found at {TOKEN_PATH}. Please run init_gmail.py first.")
            return

        creds = Credentials.from_authorized_user_file(TOKEN_PATH, GMAIL_SCOPES)
        service = build("gmail", "v1", credentials=creds)

        subject = f"✈️ Flight Price Report ({today} → {today + datetime.timedelta(days=30)}) ✈️ "
        send_email(service, MY_EMAIL, subject, report_lines)
    else:
        logging.info("No flights found under criteria.")

if __name__ == "__main__":
    logging.info("==== Flight Tracker Run Started ====")
    main()
    logging.info("==== Flight Tracker Run Finished ====\n")
