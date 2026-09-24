---
name: wiki-market-research
description: Analyze Wikipedia pageviews to help B2C product founders validate market interest across topics and languages. Generates data-driven charts and structured JSON reports.
---

# Wikipedia Market Research Skill

Use this skill when users ask to analyze, compare, or validate market demand/interest for product topics, courses, or features across different language regions using Wikipedia traffic data.

## Workflow Execution Steps

When a user makes an analytical query, follow these steps strictly:

### Step 1: Disambiguate Topics & Map Languages

Translate the user's topic into exact target Wikipedia article titles for each requested language using Wikidata mapping.

`python wiki-market-research/scripts/search_topics.py --query "Astronomy" --languages uk,pl,en`

_Output: JSON mapping query terms to exact Wikipedia article titles in each language._

### Step 2: Fetch Traffic & Compute Metrics

Fetch pageviews data for the resolved articles over the target timeframe (default: 30 days).

`python wiki-market-research/scripts/fetch_analytics.py --articles "uk:Астрономія,pl:Astronomia" --days 30 --output wiki-market-research/analytics.json`

_This script automatically calculates:_

- _Total views & Daily Average views._
- _Max & Min daily view spikes._
- _Saves dataset to `wiki-market-research/analytics.json`._

### Step 3: Generate Visual Charts

Generate trend and comparison charts using matplotlib and pandas.

`python wiki-market-research/scripts/generate_charts.py --input wiki-market-research/analytics.json --output-dir wiki-market-research/charts`

### Step 4: Interpret Results

Analyze the generated data and provide actionable business insights:

- **High volume + Stable trend**: Strong established market demand.
- **Low volume**: Niche interest or potential naming mismatch in the target region.

## Guidelines for Low-Cost Models

- **Do NOT calculate math manually.** Always rely on `fetch_analytics.py` for statistics and averages.
- **Keep responses structured.** Provide a direct recommendation first, followed by key metrics and charts.
  а
