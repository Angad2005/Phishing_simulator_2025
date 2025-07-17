# Phishing Simulation Tool

This is a basic Flask-based phishing simulation tool designed to help educate employees about phishing attacks.

## Features

*   **Employee Management:** Add employees with their names and email addresses.
*   **Campaign Creation:** Define phishing campaign details including name, subject, and email body (with a `{{tracking_link}}` placeholder).
*   **Campaign Management:** View campaign details, remove individual recipients, and delete entire campaigns.
*   **Email Sending:** Send simulated phishing emails to selected employees using SMTP.
*   **Click Tracking:** Record when an employee clicks the phishing link.
*   **Basic Reporting:** View campaign summaries (emails sent, clicks, click rate) and detailed click logs.
*   **Awareness Suggestions:** Get basic advice based on simulation results.

## Tech Stack

*   **Backend:** Python, Flask
*   **Database:** SQLite (via Flask-SQLAlchemy)
*   **Email Sending:** `smtplib`

## Setup and Running

1.  **Clone the repository (or create the directory structure and files):**
    ```bash
    mkdir phishing_sim
    cd phishing_sim
    # Create the files as shown above (app.py, config.py, etc.)
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows: `venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure SMTP settings:**
    Open `config.py` and update the following with your actual SMTP server details:
    ```python
    SMTP_SERVER = 'your_smtp_server.com'
    SMTP_PORT = 587  # Or 465 for SSL
    SMTP_USERNAME = 'your_smtp_username'
    SMTP_PASSWORD = 'your_smtp_password' # Use an App Password for Gmail
    SMTP_FROM_ADDRESS = 'no-reply@yourcompany.com' # Email address that appears as sender
    ```
    **WARNING:** Storing credentials directly in `config.py` is not recommended for production. Consider environment variables or a more secure secrets management solution. If using Gmail, you **must** use a 16-digit App Password, not your regular password.

6.  **Set Flask Secret Key (important for security):**
    Set an environment variable for `SECRET_KEY`.
    *   On Windows: `set SECRET_KEY=your_strong_secret_key`
    *   On macOS/Linux: `export SECRET_KEY='your_strong_secret_key'`
    Replace `your_strong_secret_key` with a long, random string.

7.  **Run the Flask application:**
    ```bash
    python app.py
    ```

8.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage Workflow

1.  **Add Employees:** Go to `/employees/add` to add your target employees.
2.  **Create Campaign:** Go to `/campaigns/create` to define your phishing email. Use `{{tracking_link}}` as a placeholder for where the unique tracking URL should go in your email body.
3.  **Manage Campaign:** From the home page, click "View/Manage" to see campaign recipients and remove them if necessary.
4.  **Send Campaign:** From the home page or the management page, click "Send Campaign". Emails will be dispatched to the selected employees.
5.  **View Reports:** Go to `/reports` to see summaries of campaigns and detailed click logs.

---

## Important Considerations & Future Scope

### Why Emails Might Go to Spam

A major challenge with any email-sending application is ensuring emails land in the inbox, not the spam folder. The default configuration of this tool is likely to be flagged as spam for several important reasons:

*   **You're Using a Consumer Service for Bulk Mail:** Sending from `smtp.gmail.com` with a standard Gmail account is meant for person-to-person conversation. When email providers' servers detect an application (your Flask app) sending scripted, identical emails to multiple people, it's a massive red flag. This is not the intended use of a personal Gmail account.

*   **IP Address Reputation:** Your application is sending from a server's IP address (or your home IP address if running locally). These IPs don't have a history of sending good, trusted email and are considered "cold" or untrustworthy by default. Professional email services use dedicated, "warmed-up" IP addresses with a long history of sending legitimate mail.

*   **Lack of Email Authentication (CRITICAL):** This is a huge one. Legitimate senders prove their identity using three key records in their domain's DNS settings. Your setup has none of these.
    *   **SPF (Sender Policy Framework):** This record says, "Only IP addresses X, Y, and Z are allowed to send email for my domain." Since you're sending from a random server IP, it fails this check.
    *   **DKIM (DomainKeys Identified Mail):** This adds a digital signature to your email, proving it hasn't been tampered with and that it genuinely came from your domain. Your emails don't have this signature.
    *   **DMARC (Domain-based Message Authentication, Reporting, and Conformance):** This tells the receiving server what to do if SPF or DKIM fails (e.g., "Reject the email" or "Put it in spam"). Without the first two, DMARC is irrelevant.

## Recommendations for Production Use

**For a serious and effective phishing simulation tool, do not use a personal Gmail account.** To significantly improve email deliverability and appear legitimate to spam filters, you should:

1.  **Purchase a dedicated domain name to send from** (e.g., `my-company-security.com`). This separates your simulation activities from your primary corporate domain.
2.  **Sign up for a professional email sending service** like **SendGrid**, **Mailgun**, or **Amazon SES**.
3.  These services are built for application-based email sending. **They will guide you through setting up SPF and DKIM correctly** for your domain, which will solve the biggest authentication problems and dramatically improve your chances of landing in the inbox.

## Ethical Use

This tool is for educational purposes within an organization, with proper consent and ethical guidelines. Do not use it for malicious activities.