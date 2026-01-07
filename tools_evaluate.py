# TODO: Create game_web_search tool
# Please use Tavily client to search the web
# Tool Docstring:
#    Semantic search: Finds most results in the vector DB
#    args:
#    - question: a question about game industry. 
query = "in what year was need for speed first sold and by whom?"

##Game web Search - External search helper (graceful fallback)

# def game_web_search(query: str, max_results: int = 5) -> list[dict]:
#     """
#     Lightweight web search helper for game-related queries.
#     Tries to fetch simple web results. Falls back gracefully if no internet.

#     Args:
#         query: Search query (e.g., game name + platform + release year).
#         max_results: Max items to return.

#     Returns:
#         A list of dicts: { "title": str, "url": str, "snippet": str }.
#         If web access is unavailable, returns an empty list and a note in 'snippet'.

    import os

# TODO: Create game_web_search tool
# Please use Tavily client to search the web
# Tool Docstring:
#    Semantic search: Finds most results in the vector DB
#    args:
#    - question: a question about game industry. 
query = "in what year was need for speed first sold and by whom?"

##Game web Search - External search helper (graceful fallback)

def game_web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Lightweight web search helper for game-related queries.
    Uses Tavily for web search.

    Args:
        query: Search query (e.g., game name + platform + release year).
        max_results: Max items to return.

    Returns:
        A list of dicts: { "title": str, "url": str, "snippet": str, "developer": str, "publisher": str, "release_date": str, "platforms": str }.
    """
    from tavily import TavilyClient

    try:
        client = TavilyClient(api_key=tavily_key)
        response = client.search(query, max_results=max_results)
        results = []
        for r in response['results']:
            results.append({
                "title": r['title'],
                "url": r['url'],
                "snippet": r['content'],
                "developer": "",
                "publisher": "",
                "release_date": "",
                "platforms": ""
            })
        return results
    except Exception as e:
        return [{
            "title": "Web search error",
            "url": "",
            "snippet": f"Exception during web search: {e}",
            "developer": "",
            "publisher": "",
            "release_date": "",
            "platforms": ""
        }]

# Eval retrieval tool
def evaluate_retrieval(
    question: str,
    retrieved_docs: List[Dict[str, Any]],
    max_docs: int = 8,
) -> EvaluationReport:
    """
    Tool: evaluate_retrieval
    ------------------------
    Based on the user's question and on the list of retrieved documents,
    it will analyze the usability of the documents to respond to that question.

    Args:
        - question: original question from user
        - retrieved_docs: retrieved documents most similar to the user query in the Vector Database

    Returns:
        EvaluationReport:
            - useful: whether the documents are useful to answer the question
            - description: description about the evaluation result
    """
    # Basic validation
    if not isinstance(question, str) or not question.strip():
        return EvaluationReport(useful=False, description="Invalid question.")
    if not retrieved_docs:
        return EvaluationReport(useful=False, description="No documents retrieved to evaluate.")

    # Compact, LLM-friendly view of docs
    lines: List[str] = []
    for i, d in enumerate(retrieved_docs[:max_docs], start=1):
        name = str(d.get("Name", "Unknown"))
        plat = str(d.get("Platform", ""))
        year = str(d.get("YearOfRelease", ""))
        desc = str(d.get("Description", ""))[:500]
        score = d.get("score")
        doc_id = d.get("id")
        lines.append(
            f"Doc {i}: Name={name}; Platform={plat}; Year={year}; Score={score}; Id={doc_id}; Description={desc}"
        )
    docs_block = "\n".join(lines)

    # LLM judge prompt
    prompt = f"""
You are an expert evaluator.
Your task is to evaluate if the provided documents are enough to respond to the query.

Query:
\"\"\"{question}\"\"\"

Documents:
{docs_block}

Instructions:
- Determine if the documents, as a set, are sufficient and relevant to answer the query.
- Consider coverage of key facts the query implies (e.g., developer, release date, platform), when applicable.
- If not sufficient, explain what's missing or ambiguous.
- Give a detailed explanation, so it's possible to take an action to accept it or not.

Respond ONLY in strict JSON with the following keys:
- "useful": true or false
- "description": a concise but informative explanation
"""

    # Call the model
    try:
        response = _client.chat.completions.create()(
            model=_MODEL_NAME,
            input=prompt,
            response_format={"type": "json_object"},
        )
        raw_text = response.output_text.strip()
    except Exception as e:
        return EvaluationReport(
            useful=False,
            description=f"LLM evaluation failed: {e}"
        )

    # Parse JSON safely
    try:
        parsed = json.loads(raw_text)
        useful = bool(parsed.get("useful"))
        description = str(parsed.get("description", "")).strip() or "No description provided."
        return EvaluationReport(useful=useful, description=description)
    except Exception:
        return EvaluationReport(
            useful=False,
            description=f"LLM response could not be parsed as JSON: {raw_text}"
        )


# Tool Docstring:
#    Semantic search: Finds most results in the vector DB
#    args:
#    - query: a question about game industry. 
#
#    You'll receive results as list. Each element contains:
#    - Platform: like Game Boy, Playstation 5, Xbox 360...)
#    - Name: Name of the Game
#    - YearOfRelease: Year when that game was released for that platform
#    - Description: Additional details about the game

  
  ## beautiful soup implementation.

  
  
    # try:
    #     import requests
    #     # from bs4 import BeautifulSoup  # requires 'beautifulsoup4' installed
    # except Exception:
    #     # Fallback (no web libs)
    #     return [{
    #         "title": "Web search unavailable",
    #         "url": "",
    #         "snippet": "Requests/BeautifulSoup not available in this environment."
    #     }]

#     try:
#         # Very simple HTML search using DuckDuckGo (no API key)
#         resp = requests.get("https://duckduckgo.com/html/", params={"q": query}, timeout=8)
#         if resp.status_code != 200:
#             return [{
#                 "title": "Web search failed",
#                 "url": "",
#                 "snippet": f"HTTP {resp.status_code} while searching for '{query}'."
#             }]
#         soup = BeautifulSoup(resp.text, "html.parser")
#         results = []
#         for a in soup.select(".result__a")[:max_results]:
#             title = a.get_text(strip=True)
#             url = a.get("href", "")
#             snippet_tag = a.find_parent("div", class_="result").select_one(".result__snippet")
#             snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
#             results.append({"title": title, "url": url, "snippet": snippet})
#         if not results:
#             results.append({"title": "No results parsed", "url": "", "snippet": "Parsing returned no items."})
#         return results
#     except Exception as e:
#         return [{
#             "title": "Web search error",
#             "url": "",
#             "snippet": f"Exception during web search: {e}"
#         }]





# # Tool Docstring:
# #    Semantic search: Finds most results in the vector DB
# #    args:
# #    - query: a question about game industry. 
# #
# #    You'll receive results as list. Each element contains:
# #    - Platform: like Game Boy, Playstation 5, Xbox 360...)
# #    - Name: Name of the Game
# #    - YearOfRelease: Year when that game was released for that platform
# #    - Description: Additional details about the game