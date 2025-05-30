# Collecting Web Data and Building a Machine Learning Model

This project is a Python-based pipeline for web scraping, data analysis, and machine learning modeling for predicting real estate prices in Albania. It is structured for modular use, including scraping, processing, and training scripts.

---

## 📁 Project Structure

```
scripts/
├── analysis.py         # Presents data analysis on the scraped dataset through visualizations.
├── model.py            # Defines and trains a machine learning model
├── scrape.py           # Script to scrape web data from given URLs
├── script.py           # Main script that coordinates the workflow
├── dataset.csv         # Collected raw dataset
├── rezultatet.csv      # Output results, potentially from the model
├── urls.txt            # Primary list of URLs to scrape
├── urls copy.txt       # Backup or alternate URL list
├── requirements.txt    # Python dependencies
└── .git/               # Git repository metadata
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd scripts
```

### 2. Create Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

1. **Scraping data:**

```bash
python scrape.py
```

2. **Running full pipeline:**

```bash
python script.py
```

3. **Analyzing the results:**

```bash
python analysis.py
```

4. **Training or testing the model:**

```bash
python model.py
```

---

## 🗃 Dataset

- `dataset.csv`: Raw data collected from web scraping.
- `rezultatet.csv`: Processed results, predictions, or evaluation metrics.

---

## 🛠 Requirements

All dependencies are listed in `requirements.txt`. Typical dependencies may include:

- `pandas`
- `requests`
- `beautifulsoup4`
- `scikit-learn`
- `matplotlib`

---

## 📌 Notes

- Ensure you have a stable internet connection while scraping.
- Update `urls.txt` with the appropriate links if needed.

---

