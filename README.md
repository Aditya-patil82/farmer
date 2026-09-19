# 🌾 Local Farmer Information System (LFIS)

> **College CSE Community Project — Demo / Prototype Application**

A beginner-friendly web application built with **Python Flask** and **SQLite** to help local farmers access crop information, market prices, weather updates, government schemes, farming tips and agricultural contacts — all in one place.

---

## 📋 Project Objective

To create a simple, modern and mobile-friendly web portal that gives farmers easy access to:
- 🌱 Crop profiles and cultivation guidance
- 💰 Local market price data (sample/demo)
- 🌦️ Weather information (demo — extendable to live API)
- 🏛️ Government scheme awareness
- 🧑‍🌾 Practical farming tips
- 📞 Agricultural helplines and contacts

---

## ✨ Features

| Module | Description |
|---|---|
| 🌱 Crop Information | Browse 9+ crop profiles with season, soil, water and cultivation info |
| 💰 Market Prices | View and filter sample market price data by crop |
| 🌦️ Weather | Enter a location — returns demo weather data (ready for API integration) |
| 🏛️ Government Schemes | Awareness cards for PM-KISAN, PMFBY, KCC, Soil Health Card, eNAM |
| 🧑‍🌾 Farming Tips | 16 tips across 6 categories with filter by category |
| 📞 Help & Contacts | Helplines, KVK info, agriculture office placeholders |
| 🔍 Search | Live crop search + market price filter |
| 📱 Responsive | Fully mobile-friendly design |
| 🗄️ SQLite Database | Auto-created with sample data on first run |

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.x, Flask |
| Database | SQLite (built into Python — no separate install needed) |
| Fonts | Google Fonts — Poppins |

---

## 📁 Folder Structure

```
farmer/
│
├── app.py                ← Main Flask application (routes + database)
├── database.db           ← SQLite database (auto-created on first run)
├── requirements.txt      ← Python packages needed
├── README.md             ← This file
│
├── templates/            ← HTML page templates (Jinja2)
│   ├── base.html         ← Base layout (nav + footer) used by all pages
│   ├── index.html        ← Home page
│   ├── crops.html        ← Crop listing with search
│   ├── crop_detail.html  ← Single crop detail page
│   ├── market.html       ← Market prices table with filter
│   ├── weather.html      ← Weather search page
│   ├── schemes.html      ← Government schemes cards
│   ├── tips.html         ← Farming tips with category filter
│   ├── contact.html      ← Help & contacts page
│   ├── 404.html          ← Custom page-not-found error page
│   └── 500.html          ← Custom server error page
│
└── static/               ← CSS and JavaScript files
    ├── style.css         ← Main stylesheet (agriculture green theme)
    └── script.js         ← JavaScript (nav, search, filter, validation)
```

---

## ⚙️ Installation & Setup Guide

### Step 1 — Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.10 or newer** for your operating system
3. Run the installer — **tick "Add Python to PATH"** before clicking Install
4. Verify: open a terminal and type `python --version`

---

### Step 2 — Open the Project in VS Code

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
2. Open VS Code
3. Click **File → Open Folder**
4. Select the `farmer` project folder
5. Install the **Python extension** from the Extensions panel (Ctrl+Shift+X)

---

### Step 3 — Open the Terminal

In VS Code:
- Press **Ctrl + `` ` ``** (backtick key)
- Or go to **Terminal → New Terminal**

---

### Step 4 — Install Dependencies

In the terminal, type:

```bash
pip install -r requirements.txt
```

This installs Flask and its dependencies. You only need to do this once.

---

### Step 5 — Run the Flask Application

```bash
python app.py
```

You will see output like:
```
✅ Database initialised successfully.
🌾 Starting Local Farmer Information System...
📡 Open your browser and go to: http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

---

### Step 6 — Open in Browser

Open your web browser and go to:

**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

The website is now running locally on your computer. 🎉

---

### Step 7 — Stop the Server

Press **Ctrl + C** in the terminal to stop the Flask server.

---

## 📁 File Explanations

