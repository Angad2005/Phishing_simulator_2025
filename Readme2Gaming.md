# 🎮 Phishing Simulator 2025 🎮

Welcome, agent. You've just been granted access to Phishing Simulator 2025, the ultimate wargaming platform for corporate cybersecurity. Your mission, should you choose to accept it, is to test your organization's human firewall.

> Craft cunning campaigns. Test your team's defenses. Level up your security posture.

---

## Gameplay Features

* 👤 **Build Your Roster:** Recruit your targets. Manage a list of employees who will be the subjects of your "educational" campaigns.
* 🎣 **Design Your Lure:** Craft custom phishing campaigns with enticing subjects and compelling email bodies. Use the special `{{tracking_link}}` tag to plant your payload.
* 🚀 **Mission Control:** View and manage your active campaigns. Remove operatives or delete entire missions before they go live.
* 📤 **Launch the Attack!:** Deploy your campaign with a single click. The simulator will dispatch your carefully crafted emails to the targets.
* 📈 **Track Your Hits:** Get real-time intel. The system logs every click, letting you know who took the bait.
* 📊 **Analyze the Aftermath:** Review your score in the Reports dashboard. See campaign success rates, detailed click logs, and overall performance.
* 🧠 **Strategy Guide:** Receive tactical suggestions based on your campaign results to help you train your team more effectively.

---

## Game Engine

* **Core Logic:** Python, Flask
* **Data Storage:** SQLite (via Flask-SQLAlchemy)
* **Communications Relay:** `smtplib`

---

## Installation & Launch Sequence

To get the simulator running, follow these steps, agent.

1.  **Download the Game Files:**
    ```bash
    git clone <repository_url>
    cd phishing_sim
    ```

2.  **Initialize the Environment:**
    ```bash
    python -m venv venv
    ```
    * **On Windows:** `venv\Scripts\activate`
    * **On macOS/Linux:** `source venv/bin/activate`

3.  **Load Game Assets:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Your Comms Relay (SMTP):**
    This is critical. Open `config.py` and input your credentials. For initial testing, a burner Gmail account is recommended.

    > **WARNING:** To use Gmail, you **must** generate a 16-digit **App Password**. Your regular password will not work and will result in a failed mission.

5.  **Set Your Encryption Key:**
    For security, you must set a secret key as an environment variable.
    * **On Windows:** `set SECRET_KEY=your_super_secret_encryption_key`
    * **On macOS/Linux:** `export SECRET_KEY='your_super_secret_encryption_key'`

6.  **Launch the Simulator!**
    ```bash
    python app.py
    ```
    Access the command console at `http://127.0.0.1:5000/`.

---

## Gameplay Loop

1.  **Recruit Your Targets:** Add employees to your roster.
2.  **Craft the Perfect Phish:** Create a new campaign with a tempting lure.
3.  **Review Your Strategy:** Use the "View/Manage" screen to confirm your targets.
4.  **LAUNCH!:** Deploy the campaign and watch the data roll in.
5.  **See Who Took the Bait:** Head to the Reports dashboard to analyze your success.

---

## Advanced Tactics & Expansion Packs

### Difficulty: Hard Mode - Evading the Spam Filters

New agents often find their first missions get caught by advanced corporate defenses (the "Spam Filter"). This is a feature, not a bug! The enemy AI is smart and looks for:

* **Unregistered Comms Channels:** Using a consumer Gmail account for tactical operations is a rookie move. The enemy AI knows these are not for official business and flags them.
* **Unknown Points of Origin:** Your home base IP address is "cold." It has no reputation. Enemy systems distrust communications from unknown locations.
* **Lack of Authentication Codes (CRITICAL):** Pro-level agents broadcast their identity with `SPF`, `DKIM`, and `DMARC` protocols. Without these, you look like a rogue operator and are instantly sent to the penalty box (the spam folder).

### ⭐ EXPANSION PACK: The Professional Campaigner ⭐

Ready to go pro? To guarantee your missions reach the primary inbox, you need to upgrade your gear.

* **Acquire a Cover Identity:** Purchase a dedicated domain name (e.g., `corporate-security-alerts.com`).
* **Upgrade Your Comms Relay:** Sign up for a professional-grade relay service like SendGrid, Mailgun, or Amazon SES.

These services will equip you with the `SPF` and `DKIM` authentication codes needed to establish a trusted reputation, making you invisible to spam filters.

---

## The Rules of Engagement

This is a simulator, not a weapon. It is designed for education and training with full consent. Use your power responsibly. Good luck, agent.