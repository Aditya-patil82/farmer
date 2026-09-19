# ============================================================
# app.py — Main Flask Application
# Local Farmer Information System
# College CSE/BCA Community Project
# ============================================================
# This file is the heart of the application.
# It handles:
#   - Database creation and sample data insertion
#   - All URL routes (pages the user visits)
#   - Passing data from the database to HTML templates
# ============================================================

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

# Create the Flask application object
app = Flask(__name__)

# Path to the SQLite database file
DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')


# -------------------------------------------------------
# DATABASE HELPER FUNCTIONS
# -------------------------------------------------------

def get_db():
    """Open a new database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row   # Rows behave like dictionaries
    return conn


def init_db():
    """
    Create all tables and insert sample data.
    Called once when the app starts.
    If the tables already exist, nothing bad happens.
    """
    conn = get_db()
    cursor = conn.cursor()

    # ------ Create Tables ------

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT NOT NULL,
            season            TEXT,
            soil              TEXT,
            water_requirement TEXT,
            temperature       TEXT,
            cultivation_info  TEXT,
            image_emoji       TEXT DEFAULT "🌾"
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_prices (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            crop    TEXT NOT NULL,
            market  TEXT,
            price   REAL,
            unit    TEXT,
            date    TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schemes (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            name             TEXT NOT NULL,
            description      TEXT,
            eligibility      TEXT,
            benefits         TEXT,
            application_info TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farming_tips (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            category    TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            role         TEXT,
            phone        TEXT,
            email        TEXT,
            address      TEXT,
            note         TEXT
        )
    ''')

    # ------ Insert Sample Crop Data (only if table is empty) ------
    cursor.execute("SELECT COUNT(*) FROM crops")
    if cursor.fetchone()[0] == 0:
        crops_data = [
            ("Rice", "Kharif (June–November)",
             "Clayey loam, well-drained",
             "High — 1200 to 1800 mm annually",
             "20°C – 37°C",
             "Rice is the most important food crop of India. "
             "Prepare land by ploughing and puddling. "
             "Use certified seeds and treat them before sowing. "
             "Transplant seedlings at 3–4 weeks age. "
             "Apply basal fertilizers (NPK) before transplanting. "
             "Maintain 5 cm standing water during early growth. "
             "Harvest when 80% of grains turn golden yellow.",
             "🌾"),
            ("Ragi (Finger Millet)", "Kharif (June–September)",
             "Sandy loam, red laterite soil",
             "Low to medium — 500 to 900 mm",
             "15°C – 30°C",
             "Ragi is a drought-tolerant millet crop. "
             "It is a nutritious crop rich in calcium and iron. "
             "Sow seeds directly or transplant seedlings. "
             "Requires well-prepared fine tilth seedbed. "
             "Apply farmyard manure before sowing. "
             "Thin plants to 10–15 cm spacing after germination. "
             "Harvest when grains are hard and the plant turns yellowish.",
             "🌿"),
            ("Maize", "Kharif & Rabi",
             "Well-drained loamy soil",
             "Medium — 600 to 900 mm",
             "18°C – 32°C",
             "Maize is a versatile crop used for food, fodder and industry. "
             "Sow seeds at a depth of 3–5 cm with 60×20 cm spacing. "
             "Apply nitrogen fertilizer in split doses. "
             "Irrigate at knee-high stage, tasseling, and grain filling. "
             "Control weeds in the first 30–40 days. "
             "Harvest when husks turn brown and dry.",
             "🌽"),
            ("Wheat", "Rabi (October–March)",
             "Loamy, well-drained, fertile soil",
             "Medium — 450 to 650 mm",
             "10°C – 25°C",
             "Wheat is the main rabi food crop of India. "
             "Sow seeds in rows 20–22 cm apart at 5 cm depth. "
             "Apply phosphorus and potassium before sowing. "
             "First irrigation critical at crown root stage (20–25 DAS). "
             "Total 5–6 irrigations recommended. "
             "Harvest when grains are hard and plants are golden.",
             "🌾"),
            ("Tomato", "Year-round (avoid extreme heat/cold)",
             "Sandy loam, well-drained, rich in organic matter",
             "Moderate — drip or furrow irrigation",
             "20°C – 27°C (optimal)",
             "Tomato is a popular vegetable crop. "
             "Raise nursery seedlings for 25–30 days before transplanting. "
             "Maintain 60×45 cm plant spacing. "
             "Apply compost or FYM at transplanting. "
             "Stake plants to support them as they grow. "
             "Watch for fungal diseases — spray as needed. "
             "Harvest fruits at breaker or mature green stage for market.",
             "🍅"),
            ("Onion", "Rabi (Oct–Nov sowing) & Kharif",
             "Sandy loam to clay loam, well-drained",
             "Moderate — 350 to 550 mm",
             "13°C – 35°C",
             "Onion is one of the most important vegetable crops. "
             "Prepare raised nursery beds and broadcast seeds. "
             "Transplant seedlings at 5–6 weeks age. "
             "Maintain proper drainage — onion dislikes waterlogging. "
             "Apply balanced fertilizers (NPK). "
             "Stop irrigation 10 days before harvest. "
             "Harvest when tops fall over naturally.",
             "🧅"),
            ("Sugarcane", "Year-round (Feb–March main planting)",
             "Deep, well-drained loamy soil",
             "High — 1500 to 2500 mm",
             "20°C – 35°C",
             "Sugarcane is a long-duration cash crop (10–12 months). "
             "Plant two or three budded setts in furrows at 90 cm row spacing. "
             "Apply heavy doses of farmyard manure before planting. "
             "Earthing-up is important to prevent lodging. "
             "Irrigate regularly — critical at tillering and grand growth stages. "
             "Harvest by cutting the cane at the ground level.",
             "🎋"),
            ("Groundnut", "Kharif (June–July) & Rabi (Oct–Nov)",
             "Sandy loam, well-drained, light soil",
             "Low to medium — 500 to 700 mm",
             "20°C – 30°C",
             "Groundnut is an important oilseed and legume crop. "
             "Shell seeds carefully before sowing to avoid damage. "
             "Sow in rows at 30×10 cm spacing at 5 cm depth. "
             "Gypsum application at pegging stage is beneficial. "
             "The crop fixes atmospheric nitrogen — needs less N fertilizer. "
             "Harvest before the rains to prevent aflatoxin contamination.",
             "🥜"),
            ("Cotton", "Kharif (May–June)",
             "Deep black (regur) soil, clay loam",
             "Medium to high — 700 to 1200 mm",
             "21°C – 35°C",
             "Cotton is the most important fiber crop of India. "
             "Use Bt cotton hybrid seeds for better yield and pest resistance. "
             "Maintain 90×60 cm plant spacing. "
             "Apply balanced NPK fertilizers in split doses. "
             "Scout fields regularly for bollworms and sucking pests. "
             "Use integrated pest management (IPM) strategies. "
             "Pick bolls when fully open — avoid delay to prevent quality loss.",
             "☁️"),
        ]
        cursor.executemany(
            "INSERT INTO crops (name, season, soil, water_requirement, temperature, cultivation_info, image_emoji) VALUES (?,?,?,?,?,?,?)",
            crops_data
        )

    # ------ Insert Sample Market Price Data ------
    cursor.execute("SELECT COUNT(*) FROM market_prices")
    if cursor.fetchone()[0] == 0:
        prices_data = [
            ("Tomato",   "Local Market",      25,   "kg",  "19-09-2026"),
            ("Onion",    "Local Market",      30,   "kg",  "19-09-2026"),
            ("Rice",     "Wholesale Market",  32,   "kg",  "19-09-2026"),
            ("Wheat",    "Wholesale Market",  28,   "kg",  "19-09-2026"),
            ("Maize",    "Local Market",      20,   "kg",  "19-09-2026"),
            ("Ragi",     "Local Market",      45,   "kg",  "19-09-2026"),
            ("Groundnut","Wholesale Market",  70,   "kg",  "19-09-2026"),
            ("Cotton",   "Wholesale Market", 620,   "quintal","19-09-2026"),
            ("Sugarcane","Sugar Factory",    350,   "quintal","19-09-2026"),
            ("Tomato",   "Wholesale Market",  18,   "kg",  "18-09-2026"),
            ("Onion",    "Wholesale Market",  25,   "kg",  "18-09-2026"),
            ("Rice",     "Local Market",      35,   "kg",  "18-09-2026"),
        ]
        cursor.executemany(
            "INSERT INTO market_prices (crop, market, price, unit, date) VALUES (?,?,?,?,?)",
            prices_data
        )

    # ------ Insert Sample Government Schemes ------
    cursor.execute("SELECT COUNT(*) FROM schemes")
    if cursor.fetchone()[0] == 0:
        schemes_data = [
            (
                "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                "A central government scheme that provides financial support of ₹6,000 per year to small and marginal farmer families with cultivable land.",
                "Small and marginal farmers with less than 2 hectares of land. (Verify current eligibility criteria on official portal.)",
                "₹6,000 per year paid in three equal instalments of ₹2,000 directly to the farmer's bank account.",
                "Register through the nearest Common Service Centre (CSC), Agriculture office, or visit pmkisan.gov.in. "
                "Aadhaar card, land records and bank passbook required. "
                "Note: Verify current application process on the official portal."
            ),
            (
                "Fasal Bima Yojana (Pradhan Mantri Fasal Bima Yojana — PMFBY)",
                "A crop insurance scheme to protect farmers from financial losses due to natural calamities, pests or diseases.",
                "All farmers — loanee and non-loanee — growing notified crops. (Verify current eligibility criteria on official portal.)",
                "Crop loss compensation for damages due to floods, drought, hailstorm, cyclone, pest attacks and other natural events. "
                "Low premium rates: 2% for Kharif crops, 1.5% for Rabi crops.",
                "Apply through your bank (if loanee farmer), CSC centre or the PMFBY portal. "
                "Application must be made before the deadline for each season. "
                "Note: Verify current application details on the official portal."
            ),
            (
                "Kisan Credit Card (KCC) Scheme",
                "Provides farmers with timely and adequate credit for crop cultivation, post-harvest expenses, maintenance of farm assets and other needs.",
                "Farmers engaged in agriculture, allied activities and non-farm activities. "
                "Both small/marginal farmers and large farmers can apply. "
                "(Verify current eligibility criteria at your bank.)",
                "Credit limit based on landholding and crop. "
                "Short-term loan at subsidised interest rates (typically 4% per annum under interest subvention). "
                "Revolving credit facility.",
                "Apply at any nationalized bank, cooperative bank, or regional rural bank. "
                "Documents needed: land records, ID proof, bank account. "
                "Note: Verify current interest rates and terms at your nearest bank."
            ),
            (
                "Soil Health Card Scheme",
                "Government initiative to issue soil health cards to farmers containing crop-wise recommendations on fertilizers and nutrients needed to maintain soil health.",
                "All farmers across India are eligible. The cards are provided free of cost.",
                "Soil nutrient status assessment of farmland. "
                "Crop-wise fertilizer recommendations to improve yield and reduce input cost. "
                "Helps reduce over-use of chemical fertilizers.",
                "Visit your local Agriculture Department office or Krishi Vigyan Kendra (KVK) for soil testing. "
                "Soil samples will be collected and analysed. "
                "Card will be issued after testing. "
                "Note: Visit soilhealth.dac.gov.in for more information."
            ),
            (
                "National Agriculture Market (eNAM)",
                "An online trading platform for agricultural commodities connecting farmers, traders and buyers across the country.",
                "Farmers registered with their local APMC (Agriculture Produce Market Committee). "
                "(Check your local APMC or agriculture office for registration.)",
                "Access to buyers across India — better price discovery. "
                "Transparent auction process. "
                "Reduced transaction costs and dependence on local middlemen.",
                "Register at your nearest APMC market or visit enam.gov.in. "
                "Aadhaar and bank account required. "
                "Note: Verify current registration process at your local APMC."
            ),
        ]
        cursor.executemany(
            "INSERT INTO schemes (name, description, eligibility, benefits, application_info) VALUES (?,?,?,?,?)",
            schemes_data
        )

    # ------ Insert Sample Farming Tips ------
    cursor.execute("SELECT COUNT(*) FROM farming_tips")
    if cursor.fetchone()[0] == 0:
        tips_data = [
            # Soil Preparation
            ("Test Your Soil First",
             "Before growing any crop, test your soil to know its pH and nutrient levels. "
             "Soil testing helps you apply the right fertilizers and avoid wasteful over-application.",
             "Soil Preparation"),
            ("Add Farmyard Manure",
             "Mix well-decomposed farmyard manure (FYM) or compost into the soil before planting. "
             "This improves soil structure, water retention and provides slow-release nutrients.",
             "Soil Preparation"),
            ("Deep Ploughing",
             "Deep ploughing (30–40 cm) once in 3–4 years breaks hardpan layers and improves root penetration and drainage.",
             "Soil Preparation"),

            # Irrigation
            ("Irrigate at Critical Growth Stages",
             "Water crops at critical growth stages — germination, tillering, flowering and grain/fruit filling. "
             "Missing irrigation at these stages causes significant yield loss.",
             "Irrigation"),
            ("Use Drip Irrigation to Save Water",
             "Drip irrigation delivers water directly to the root zone and can reduce water use by 40–60% "
             "compared to flood irrigation while improving yield.",
             "Irrigation"),
            ("Avoid Waterlogging",
             "Most crops are sensitive to waterlogging. Ensure proper field drainage by making bunds and channels. "
             "Waterlogging suffocates roots and promotes fungal diseases.",
             "Irrigation"),

            # Pest Management
            ("Scout Your Fields Regularly",
             "Walk through your fields at least twice a week to detect pests and diseases early. "
             "Early detection means less damage and lower pesticide cost.",
             "Pest Management"),
            ("Use Integrated Pest Management (IPM)",
             "Combine biological control (natural enemies), cultural practices, resistant varieties and targeted pesticide use "
             "to manage pests sustainably. Avoid spraying as a routine without scouting first.",
             "Pest Management"),
            ("Use Neem-Based Products",
             "Neem oil and neem cake are effective and eco-friendly options for managing many insects and soil pests. "
             "They are safe for beneficial insects when used correctly.",
             "Pest Management"),

            # Crop Care
            ("Use Certified Seeds",
             "Always buy certified seeds from a reputable source or government agricultural department. "
             "Certified seeds give better germination, uniform growth and higher yield.",
             "Crop Care"),
            ("Apply Fertilizers in Split Doses",
             "Apply nitrogen-based fertilizers in 2–3 split doses instead of all at once. "
             "This improves uptake by plants and reduces losses through leaching and volatilisation.",
             "Crop Care"),
            ("Practice Crop Rotation",
             "Do not grow the same crop in the same field every season. "
             "Rotating crops (e.g., cereal → legume) improves soil health and breaks pest and disease cycles.",
             "Crop Care"),

            # Harvesting
            ("Harvest at the Right Stage",
             "Harvesting too early or too late reduces quality and quantity. "
             "Learn the right maturity indicators for each crop — grain colour, moisture, leaf fall, etc.",
             "Harvesting"),
            ("Minimise Harvest Losses",
             "Use proper harvesting tools and techniques. In cereals, losses during cutting, threshing and transportation "
             "can be 5–15% — small improvements save a lot.",
             "Harvesting"),

            # Storage
            ("Dry Grains Properly Before Storage",
             "Grains must be dried to a safe moisture level before storage — typically 12–14% moisture for cereals. "
             "Storing wet grain causes mould, heating and quality loss.",
             "Storage"),
            ("Use Clean, Pest-Free Storage",
             "Clean storage structures thoroughly before filling. "
             "Use hermetic bags or metal silos to protect grain from insects and rodents. "
             "Do not store new grain on top of old grain.",
             "Storage"),
        ]
        cursor.executemany(
            "INSERT INTO farming_tips (title, description, category) VALUES (?,?,?)",
            tips_data
        )

    # ------ Insert Sample Contact Data ------
    cursor.execute("SELECT COUNT(*) FROM contacts")
    if cursor.fetchone()[0] == 0:
        contacts_data = [
            ("Local Agriculture Officer",
             "Agriculture Development Officer (ADO)",
             "[Contact your local Taluk Agriculture Office]",
             "ado@agriculture.gov.in (sample)",
             "Taluk Agriculture Office — visit your nearest office",
             "Sample placeholder — contact your local Taluk Agriculture Office for the verified contact."),
            ("Krishi Vigyan Kendra (KVK)",
             "Agricultural Knowledge & Technology Centre",
             "[Contact your nearest KVK — check icar.org.in/kvk]",
             "kvk@icar.org.in (sample)",
             "Nearest KVK — check the ICAR website for your district",
             "KVKs provide free soil testing, training and guidance. Visit icar.org.in for your nearest KVK."),
            ("National Helpline — Kisan Call Centre",
             "Free Farmer Helpline",
             "1800-180-1551",
             "kisancallcentre@gov.in (sample)",
             "Pan-India — toll free",
             "Toll-free agricultural helpline. Available daily 6 AM to 10 PM in multiple languages."),
            ("PM-KISAN Helpline",
             "PM-KISAN Scheme Support",
             "155261 / 011-24300606",
             "pmkisan-ict@gov.in (sample)",
             "Ministry of Agriculture, New Delhi",
             "For PM-KISAN queries. Verify current numbers at pmkisan.gov.in."),
            ("State Agriculture Department",
             "State Government Agricultural Support",
             "[Contact your State Agriculture Department]",
             "[Check your State Agriculture Department website]",
             "State Agriculture Department Headquarters",
             "Sample placeholder — visit your State Agriculture Department official website for verified contact details."),
            ("Soil Testing Laboratory",
             "Soil Health & Fertility Testing",
             "[Contact your District Soil Testing Lab]",
             "[Check your district agriculture office]",
             "District Agriculture Office or nearest Krishi Vigyan Kendra",
             "Soil testing is usually free or low-cost through government labs. Contact your local KVK or agriculture office."),
        ]
        cursor.executemany(
            "INSERT INTO contacts (name, role, phone, email, address, note) VALUES (?,?,?,?,?,?)",
            contacts_data
        )

    conn.commit()
    conn.close()
    print("[OK] Database initialised successfully.")


# -------------------------------------------------------
# ROUTES — These decide what page the user sees
# -------------------------------------------------------

@app.route('/')
def index():
    """Home page — shows feature cards and hero section."""
    return render_template('index.html')


@app.route('/crops')
def crops():
    """
    Crop listing page.
    Supports search via ?q=cropname query parameter.
    """
    search_query = request.args.get('q', '').strip()
    conn = get_db()

    if search_query:
        crops_list = conn.execute(
            "SELECT * FROM crops WHERE name LIKE ? ORDER BY name",
            (f'%{search_query}%',)
        ).fetchall()
    else:
        crops_list = conn.execute("SELECT * FROM crops ORDER BY name").fetchall()

    conn.close()
    return render_template('crops.html', crops=crops_list, query=search_query)


@app.route('/crop/<int:crop_id>')
def crop_detail(crop_id):
    """
    Crop detail page for a single crop.
    Shows full information about one crop.
    """
    conn = get_db()
    crop = conn.execute("SELECT * FROM crops WHERE id = ?", (crop_id,)).fetchone()
    conn.close()

    if crop is None:
        # If the crop ID doesn't exist, show a 404 error
        abort(404)

    return render_template('crop_detail.html', crop=crop)


@app.route('/market')
def market():
    """
    Market Prices page.
    Supports filter by crop name.
    """
    filter_crop = request.args.get('crop', '').strip()
    conn = get_db()

    if filter_crop:
        prices = conn.execute(
            "SELECT * FROM market_prices WHERE crop LIKE ? ORDER BY date DESC",
            (f'%{filter_crop}%',)
        ).fetchall()
    else:
        prices = conn.execute(
            "SELECT * FROM market_prices ORDER BY date DESC, crop"
        ).fetchall()

    # Get list of unique crops for the filter dropdown
    all_crops = conn.execute(
        "SELECT DISTINCT crop FROM market_prices ORDER BY crop"
    ).fetchall()

    conn.close()
    return render_template('market.html', prices=prices, all_crops=all_crops, filter_crop=filter_crop)


@app.route('/weather')
def weather():
    """
    Weather page.
    Returns demo weather data. Structure is ready for a real API.
    To add a real weather API, add your API call here and pass real data.
    """
    location = request.args.get('location', '').strip()

    # -------------------------------------------------------
    # DEMO DATA — Replace this block with a real weather API
    # when the project is extended in the future.
    # Example: Use OpenWeatherMap API with an environment variable:
    #   api_key = os.environ.get('WEATHER_API_KEY')
    # -------------------------------------------------------
    weather_data = None

    if location:
        # This is SAMPLE/DEMO data — not real weather
        weather_data = {
            'location': location,
            'temperature': 28,
            'condition': 'Partly Cloudy',
            'humidity': 72,
            'wind_speed': 14,
            'rain_possibility': 30,
            'feels_like': 31,
            'is_demo': True   # Flag to display the demo notice in the template
        }

    return render_template('weather.html', weather=weather_data, location=location)


@app.route('/schemes')
def schemes():
    """Government Schemes page — shows all scheme cards from the database."""
    conn = get_db()
    all_schemes = conn.execute("SELECT * FROM schemes ORDER BY id").fetchall()
    conn.close()
    return render_template('schemes.html', schemes=all_schemes)


@app.route('/tips')
def tips():
    """
    Farming Tips page.
    Supports filter by category.
    """
    category = request.args.get('category', '').strip()
    conn = get_db()

    if category:
        all_tips = conn.execute(
            "SELECT * FROM farming_tips WHERE category = ? ORDER BY id",
            (category,)
        ).fetchall()
    else:
        all_tips = conn.execute(
            "SELECT * FROM farming_tips ORDER BY category, id"
        ).fetchall()

    # Get all unique categories for the filter buttons
    categories = conn.execute(
        "SELECT DISTINCT category FROM farming_tips ORDER BY category"
    ).fetchall()

    conn.close()
    return render_template('tips.html', tips=all_tips, categories=categories, active_category=category)


@app.route('/contact')
def contact():
    """Help & Contacts page — shows agricultural contact information."""
    conn = get_db()
    all_contacts = conn.execute("SELECT * FROM contacts ORDER BY id").fetchall()
    conn.close()
    return render_template('contact.html', contacts=all_contacts)


# -------------------------------------------------------
# API ENDPOINT — For future AJAX / mobile app use
# -------------------------------------------------------

@app.route('/api/crops')
def api_crops():
    """Returns crops as JSON — useful for future enhancements."""
    conn = get_db()
    crops_list = conn.execute("SELECT id, name, season, soil, image_emoji FROM crops ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(row) for row in crops_list])


# -------------------------------------------------------
# ERROR HANDLERS
# -------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle unexpected server errors."""
    return render_template('500.html'), 500


# -------------------------------------------------------
# RUN THE APPLICATION
# -------------------------------------------------------

if __name__ == '__main__':
    # Step 1: Make sure the database and tables exist
    init_db()

    # Step 2: Start the Flask development server
    # debug=True means the server restarts automatically when you edit code
    # Do NOT use debug=True in a real production environment
    print("[LFIS] Starting Local Farmer Information System...")
    print("[INFO] Open your browser and go to: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
