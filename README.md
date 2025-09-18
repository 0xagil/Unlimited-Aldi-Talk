<div align="center">

[**English**](#-alditalk-data-refresher-) | [**Deutsch**](#-alditalk-daten-refresher-)

</div>

<div align="center">
  <h1 align="center" id="-alditalk-data-refresher-">🚀 AldiTalk Data Refresher 🚀</h1>
  <p align="center">
    <strong>Never run out of high-speed data again!</strong>
    <br />
    This automated script keeps your AldiTalk "unlimited" data plan topped up by periodically calling the refresh endpoint.
    <br />
    Features Telegram notifications and easy deployment with Docker.
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python 3.11">
    <img src="https://img.shields.io/badge/Playwright-Ready-green.svg" alt="Playwright Ready">
    <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker Ready">
  </p>
</div>

---

## ✨ Features

-   **🤖 Automated Login:** Securely logs into your AldiTalk account.
-   **🔄 Automatic Data Refresh:** Continuously calls the API to refresh your data allowance.
-   **📊 Dynamic ID Fetching:** Automatically finds your `subscriptionId` and `offerId`.
-   **🔔 Telegram Notifications:** Get instant updates on successful refreshes, startups, and critical errors.
-   **🐳 Dockerized:** Easy to deploy and run as a background service with Docker.
-   **⚙️ Configurable:** Easily change settings like request intervals in a central `config.py` file.

---

## 🛠️ Setup Guide

Follow these steps to get the AldiTalk Refresher up and running.

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started) (Recommended for deployment)
-   [Python 3.9+](https://www.python.org/downloads/) (For local development)

### Step 1: Clone the Repository

Open your terminal and clone this repository to your local machine.

```bash
git clone https://github.com/0xagil/Unlimited-Aldi-Talk
cd AldiTalkRefresher
```

### Step 2: Configure Your Credentials

The most important step is to configure your personal details.

1.  If it doesn't exist, create a `config.py` file.
2.  Fill in the following details:

    ```python
    # --- AldiTalk Credentials ---
    PHONE_NUMBER = "YOUR_PHONE_NUMBER"  # Your AldiTalk mobile number
    PASSWORD = "YOUR_PASSWORD"          # Your AldiTalk customer portal password

    # --- Telegram Bot Configuration ---
    TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
    ```

#### How to get your Telegram credentials:

-   **`TELEGRAM_BOT_TOKEN`**:
    1.  Open Telegram and search for the `@BotFather`.
    2.  Start a chat and send `/newbot`.
    3.  Follow the instructions to name your bot.
    4.  BotFather will give you a unique token. Copy and paste it here.
-   **`TELEGRAM_CHAT_ID`**:
    1.  Search for the `@userinfobot`.
    2.  Start a chat and it will immediately give you your `Chat ID`.
    3.  Copy and paste it here.

### Step 3: Run the Application

You have two options to run the script. Docker is the recommended method for a stable, "set-it-and-forget-it" deployment.

#### Option A: Run with Docker (Recommended)

This is the easiest way to run the script 24/7.

1.  **Build the Docker image:**

    ```bash
    docker build -t alditalk-refresher .
    ```

2.  **Run the container in detached mode:**
    This will start the container in the background.

    ```bash
    docker run -d --name aldi-refresher alditalk-refresher
    ```

    You're all set! The script is now running in the background.

#### Option B: Run Locally with Python

Use this method for testing or if you prefer not to use Docker.

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright's browser dependencies:**

    ```bash
    playwright install chromium
    ```

4.  **Run the script:**
    ```bash
    python main.py
    ```

---

## ⚙️ Usage

-   **Check Logs (Docker):** To see what the script is doing, you can check the container's logs.

    ```bash
    # Follow logs in real-time
    docker logs -f aldi-refresher

    # View all past logs
    docker logs aldi-refresher
    ```

-   **Stop the Container:**

    ```bash
    docker stop aldi-refresher
    ```

-   **Restart the Container:**
    ```bash
    docker start aldi-refresher
    ```

---

## DISCLAIMER

This script is for personal and educational use only. The developers are not responsible for any misuse or any issues that arise with your AldiTalk account. Use at your own risk.

---
<br>
<br>
---

<div align="center">
  <h1 align="center" id="-alditalk-daten-refresher-">🚀 AldiTalk Daten-Refresher 🚀</h1>
  <p align="center">
    <strong>Nie wieder ohne High-Speed-Daten!</strong>
    <br />
    Dieses automatisierte Skript hält deinen AldiTalk "unlimited" Datentarif aufgefrischt, indem es periodisch den Refresh-Endpunkt aufruft.
    <br />
    Mit Telegram-Benachrichtigungen und einfacher Bereitstellung über Docker.
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python 3.11">
    <img src="https://img.shields.io/badge/Playwright-Ready-green.svg" alt="Playwright Ready">
    <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker Ready">
  </p>
</div>

---

## ✨ Funktionen

-   **🤖 Automatisierte Anmeldung:** Meldet sich sicher in deinem AldiTalk-Konto an.
-   **🔄 Automatischer Daten-Refresh:** Ruft kontinuierlich die API auf, um dein Datenvolumen zu erneuern.
-   **📊 Dynamisches Abrufen von IDs:** Findet automatisch deine `subscriptionId` und `offerId`.
-   **🔔 Telegram-Benachrichtigungen:** Erhalte sofortige Updates bei erfolgreichen Aktualisierungen, beim Start und bei kritischen Fehlern.
-   **🐳 Docker-fähig:** Einfach bereitzustellen und als Hintergrunddienst mit Docker auszuführen.
-   **⚙️ Konfigurierbar:** Ändere einfach Einstellungen wie Anfrageintervalle in einer zentralen `config.py`-Datei.

---

## 🛠️ Einrichtungsanleitung

Befolge diese Schritte, um den AldiTalk Refresher in Betrieb zu nehmen.

### Voraussetzungen

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started) (Empfohlen für die Bereitstellung)
-   [Python 3.9+](https://www.python.org/downloads/) (Für die lokale Entwicklung)

### Schritt 1: Repository klonen

Öffne dein Terminal und klone dieses Repository auf deinen lokalen Rechner.

```bash
git clone https://github.com/0xagil/Unlimited-Aldi-Talk
cd AldiTalkRefresher
```

### Schritt 2: Anmeldedaten konfigurieren

Der wichtigste Schritt ist die Konfiguration deiner persönlichen Daten.

1.  Falls sie nicht existiert, erstelle eine `config.py`-Datei.
2.  Fülle die folgenden Details aus:

    ```python
    # --- AldiTalk Anmeldedaten ---
    PHONE_NUMBER = "DEINE_RUFNUMMER"  # Deine AldiTalk-Rufnummer
    PASSWORD = "DEIN_PASSWORT"          # Dein Passwort für das AldiTalk-Kundenportal

    # --- Telegram Bot Konfiguration ---
    TELEGRAM_BOT_TOKEN = "DEIN_TELEGRAM_BOT_TOKEN"
    TELEGRAM_CHAT_ID = "DEINE_TELEGRAM_CHAT_ID"
    ```

#### So erhältst du deine Telegram-Anmeldedaten:

-   **`TELEGRAM_BOT_TOKEN`**:
    1.  Öffne Telegram und suche nach dem `@BotFather`.
    2.  Starte einen Chat und sende `/newbot`.
    3.  Folge den Anweisungen, um deinem Bot einen Namen zu geben.
    4.  Der BotFather gibt dir einen einzigartigen Token. Kopiere ihn und füge ihn hier ein.
-   **`TELEGRAM_CHAT_ID`**:
    1.  Suche nach dem `@userinfobot`.
    2.  Starte einen Chat und er wird dir sofort deine `Chat ID` geben.
    3.  Kopiere sie und füge sie hier ein.

### Schritt 3: Anwendung ausführen

Du hast zwei Möglichkeiten, das Skript auszuführen. Docker ist die empfohlene Methode für eine stabile Bereitstellung, die "einmal einrichten und vergessen" ist.

#### Option A: Mit Docker ausführen (Empfohlen)

Dies ist der einfachste Weg, das Skript rund um die Uhr laufen zu lassen.

1.  **Baue das Docker-Image:**

    ```bash
    docker build -t alditalk-refresher .
    ```

2.  **Führe den Container im Hintergrundmodus aus:**
    Dadurch wird der Container im Hintergrund gestartet.

    ```bash
    docker run -d --name aldi-refresher alditalk-refresher
    ```

    Fertig! Das Skript läuft jetzt im Hintergrund.

#### Option B: Lokal mit Python ausführen

Verwende diese Methode zum Testen oder wenn du Docker nicht verwenden möchtest.

1.  **Erstelle eine virtuelle Umgebung:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Unter Windows, verwende `venv\Scripts\activate`
    ```

2.  **Installiere die erforderlichen Pakete:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Installiere die Browser-Abhängigkeiten von Playwright:**

    ```bash
    playwright install chromium
    ```

4.  **Führe das Skript aus:**
    ```bash
    python main.py
    ```

---

## ⚙️ Verwendung

-   **Logs überprüfen (Docker):** Um zu sehen, was das Skript tut, kannst du die Logs des Containers überprüfen.

    ```bash
    # Logs in Echtzeit verfolgen
    docker logs -f aldi-refresher

    # Alle vergangenen Logs anzeigen
    docker logs aldi-refresher
    ```

-   **Container anhalten:**

    ```bash
    docker stop aldi-refresher
    ```

-   **Container neu starten:**
    ```bash
    docker start aldi-refresher
    ```

---

## HAFTUNGSAUSSCHLUSS

Dieses Skript ist nur für den persönlichen und bildungsbezogenen Gebrauch bestimmt. Die Entwickler sind nicht verantwortlich für Missbrauch oder Probleme, die mit deinem AldiTalk-Konto auftreten. Benutzung auf eigene Gefahr.
