#!/usr/bin/env python3
"""
Script to fetch daily pageview metrics from Wikimedia REST API for specified articles and time window.
Handles Wikipedia redirects and URL encoding automatically.
"""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List

USER_AGENT = "WikiMarketAnalystBot/1.0 (https://github.com/example/wiki-market-analyst; )"


def fetch_json(url: str) -> dict:
    """Helper function to make HTTP GET requests with custom User-Agent."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            sys.stderr.write(f"HTTP Error {e.code} for {url}\n")
    except Exception as e:
        sys.stderr.write(f"HTTP Request failed for {url}: {e}\n")
    return {}


def parse_articles_param(articles_str: str) -> List[Dict[str, str]]:
    """Parse comma-separated 'lang:Title' strings into a list of dictionaries."""
    result = []
    items = articles_str.split(",")
    for item in items:
        if ":" in item:
            lang, title = item.split(":", 1)
            result.append({"lang": lang.strip().lower(), "title": title.strip()})
    return result


def resolve_redirect_title(lang: str, article_title: str) -> str:
    """Check if article exists/redirects. Fallback to exact search if missing."""
    encoded_title = urllib.parse.quote(article_title)
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={encoded_title}&redirects=1&format=json&utf8=1"

    data = fetch_json(url)
    pages = data.get("query", {}).get("pages", {})

    for page_id, page_info in pages.items():
        if page_id != "-1":
            redirects = data.get("query", {}).get("redirects", [])
            if redirects:
                return redirects[0].get("to", article_title)
            return page_info.get("title", article_title)

    # Якщо сторінки немає, шукаємо ТОЧНУ фразу в лапках
    exact_query = urllib.parse.quote(f'"{article_title}"')
    search_url = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={exact_query}&format=json&utf8=1"
    search_data = fetch_json(search_url)
    search_results = search_data.get("query", {}).get("search", [])

    if search_results:
        matched_title = search_results[0].get("title")
        sys.stderr.write(f"[{lang}] '{article_title}' direct page not found. Matched search: '{matched_title}'\n")
        return matched_title

    return article_title
def fetch_daily_pageviews(lang: str, article_title: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Fetch daily pageviews for a single article using Wikimedia REST API.
    Resolves redirects and replaces spaces with underscores.
    """
    canonical_title = resolve_redirect_title(lang, article_title)
    formatted_title = canonical_title.replace(" ", "_")
    encoded_title = urllib.parse.quote(formatted_title, safe="")

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"{lang}.wikipedia/all-access/user/{encoded_title}/daily/{start_date}/{end_date}"
    )

    data = fetch_json(url)
    items = data.get("items", [])

    daily_metrics = []
    for item in items:
        timestamp_str = item.get("timestamp", "")
        views = item.get("views", 0)
        if len(timestamp_str) >= 8:
            formatted_date = f"{timestamp_str[:4]}-{timestamp_str[4:6]}-{timestamp_str[6:8]}"
            daily_metrics.append({"date": formatted_date, "views": views})

    return daily_metrics


def aggregate_article_stats(daily_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate aggregate statistics for a given list of daily metrics."""
    if not daily_metrics:
        return {"total_views": 0, "daily_average": 0.0, "max_daily_views": 0, "min_daily_views": 0}

    views = [m["views"] for m in daily_metrics]
    total_views = sum(views)
    return {
        "total_views": total_views,
        "daily_average": round(total_views / len(views), 2),
        "max_daily_views": max(views),
        "min_daily_views": min(views),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch Wikimedia pageview analytics for specified articles.")
    parser.add_argument(
        "--articles",
        required=True,
        help="Comma-separated articles in 'lang:Title' format (e.g. 'uk:Інтервальне голодування,pl:Post przerywany')",
    )
    parser.add_argument("--days", type=int, default=30, help="Number of days to look back (default: 30)")

    args = parser.parse_args()

    end_dt = datetime.date.today() - datetime.timedelta(days=1)
    start_dt = end_dt - datetime.timedelta(days=args.days - 1)

    start_date_str = start_dt.strftime("%Y%m%d")
    end_date_str = end_dt.strftime("%Y%m%d")

    articles_list = parse_articles_param(args.articles)

    results = {
        "time_window": {
            "start_date": start_dt.strftime("%Y-%m-%d"),
            "end_date": end_dt.strftime("%Y-%m-%d"),
            "days_analyzed": args.days,
        },
        "articles_analytics": {},
    }

    for item in articles_list:
        lang = item["lang"]
        title = item["title"]

        daily_data = fetch_daily_pageviews(lang, title, start_date_str, end_date_str)
        aggregates = aggregate_article_stats(daily_data)

        results["articles_analytics"][f"{lang}:{title}"] = {
            "lang": lang,
            "title": title,
            "aggregates": aggregates,
            "daily_views": daily_data,
        }

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()