| File | What it does |
|---|---|
| `app.py` | The main Python file. Creates the database, defines URL routes, passes data to templates. |
| `database.db` | The SQLite database file. Auto-created on first run. Contains all sample data. |
| `requirements.txt` | Lists Python packages to install (`pip install -r requirements.txt`) |
| `templates/base.html` | The base HTML layout. All other pages extend this for the nav and footer. |
| `templates/index.html` | The home page with the hero section and feature cards. |
| `templates/crops.html` | Lists all crops with a live search box. |
| `templates/crop_detail.html` | Shows full information for a single crop. |
| `templates/market.html` | Market price table with crop filter. |
| `templates/weather.html` | Weather search page (demo data only). |
| `templates/schemes.html` | Government scheme awareness cards. |
| `templates/tips.html` | Farming tips with category filter. |
| `templates/contact.html` | Agricultural helplines and contact info. |
| `static/style.css` | All the CSS styles — green theme, responsive layout, animations. |
| `static/script.js` | JavaScript for mobile menu, live search, filter, form validation. |

---

## 🗄️ Database Structure

The SQLite database (`database.db`) is automatically created when you run `python app.py`. It contains 5 tables:

### `crops`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Crop name (e.g., Rice) |
| season | TEXT | Growing season |
| soil | TEXT | Suitable soil type |
| water_requirement | TEXT | Water needs |
| temperature | TEXT | Optimal temperature range |
| cultivation_info | TEXT | Detailed cultivation notes |
| image_emoji | TEXT | Display emoji for the crop |

### `market_prices`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| crop | TEXT | Crop name |
| market | TEXT | Market name |
| price | REAL | Price value |
| unit | TEXT | Unit (kg, quintal, etc.) |
| date | TEXT | Date of the price record |

### `schemes`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Scheme name |
| description | TEXT | What the scheme is |
| eligibility | TEXT | Who can apply |
| benefits | TEXT | What farmers get |
| application_info | TEXT | How to apply |

### `farming_tips`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| title | TEXT | Tip heading |
| description | TEXT | Detailed tip text |
| category | TEXT | Category (e.g., Irrigation) |

### `contacts`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| name | TEXT | Organisation/person name |
| role | TEXT | Role or type of contact |
| phone | TEXT | Phone number |
| email | TEXT | Email address |
| address | TEXT | Office address |
| note | TEXT | Additional information |

---

## ⚠️ Important Data Notice

| Module | Data Type |
|---|---|
| Market Prices | **Sample/Demo Data** — not real-time market rates |
| Weather | **Demo Data** — not live weather |
| Government Schemes | **Awareness Info** — verify on official portals before applying |
| Contacts | **Partially placeholder** — verify local office numbers |
| Kisan Call Centre 1800-180-1551 | ✅ Verified national toll-free number |

---

## 🚀 Future Improvements

This prototype can be extended with:

1. **Live Weather API** — Integrate OpenWeatherMap or IMD API using environment variables for the API key
2. **Live Market Data** — Connect to AGMARKNET or eNAM for verified real-time prices
3. **Kannada / Regional Language Support** — Add multilingual interface for local farmers
4. **Farmer Login System** — Allow farmers to save preferences, saved tips, alerts
5. **Admin Dashboard** — Let administrators add/edit crops, prices and tips via the web
6. **Real Government Scheme Links** — Link directly to official portals with current URLs
7. **Crop Disease Detection** — Use AI/ML image recognition for plant disease identification
8. **Voice-Based Assistant** — Allow voice queries for non-literate farmers
9. **Location-Based Information** — Show local market prices and weather by GPS
10. **Push Notifications** — Alerts for rain forecasts, price changes, scheme deadlines
11. **Online Expert Consultation** — Connect farmers with agriculture extension officers
12. **SMS Integration** — Send tips and price alerts via SMS for non-smartphone users

---

## ⚡ Limitations

- **No live data** — All prices and weather are sample data
- **No user accounts** — No login or personalisation
- **No admin panel** — Data can only be changed by editing `app.py` directly
- **English only** — No regional language support yet
- **Local only** — Runs only on the computer where `python app.py` is started
- **Development server** — Flask's built-in server is not for production use

---

## 👥 Project Team

College CSE Community Project

---

## 📄 License

This project is for educational purposes only. All data is sample/demo data.
