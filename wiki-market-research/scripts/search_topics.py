#!/usr/bin/env python3
"""
Script to search Wikipedia article titles and map them across multiple target languages using Wikidata.
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

USER_AGENT = "WikiMarketAnalystBot/1.0 (https://github.com/example/wiki-market-analyst; )"


def fetch_json(url: str) -> dict:
    """Helper function to make HTTP GET requests with custom User-Agent."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        sys.stderr.write(f"HTTP Request failed for {url}: {e}\n")
    return {}


def search_wikipedia(query: str, lang: str = "en") -> Optional[str]:
    """Search Wikipedia for a given query and return the best-matching article title."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json&utf8=1"

    data = fetch_json(url)
    search_results = data.get("query", {}).get("search", [])

    if search_results:
        return search_results[0]["title"]
    return None


def get_wikidata_id(article_title: str, lang: str = "en") -> Optional[str]:
    """Retrieve the Wikidata QID for a specific Wikipedia article title."""
    encoded_title = urllib.parse.quote(article_title)
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={encoded_title}&format=json&utf8=1"

    data = fetch_json(url)
    pages = data.get("query", {}).get("pages", {})

    for _, page in pages.items():
        pageprops = page.get("pageprops", {})
        if "wikibase_item" in pageprops:
            return pageprops["wikibase_item"]
    return None


def get_sitelinks_from_wikidata(qid: str, target_languages: List[str]) -> Dict[str, str]:
    """Retrieve translated Wikipedia article titles across target languages using Wikidata QID."""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=sitelinks&format=json&utf8=1"

    data = fetch_json(url)
    entities = data.get("entities", {}).get(qid, {})
    sitelinks = entities.get("sitelinks", {})

    mapped_titles = {}
    for lang in target_languages:
        wiki_key = f"{lang}wiki"
        if wiki_key in sitelinks:
            mapped_titles[lang] = sitelinks[wiki_key]["title"]

    return mapped_titles


def resolve_topic_mapping(query: str, target_languages: List[str], base_lang: Optional[str] = None) -> dict:
    """Main function to search, resolve QID, and map topic across all target languages."""

    # 1. Якщо base_lang не вказано явно, беремо першу мову зі списку target_languages
    # Це дозволяє шукати українською, якщо користувач передав --languages "uk,pl,en"
    primary_lang = base_lang if base_lang else target_languages[0]

    matched_title = search_wikipedia(query, primary_lang)

    # 2. Якщо мовою primary_lang нічого не знайдено, пробуємо пошук по всіх інших мовах зі списку
    if not matched_title:
        for lang in target_languages:
            if lang == primary_lang:
                continue
            matched_title = search_wikipedia(query, lang)
            if matched_title:
                primary_lang = lang
                break

    if not matched_title:
        return {
            "query": query,
            "status": "error",
            "message": f"No matching Wikipedia article found for '{query}'"
        }

    # 3. Отримуємо універсальний Wikidata QID
    qid = get_wikidata_id(matched_title, primary_lang)

    if not qid:
        return {
            "query": query,
            "primary_match": {"lang": primary_lang, "title": matched_title},
            "status": "partial",
            "message": "Found Wikipedia page but could not map to Wikidata item."
        }

    # 4. Отримуємо міжмовні посилання для всіх потрібних мов за цим QID
    sitelinks = get_sitelinks_from_wikidata(qid, target_languages)

    # Переконуємося, що первинна стаття збережена у результатах
    if primary_lang in target_languages and primary_lang not in sitelinks:
        sitelinks[primary_lang] = matched_title

    return {
        "query": query,
        "wikidata_qid": qid,
        "status": "success",
        "primary_match": {"lang": primary_lang, "title": matched_title},
        "mapped_articles": sitelinks,
        "formatted_articles_param": ",".join([f"{lang}:{title}" for lang, title in sitelinks.items()])
    }

def main():
    parser = argparse.ArgumentParser(description="Map search terms to Wikipedia article titles in target languages.")
    parser.add_argument("--query", required=True, help="Topic query (e.g., 'Intermittent fasting')")
    parser.add_argument("--languages", required=True, help="Comma-separated language codes (e.g., 'uk,pl,cs,en')")
    parser.add_argument("--base_lang", default="en", help="Primary language to perform initial search (default: 'en')")

    args = parser.parse_args()
    target_langs = [l.strip().lower() for l in args.languages.split(",")]

    mapping_result = resolve_topic_mapping(args.query, target_langs, args.base_lang)
    print(json.dumps(mapping_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()