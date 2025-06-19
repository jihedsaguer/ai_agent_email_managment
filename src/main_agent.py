# main_agent.py

import time
import logging
from datetime import datetime
import argparse

from gmail_connection import get_gmail_service, create_label
from email_classifier import classify_email_rule_based, classify_email_ml_based
from email_actions import apply_labels_and_move, archive_old_emails, flag_urgent_unread_emails
from email_summary import generate_daily_summary

# Configure logging
logging.basicConfig(filename="email_agent.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def process_emails():
    logging.info("Starting email processing.")
    service = get_gmail_service()
    user_id = "me"

    try:
        # 1. Fetch unread messages
        response = service.users().messages().list(userId=user_id, q="is:unread").execute()
        messages = response.get("messages", [])

        if not messages:
            logging.info("No unread messages to process.")
        else:
            logging.info(f"Found {len(messages)} unread messages.")
            for message in messages:
                msg_id = message["id"]
                msg = service.users().messages().get(userId=user_id, id=msg_id, format="full").execute()

                # Extract subject, body, and sender
                headers = msg["payload"]["headers"]
                subject = next(header["value"] for header in headers if header["name"] == "Subject")
                sender = next(header["value"] for header in headers if header["name"] == "From")

                # Get email body (handling multipart messages)
                email_body = ""
                if "parts" in msg["payload"]:
                    for part in msg["payload"]["parts"]:
                        if part["mimeType"] == "text/plain":
                            email_body = part["body"]["data"]
                            break
                elif "body" in msg["payload"]:
                    email_body = msg["payload"]["body"]["data"]
                
                # Decode base64 if necessary
                if email_body:
                    import base64
                    email_body = base64.urlsafe_b64decode(email_body).decode("utf-8")

                logging.info(f"Processing message {msg_id} - Subject: {subject}, From: {sender}")

                # 2. Classify email
                # You can choose between rule-based or ML-based classification here
                classification = classify_email_ml_based(subject, email_body, sender)
                logging.info(f"Message {msg_id} classified as: {classification}")

                # 3. Take action
                apply_labels_and_move(service, user_id, msg_id, classification)

        # 4. Archive old emails
        logging.info("Archiving old emails...")
        archive_old_emails(service, user_id, days_old=30)

        # 5. Flag urgent/unread emails from key contacts
        logging.info("Flagging urgent/unread emails from key contacts...")
        # TODO: Replace with actual key contacts
        flag_urgent_unread_emails(service, user_id, key_contacts=["example@example.com", "another@example.com"])

        # 6. Generate daily summary
        logging.info("Generating daily summary...")
        generate_daily_summary(service, user_id)

    except Exception as e:
        logging.error(f"An error occurred during email processing: {e}")

    logging.info("Email processing finished.")

def main():
    parser = argparse.ArgumentParser(description="Email Agent for classification and organization.")
    parser.add_argument("--run-now", action="store_true", help="Run the email processing immediately.")
    args = parser.parse_args()

    service = get_gmail_service()
    label_name = "MonNouvelAgent"  # Nom du libellé à créer
    create_label(service, label_name)

    if args.run_now:
        results = process_emails()  # Exemple : exécuter l'agent et récupérer les résultats
        print("Résultats de l'agent :")
        print(results)  # Affiche les résultats dans la console
    else:
        print("To run the email agent, use: python3 main_agent.py --run-now")
        print("This script is intended to be run via a scheduler for automated processing.")

if __name__ == "__main__":
    main()
