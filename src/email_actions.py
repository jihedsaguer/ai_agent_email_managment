
# email_actions.py

from datetime import datetime, timedelta

def create_label_if_not_exists(service, user_id, label_name):
    try:
        results = service.users().labels().list(userId=user_id).execute()
        labels = results.get("labels", [])
        
        for label in labels:
            if label["name"] == label_name:
                print("Label ", label_name, " already exists.")
                return label["id"]

        # If label does not exist, create it
        label_body = {
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
        created_label = service.users().labels().create(userId=user_id, body=label_body).execute()
        print("Created label: ", created_label["name"])
        return created_label["id"]

    except Exception as e:
        print("Error creating label ", label_name, ": ", e)
        return None

def apply_labels_and_move(service, user_id, msg_id, classification):
    labels_to_add = []
    labels_to_remove = ["INBOX"]

    # Ensure custom labels exist and get their IDs
    custom_label_names = {
        "Work": "Work",
        "Personal": "Personal",
        "Newsletters": "Newsletters",
        "Promotions": "Promotions",
        "Urgent": "Urgent",
        "Spam": "Spam" 
    }

    # Add the specific classification label
    if classification in custom_label_names:
        label_id = create_label_if_not_exists(service, user_id, custom_label_names[classification])
        if label_id:
            labels_to_add.append(label_id)

    # Add Gmail\'s built-in category labels
    if classification == "Work":
        labels_to_add.append("CATEGORY_PERSONAL") 
    elif classification == "Personal":
        labels_to_add.append("CATEGORY_PERSONAL")
    elif classification == "Newsletters":
        labels_to_add.append("CATEGORY_UPDATES")
    elif classification == "Promotions":
        labels_to_add.append("CATEGORY_PROMOTIONS")
    elif classification == "Urgent":
        labels_to_add.append("IMPORTANT")
    elif classification == "Spam":
        labels_to_add.append("SPAM")
        labels_to_remove.append("INBOX")

    try:
        service.users().messages().modify(userId=user_id, id=msg_id,
                                         body={
                                             "addLabelIds": labels_to_add,
                                             "removeLabelIds": labels_to_remove
                                         }).execute()
        print(f"Applied labels for message {msg_id}: {classification}")
    except Exception as e:
        print(f"Error applying labels for message {msg_id}: {e}")

def archive_old_emails(service, user_id, days_old=30):
    date_before = (datetime.now() - timedelta(days=days_old)).strftime("%Y/%m/%d")
    query = f"before:{date_before} -in:inbox -is:starred"
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get("messages", [])

        if not messages:
            print(f"No emails older than {days_old} days to archive.")
            return

        for message in messages:
            msg_id = message["id"]
            service.users().messages().modify(userId=user_id, id=msg_id,
                                             body={
                                                 "removeLabelIds": ["INBOX"]
                                             }).execute()
            print(f"Archived message {msg_id}")

    except Exception as e:
        print(f"Error archiving old emails: {e}")

def flag_urgent_unread_emails(service, user_id, key_contacts=None):
    if key_contacts is None:
        key_contacts = [] # Example: ["important@example.com", "boss@company.com"]

    query = "is:unread"
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get("messages", [])

        if not messages:
            print("No unread emails to flag.")
            return

        for message in messages:
            msg_id = message["id"]
            msg = service.users().messages().get(userId=user_id, id=msg_id, format="metadata", metadataHeaders=["From"]).execute()
            headers = msg["payload"]["headers"]
            sender = next(header["value"] for header in headers if header["name"] == "From")

            is_key_contact = False
            for contact in key_contacts:
                if contact.lower() in sender.lower():
                    is_key_contact = True
                    break

            if is_key_contact:
                service.users().messages().modify(userId=user_id, id=msg_id,
                                                 body={
                                                     "addLabelIds": ["STARRED"]
                                                 }).execute()
                print(f"Flagged unread email from key contact {sender} (message {msg_id})")

    except Exception as e:
        print(f"Error flagging urgent/unread emails: {e}")


if __name__ == "__main__":
    # This part is for testing purposes and requires a connected Gmail service.
    # You would typically import and use these functions in your main agent script.
    print("This script contains functions for email actions. It needs to be imported and used with a Gmail service object.")
    print("Example usage (assuming \"service\" is a connected Gmail API service object and \"user_id\" is \"me\"): ")
    print("  apply_labels_and_move(service, user_id, \"message_id_here\", \"Work\")")
    print("  archive_old_emails(service, user_id, days_old=30)")
    print("  flag_urgent_unread_emails(service, user_id, key_contacts=[\"important@example.com\"])")


