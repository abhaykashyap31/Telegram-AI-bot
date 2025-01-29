import requests

def search_web(query):
    # Example: Replace with your preferred web search API
    url = f"https://api.searchengine.com/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        summary = "\n".join([f"{result['title']}: {result['link']}" for result in results[:3]])
        return f"Search Results:\n{summary}"
    else:
        return "Failed to fetch search results."
