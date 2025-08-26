from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import requests
import os
from notetaker import save_note
from config import (
    GROQ_API_KEY,
    TAVILY_API_KEY,
    SHOPIFY_ACCESS_TOKEN,
    SHOPIFY_STORE_URL,
    MODEL_NAME,
)

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME
)

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
tavily = TavilySearch(max_results=3)


def research_agent(query: str) -> dict:
    wiki_result = wiki.run(query)
    arxiv_result = arxiv.run(query)
    tavily_result = tavily.run(query)

    template = """
    You are a research assistant. Summarize the following into clear bullet points.
    DO NOT make up citations. Only summarize from the text.

    Wikipedia:
    {wiki_result}

    Arxiv:
    {arxiv_result}

    Web Search:
    {tavily_result}

    Summary:
    """
    prompt = PromptTemplate(
        input_variables=["wiki_result", "arxiv_result", "tavily_result"],
        template=template,
    )

    final_prompt = prompt.format(
        wiki_result=wiki_result,
        arxiv_result=arxiv_result,
        tavily_result=tavily_result,
    )

    response = llm.invoke(final_prompt)

    return {
        "summary": response.content,
        "sources": {
            "Wikipedia": wiki_result,
            "Arxiv": arxiv_result,
            "Web": tavily_result,
        }
    }


def get_shopify_orders(limit=5):
    url = f"https://{SHOPIFY_STORE_URL}/admin/api/2024-07/orders.json?limit={limit}&status=any"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("orders", [])


def get_shopify_products(limit=5):
    url = f"https://{SHOPIFY_STORE_URL}/admin/api/2024-07/products.json?limit={limit}"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("products", [])


def public_shopify_scraper(store_url: str, limit=10):
    s = store_url.strip().rstrip("/")
    if not s.startswith("http"):
        s = "https://" + s
    url = f"{s}/products.json?limit={limit}"
    resp = requests.get(url, timeout=15)
    data = resp.json()
    products = [
        {
            "title": p.get("title"),
            "price": (p.get("variants") or [{}])[0].get("price"),
            "inventory": (p.get("variants") or [{}])[0].get("inventory_quantity", "N/A"),
            "handle": p.get("handle"),
            "product_type": p.get("product_type"),
            "vendor": p.get("vendor"),
        }
        for p in data.get("products", [])
    ]
    return {"mode": "public", "products": products, "note": "Sales data is private and not available via public endpoints."}


def ecommerce_agent(store_url=None, limit=5, public_mode=False):
    """
    Shopify agent that supports:
    - public mode (scrapes /products.json from any Shopify store)
    - private mode (uses your API token to fetch orders + products)
    """
    try:
        if public_mode and store_url:
            clean_url = store_url.replace("https://", "").replace("http://", "").strip("/")
            api_url = f"https://{clean_url}/products.json?limit={limit}"
            resp = requests.get(api_url, timeout=10)
            resp.raise_for_status()
            products = resp.json().get("products", [])

            top_products = [p["title"] for p in products]
            inventory_alerts = []
            for p in products:
                for v in p.get("variants", []):
                    qty = v.get("inventory_quantity")
                    if qty is not None and qty < 10:
                        inventory_alerts.append(
                            f"{p['title']} (variant {v['title']}) low: {qty} left"
                        )

            return {
                "mode": "public",
                "store": clean_url,
                "total_sales": "N/A (not accessible in public mode)",
                "top_products": top_products,
                "inventory_alerts": inventory_alerts,
            }

        else:
            # Orders
            url_orders = f"https://{SHOPIFY_STORE_URL}/admin/api/2024-07/orders.json?limit={limit}&status=any"
            headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
            orders = requests.get(url_orders, headers=headers, timeout=10).json().get("orders", [])
            total_sales = sum(float(o.get("total_price", 0)) for o in orders)

            # Products
            url_products = f"https://{SHOPIFY_STORE_URL}/admin/api/2024-07/products.json?limit={limit}"
            products = requests.get(url_products, headers=headers, timeout=10).json().get("products", [])
            top_products = [p["title"] for p in products]

            inventory_alerts = []
            for p in products:
                for v in p.get("variants", []):
                    qty = v.get("inventory_quantity")
                    if qty is not None and qty < 10:
                        inventory_alerts.append(
                            f"{p['title']} (variant {v['title']}) low: {qty} left"
                        )

            return {
                "mode": "private",
                "store": SHOPIFY_STORE_URL,
                "total_sales": total_sales,
                "top_products": top_products,
                "inventory_alerts": inventory_alerts,
            }

    except Exception as e:
        return {"error": f"Shopify API error: {str(e)}"}


if __name__ == "__main__":
    summary = research_agent("Generative AI in healthcare")
    print("\n=== Research Summary ===")
    print(summary)

    business_data = ecommerce_agent()
    print("\n=== Business Data ===")
    print(business_data)
    save_note("GenAI Healthcare Report", summary, business_data)
