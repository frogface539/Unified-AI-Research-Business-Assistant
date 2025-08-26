# 🧠 Unified AI Research & Business Assistant

An AI-powered assistant built with **LangChain**, **Groq LLMs**, and **Streamlit**, that helps you:

1. 🔍 **Research any topic** in real-time using **Wikipedia**, **Arxiv**, and **Web Search (Tavily)**
2. 🛒 **Analyze Shopify stores** — fetch sales data (private mode with API key) or product catalogs (public mode)
3. 📝 **Save reports automatically** as structured Markdown notes

---

## ✨ Features

* **AI Research Agent**

  * Summarizes findings from Wikipedia, Arxiv, and Tavily Search
  * Combines results into a concise, well-structured summary
  * Saves both summary & sources to `/notes`

* **Shopify Analyzer**

  * 🔓 Public Mode → Scrape products/inventory from any Shopify store via `/products.json`
  * 🔒 Private Mode → Use your Shopify Admin API credentials to get **orders, sales, products, inventory**
  * Detects low-stock products automatically

* **Streamlit Web App**

  * Interactive UI with two tabs: **Research** and **Shopify Analyzer**
  * Results saved to notes folder in Markdown format

---

## 📂 Project Structure

```
Unified-AI-Research-Business-Assistant/
│── app.py                # Streamlit UI
│── research_agent.py      # Research + Shopify logic
│── notetaker.py           # Save notes as Markdown
│── config.py              # API keys (gitignored)
│── requirements.txt       # Dependencies
│── notes/                 # Auto-generated research + business reports
│── .gitignore
│── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/Unified-AI-Research-Business-Assistant.git
cd Unified-AI-Research-Business-Assistant
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Configure API Keys

Create a file named **`config.py`** (this file is `.gitignore`d) and add:

```python
# config.py
GROQ_API_KEY = "your_groq_api_key"
MODEL_NAME = "llama2-70b-4096"   # or any supported Groq model

TAVILY_API_KEY = "your_tavily_api_key"

# Private Shopify (optional)
SHOPIFY_ACCESS_TOKEN = "your_private_access_token"
SHOPIFY_STORE_URL = "yourstore.myshopify.com"
```

👉 Public Shopify scraping requires **no keys** — just enter any Shopify store domain.

---

## 🚀 Running the App

```bash
streamlit run app.py
```
---

## 🛠 Example Usage

### 🔍 Research Agent

Input: `Generative AI in Healthcare`
Output:

* Bullet-point summary
* JSON sources from Wikipedia, Arxiv, Tavily
* Markdown note in `/notes/`

### 🛒 Shopify Analyzer

* Public Mode: Enter `xyz.com` → gets product list
* Private Mode: Uses your API credentials → gets sales, orders, inventory alerts

---

## 🧰 Tech Stack

* **[LangChain](https://www.langchain.com/)** – AI orchestration
* **[Groq](https://groq.com/)** – LLM inference
* **[Tavily Search](https://tavily.com/)** – Real-time web results
* **[Streamlit](https://streamlit.io/)** – Frontend UI
* **Shopify Admin API** – Business analytics

---

## 🌐 Connect with Me

* [GitHub](https://github.com/frogface539)
* [LinkedIn](https://www.linkedin.com/in/lakshay-jain-a48979289/)