# api.py
import os
from flask import Flask, request, send_file, make_response
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read Google Apps Script Web App URL
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")

app = Flask(__name__)

# Path to the tracking pixel image
# PIXEL_PATH = os.path.join(os.path.dirname(__file__), "pixel.png")
PIXEL_PATH = "https://cgahzcwiqcblmkwblqaj.supabase.co/storage/v1/object/public/cellular-text-pdf/pixel%20(1).png"

def format_india_timestamp():
    """Return timestamp in DD/MM/YYYY hh:mm AM/PM format (Asia/Kolkata)"""
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    return now.strftime("%d/%m/%Y %I:%M %p")

@app.route("/email/track", methods=["GET", "POST"])
def track():
    track_id = request.args.get("id") or request.form.get("id") or "unknown"
    ts = format_india_timestamp()
    ua = request.headers.get("User-Agent", "")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "")

    # Send tracking event to Google Apps Script
    if APPS_SCRIPT_URL:
        try:
            payload = {
                "id": track_id,
                "ts": ts,
                # "ua": ua,
                # "ip": ip,
            }
            r = requests.post(APPS_SCRIPT_URL, json=payload, timeout=10)
            app.logger.info("Apps Script response: %s", r.text)
        except Exception as e:
            app.logger.error("Failed to POST to Apps Script: %s", e)

    # Return the 1x1 transparent pixel
    try:
        response = make_response(send_file(PIXEL_PATH, mimetype="image/png"))
    except Exception as e:
        app.logger.error("Missing pixel image: %s", e)
        return ("", 204)

    # Prevent caching by email clients
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
