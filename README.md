# Email Agent

This AI agent connects to your Gmail inbox, classifies incoming messages, and organizes them into folders or labels. It can also archive old emails, flag urgent messages from key contacts, and generate daily summaries.

## Features

*   **Email Connection**: Connects to Gmail using the Gmail API.
*   **Secure Authentication**: Uses OAuth2 for secure authentication.
*   **Email Classification**: Classifies emails into categories like Work, Personal, Newsletters, Promotions, Urgent, and Spam using a rule-based system and a lightweight ML model.
*   **Email Organization**: Applies labels, moves emails to folders, archives old emails, and flags urgent/unread emails from key contacts.
*   **Automated Scheduling**: Designed to run automatically at specified intervals.
*   **Logging**: Logs all actions to a local file.
*   **Daily Summary**: Generates a daily summary of important emails and can send it to a Slack channel.
*   **Manual Override**: Provides a command-line interface for manual execution.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd email_agent
```

### 2. Set up Google Cloud Project and Credentials

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project or select an existing one.
3.  Enable the **Gmail API** for your project:
    *   In the navigation menu, go to "APIs & Services" > "Library".
    *   Search for "Gmail API" and click on it.
    *   Click the "Enable" button.
4.  Create **OAuth 2.0 Client ID** credentials:
    *   In the navigation menu, go to "APIs & Services" > "Credentials".
    *   Click "+ Create Credentials" and choose "OAuth client ID".
    *   Select "Desktop app" as the application type and give it a name (e.g., "Email Agent Desktop App").
    *   Click "Create" and then "Download JSON" to get your `client_secrets.json` file.
5.  Rename the downloaded file to `client_secrets.json` and place it in the `email_agent/src/` directory.

### 3. Install Dependencies

Navigate to the `email_agent` directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Initial Gmail API Authorization

The first time you run the agent, it will prompt you to authorize access to your Gmail account:

```bash
cd src
python3 gmail_connection.py
```

Follow the instructions in the console:
1.  Open the provided URL in your web browser.
2.  Authorize access to your Gmail account.
3.  Copy the authorization code displayed in your browser.
4.  Paste the authorization code back into the console and press Enter.

This will create a `token.pickle` file in the `src/` directory, which stores your credentials for future use.

### 5. Configure Slack Integration (Optional)

If you want to enable daily summaries to a Slack channel, set the following environment variables:

```bash
export SLACK_BOT_TOKEN="YOUR_SLACK_BOT_TOKEN"
export SLACK_CHANNEL_ID="YOUR_SLACK_CHANNEL_ID"
```

Replace `YOUR_SLACK_BOT_TOKEN` with your Slack bot token and `YOUR_SLACK_CHANNEL_ID` with the ID of the Slack channel where you want to receive summaries.

### 6. Run the Agent

#### Manual Run

To run the agent manually, navigate to the `src` directory and execute:

```bash
python3 main_agent.py --run-now
```

#### Scheduled Run (Example using Cron)

To schedule the agent to run every 30 minutes (as per requirements), you can use `cron` on Linux systems. Open your crontab for editing:

```bash
crontab -e
```

Add the following line to the crontab. Make sure to replace `/path/to/your/email_agent/src` with the actual absolute path to your `src` directory.

```cron
*/30 * * * * /usr/bin/python3 /path/to/your/email_agent/src/main_agent.py --run-now >> /path/to/your/email_agent/email_agent.log 2>&1
```

This command will run the `main_agent.py` script every 30 minutes and append its output (including logs) to `email_agent.log`.

## Project Structure

```
email_agent/
├── src/
│   ├── gmail_connection.py
│   ├── email_classifier.py
│   ├── email_actions.py
│   ├── email_summary.py
│   ├── main_agent.py
│   └── client_secrets.json
├── docs/
├── data/
├── requirements.txt
└── README.md
```

## Customization

*   **Email Categories**: Modify `email_classifier.py` to adjust rule-based classification or integrate a more sophisticated LLM.
*   **Key Contacts**: Update the `key_contacts` list in `main_agent.py` to flag important emails from specific senders.
*   **Archiving Policy**: Adjust the `days_old` parameter in `archive_old_emails` in `email_actions.py` to change the archiving policy.

## Troubleshooting

*   **`webbrowser.Error: could not locate runnable browser`**: This error occurs because the sandbox environment does not have a graphical browser. The `gmail_connection.py` script has been modified to use a console-based authorization flow.
*   **`Invalid label` errors**: Ensure that the custom labels (Work, Personal, Newsletters, Promotions, Urgent) are created in your Gmail account. The agent will attempt to create them if they don't exist, but sometimes manual intervention might be needed.
*   **`HttpError 403: accessNotConfigured`**: Make sure the Gmail API is enabled in your Google Cloud Project.

## License

[Specify your license here, e.g., MIT License]

