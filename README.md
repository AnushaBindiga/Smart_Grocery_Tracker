# Smart Grocery Tracker

A web app built for students in France who want to save money on groceries without spending hours comparing supermarket deals every week.

---

## The Problem

As a student, groceries eat into your budget fast. Carrefour, Lidl, Auchan, Super U, E.Leclerc and Intermarché all have different deals every week — but who has time to check all of them before doing the weekly shop?

---

## The Solution

Add your grocery items by typing or speaking, pick the stores near you, and the app tells you exactly which store to go to this week and how much you will save. No more guessing. No more wasted money.

---

## Features

- Add items by typing or voice in French
- Select only the stores near you
- Live promotion scraping from Carrefour and Auchan
- Smart matching engine compares your list against current deals
- Recommends the best store with exact savings
- Full store comparison ranked by savings
- Mobile friendly — works on your phone
- Scrapers run automatically every morning

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core logic |
| Flask | Web framework |
| SQLite | Database |
| Playwright | Web scraping |
| APScheduler | Daily automation |
| Web Speech API | Voice input |
| HTML + CSS | Frontend |
| Git and GitHub | Version control |

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/AnushaBindiga/Smart_Grocery_Tracker.git
cd Smart_Grocery_Tracker
```

**2. Install dependencies**
```bash
python -m pip install flask beautifulsoup4 requests playwright apscheduler
python -m playwright install
```

**3. Set up database**
```bash
python database.py
python seed_mock_data.py
```

**4. Run scrapers**
```bash
python scrapers/carrefour.py
python scrapers/auchan.py
```

**5. Start the app**
```bash
python app.py
```

**6. Open in browser**
http://127.0.0.1:5000

---

## Scraping Notes

Live scraping works for Carrefour and Auchan. Other stores use realistic mock data due to bot protection — a common real world scraping challenge.

---

## Future Improvements

- English language support
- Barcode scanner to add items
- Price history tracking
- Push notifications for new deals
- Google Maps integration for store locations
- User accounts to save lists

---

## Author

**Anusha Bindiga**
Aspiring Business and Data Analyst
[GitHub](https://github.com/AnushaBindiga)---

## Scraping Notes

Live scraping works for Carrefour and Auchan. Other stores use realistic mock data due to bot protection — a common real world scraping challenge.

---

## Future Improvements

- English language support
- Barcode scanner to add items
- Price history tracking
- Push notifications for new deals
- Google Maps integration for store locations
- User accounts to save lists

---

## Author

**Anusha Bindiga**
Aspiring Business and Data Analyst
[GitHub](https://github.com/AnushaBindiga)