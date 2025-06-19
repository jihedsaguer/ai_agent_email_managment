
# email_summary.py

import logging
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Configure logging
logging.basicConfig(filename="email_agent.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# TODO: Replace with your Slack Bot Token and Channel ID
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

def send_summary_to_channel(summary_text):
    if not SLACK_BOT_TOKEN or not SLACK_CHANNEL_ID:
        logging.warning("Slack bot token or channel ID not configured. Skipping Slack notification.")
        print("Slack bot token or channel ID not configured. Skipping Slack notification.")
        return

    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=summary_text
        )
        logging.info("Message sent to Slack: {}".format(response["ts"]))
        print("Summary sent to Slack channel.")
    except SlackApiError as e:
        logging.error("Error sending message to Slack: {}".format(e.response["error"]))
        print("Error sending message to Slack: {}".format(e.response["error"]))

def generate_daily_summary(service, user_id):
    logging.info("Generating daily email summary.")
    summary_text = "Daily Email Summary - " + datetime.now().strftime("%Y-%m-%d") + "\n\n"
    
    # Fetch important emails from the last 24 hours
    date_str = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")
    query = "after:{} is:important".format(date_str)
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get("messages", [])

        if not messages:
            summary_text += "No important emails in the last 24 hours.\n"
        else:
            summary_text += "Important Emails (last 24 hours):\n"
            for message in messages:
                msg_id = message["id"]
                msg = service.users().messages().get(userId=user_id, id=msg_id, format="metadata", metadataHeaders=["From", "Subject"]).execute()
                
                headers = msg["payload"]["headers"]
                subject = next(header["value"] for header in headers if header["name"] == "Subject")
                sender = next(header["value"] for header in headers if header["name"] == "From")
                
                summary_text += "- Subject: {}, From: {}\n".format(subject, sender)

    except Exception as e:
        logging.error("Error generating daily summary: {}".format(e))
        summary_text += "Error retrieving important emails: {}\n".format(e)

    send_summary_to_channel(summary_text)
    logging.info("Daily email summary generation finished.")

if __name__ == "__main__":
    # This part is for testing purposes and requires a connected Gmail service.
    # You would typically import and use these functions in your main agent script.
    print("This script contains functions for generating email summaries. It needs to be imported and used with a Gmail service object.")


