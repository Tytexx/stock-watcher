# 📈 Stock Market Watcher

A Python-based stock analysis utility that helps users identify companies, gather basic financial information, and retrieve recent news insights based on fuzzy-matched stock names and sectors.


## 🚀 Features

### 🔍 Fuzzy Matching of Company Names

Accepts partial or misspelled stock names and finds the best match from a CSV dataset using `thefuzz`.


### 🏷️ Stock Metadata Fetching

Retrieves stock details including:

- Security code  
- Sector and industry  
- Current price  
- Company overview (from [Screener.in](https://www.screener.in))


### 📰 Latest Sector News

Scrapes Google News to find recent news articles related to the company's sector (from the past 24 hours).


### 🧠 Keyword Mapping by Industry

Built-in dictionary mapping of sectors to keywords commonly found in related news.

## ⚙️ Setup Instructions

Follow the steps below to get **Stock Market Watcher** running on your system:

---

### 1. 📁 Clone the Repository

First, clone the project from GitHub to your local machine:


### 2. 📦 Install Dependencies
Make sure you have Python 3.8 or higher installed. Then, install the required Python packages:

pandas
thefuzz[speedup]
requests
beautifulsoup4

