
# email_classifier.py

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pickle
import os

# Define email categories
CATEGORIES = ["Work", "Personal", "Newsletters", "Promotions", "Urgent", "Spam"]

# Placeholder for a simple model and vectorizer
# In a real scenario, these would be trained on a dataset.
model = None
vectorizer = None

def train_dummy_model():
    global model, vectorizer
    # Dummy data for training - in a real scenario, this would come from labeled emails
    emails = [
        ("Urgent: Project Deadline", "Urgent"),
        ("Weekly Tech Newsletter", "Newsletters"),
        ("Great Discount on Shoes!", "Promotions"),
        ("Hello from your friend", "Personal"),
        ("You won a lottery!", "Spam"),
        ("Meeting Agenda", "Work"),
        ("Important: Review Document", "Urgent"),
        ("Daily News Digest", "Newsletters"),
        ("Save big on your next purchase", "Promotions"),
        ("Family vacation photos", "Personal"),
        ("Unsubscribe from this list", "Newsletters"),
        ("Your order has shipped", "Promotions"),
        ("Action Required: Account Security", "Urgent"),
        ("Team Sync Meeting", "Work"),
        ("Regarding your recent inquiry", "Work"),
        ("FW: Important Update", "Work"),
        ("Your bill is due", "Urgent"),
        ("Friendship request", "Personal"),
        ("Exclusive offer for you", "Promotions"),
        ("Click here to win", "Spam"),
    ]

    texts = [email[0] for email in emails]
    labels = [email[1] for email in emails]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, labels)

    # Save the trained model and vectorizer
    with open("classifier_model.pkl", "wb") as f:
        pickle.dump({"model": model, "vectorizer": vectorizer}, f)

def load_model():
    global model, vectorizer
    if os.path.exists("classifier_model.pkl"):
        with open("classifier_model.pkl", "rb") as f:
            data = pickle.load(f)
            model = data["model"]
            vectorizer = data["vectorizer"]
    else:
        train_dummy_model()

def classify_email_rule_based(email_subject, email_body, sender_email):
    email_subject = email_subject.lower()
    email_body = email_body.lower()
    sender_email = sender_email.lower()

    # Rule-based classification
    if "urgent" in email_subject or "action required" in email_subject:
        return "Urgent"
    elif "newsletter" in email_subject or "unsubscribe" in email_body:
        return "Newsletters"
    elif "promotion" in email_subject or "discount" in email_subject or "sale" in email_subject:
        return "Promotions"
    elif "spam" in email_subject or "viagra" in email_body or "lottery" in email_body:
        return "Spam"
    elif "work" in email_subject or "meeting" in email_subject or "project" in email_subject or "company.com" in sender_email: # Assuming company.com is a work domain
        return "Work"
    else:
        return "Personal"

def classify_email_ml_based(email_subject, email_body, sender_email):
    if model is None or vectorizer is None:
        load_model()

    text = f"{email_subject} {email_body} {sender_email}"
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    return prediction


if __name__ == "__main__":
    load_model()
    # Example Usage
    print("--- Rule-based Classification ---")
    print(f"'Urgent: Project Deadline' -> {classify_email_rule_based('Urgent: Project Deadline', 'Please complete the report by EOD.', 'manager@company.com')}")
    print(f"'Weekly Tech Newsletter' -> {classify_email_rule_based('Weekly Tech Newsletter', 'Read our latest articles.', 'info@tech-news.com')}")
    print(f"'Great Discount on Shoes!' -> {classify_email_rule_based('Great Discount on Shoes!', 'Limited time offer!', 'sales@shop.com')}")
    print(f"'Hello from your friend' -> {classify_email_rule_based('Hello from your friend', 'How are you doing?', 'friend@example.com')}")
    print(f"'You won a lottery!' -> {classify_email_rule_based('You won a lottery!', 'Click here to claim your prize.', 'scam@bad.com')}")
    print(f"'Meeting Agenda' -> {classify_email_rule_based('Meeting Agenda', 'Please review the attached document.', 'colleague@company.com')}")

    print("\n--- ML-based Classification ---")
    print(f"'Urgent: Project Deadline' -> {classify_email_ml_based('Urgent: Project Deadline', 'Please complete the report by EOD.', 'manager@company.com')}")
    print(f"'Weekly Tech Newsletter' -> {classify_email_ml_based('Weekly Tech Newsletter', 'Read our latest articles.', 'info@tech-news.com')}")
    print(f"'Great Discount on Shoes!' -> {classify_email_ml_based('Great Discount on Shoes!', 'Limited time offer!', 'sales@shop.com')}")
    print(f"'Hello from your friend' -> {classify_email_ml_based('Hello from your friend', 'How are you doing?', 'friend@example.com')}")
    print(f"'You won a lottery!' -> {classify_email_ml_based('You won a lottery!', 'Click here to claim your prize.', 'scam@bad.com')}")
    print(f"'Meeting Agenda' -> {classify_email_ml_based('Meeting Agenda', 'Please review the attached document.', 'colleague@company.com')}")


