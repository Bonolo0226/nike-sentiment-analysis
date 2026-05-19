# 🔍 SentiView – AI Sentiment Analysis Dashboard

> **Week 3 Project · CAPACITI AI Bootcamp · April 2026**
> Sentiment Analysis & Data Insights

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?logo=streamlit)
![TextBlob](https://img.shields.io/badge/TextBlob-NLP-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 Overview

**NikeSenti** is a portfolio-quality, AI-powered sentiment analysis dashboard built with Python and Streamlit. It classifies text as **Positive**, **Negative**, or **Neutral** using Natural Language Processing (NLP) and presents the results through interactive data visualisations.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 Real-Time Analysis | Instantly analyse any text you type |
| 🗂️ Batch Analysis | Paste multiple lines — analyse them all at once |
| 📂 CSV Upload | Upload your own dataset for bulk analysis |
| 📊 Charts | Pie chart, bar chart, scatter plot, histogram, polarity gauge |
| 📈 KPI Metrics | Total reviews, positive %, negative %, average polarity |
| 📄 Insights Report | Auto-generated summary with key findings |
| ⬇️ Export | Download results as CSV or insights as TXT |
| 🎨 Dark Dashboard | Clean, professional dark-themed UI |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — interactive web dashboard
- **TextBlob** — NLP sentiment scoring
- **Pandas** — data manipulation
- **Matplotlib** — chart generation
- **NumPy** — numerical support

---

## 📁 Project Structure

```
sentiment-analysis-tool/
├── app.py                  # Main Streamlit dashboard
├── sentiment_analyzer.py   # Core NLP functions
├── charts.py               # Matplotlib visualisations
├── styles.css              # Custom CSS for Streamlit
├── reviews.csv             # Sample dataset (35 reviews)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── insights_report.md      # Project insights write-up
├── project_structure.txt   # Folder tree overview
└── .gitignore              # Git exclusion rules
```

---

## 🚀 Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/sentiment-analysis-tool.git
cd sentiment-analysis-tool
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download TextBlob corpora (first run only)
```bash
python -m textblob.download_corpora
```

### 5. Launch the dashboard
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 📊 How It Works

1. Text is cleaned (URLs removed, lowercased, normalised).
2. **TextBlob** processes the text and returns a **polarity score** between -1.0 and +1.0.
3. The score is classified:
   - **Positive** → polarity > 0.05
   - **Negative** → polarity < -0.05
   - **Neutral**  → -0.05 ≤ polarity ≤ 0.05
4. A **subjectivity score** (0 = objective, 1 = subjective) is also returned.
5. Results are visualised with charts and summary statistics.

---

## 🖼️ Screenshots

> *(Add screenshots here after running the app)*

| Analyse Text | Dataset Analysis | Insights Report |
|---|---|---|
| ![text](screenshots/text.png) | ![dataset](screenshots/dataset.png) | ![report](screenshots/report.png) |

---

## 🗃️ Sample Dataset

`reviews.csv` contains **35 product reviews** across 5 categories:
- 📱 Electronics
- 👕 Clothing
- 🚚 Delivery
- 🛎️ Service
- 📦 Packaging

Mix of positive, negative, and neutral reviews for a realistic distribution.

---

## 🔮 Future Improvements

- [ ] Add support for **multilingual** analysis
- [ ] Integrate **VADER** for social-media-specific sentiment
- [ ] Add **word cloud** visualisation
- [ ] Connect to **Twitter/X API** for live tweet analysis
- [ ] Export full PDF report
- [ ] Deploy to **Streamlit Cloud** / **Heroku**

---

## 👤 Author

**[Your Name]**
CAPACITI AI Bootcamp · Cohort April 2026
- GitHub: [@your_username](https://github.com/your_username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
