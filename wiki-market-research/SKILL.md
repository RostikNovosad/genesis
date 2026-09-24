---
name: wiki-market-research
description: Analyze Wikipedia pageviews to help B2C product founders validate market interest across topics and languages. Generates data-driven charts and 1-page PDF reports.
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

Fetch pageviews data for the resolved articles over the target timeframe (default: 24 months).

`python wiki-market-research/scripts/fetch_analytics.py --articles "uk:Астрономія,pl:Astronomia" --months 24`

_This script automatically calculates:_

- _Total views & Average views._
- _CAGR / Growth %._
- _Volatility & Anomaly Spikes._
- _Confidence Score (0-100%)._
  _And saves generated comparison charts to `wiki-market-research/assets/charts/`._

### Step 3: Interpret Results

Analyze the JSON output from `fetch_analytics.py` and provide actionable business insights:

- **High growth + High confidence (>70%)**: Strong long-term market opportunity.
- **High growth + Low confidence (<40%)**: Viral news spike/hype; temporary trend, proceed with caution.
- **Negative growth**: Declining interest in the market.

### Step 4: Generate Report (If Requested)

If the user explicitly asks for a shareable report, executive summary, or a single-page PDF:

`python wiki-market-research/scripts/generate_pdf.py --input_data "path/to/analytics_result.json" --chart "path/to/chart.png" --summary "Agent key takeaway insights" --output "report.pdf"`

## Guidelines for Low-Cost Models

- **Do NOT calculate math manually.** Always rely on `fetch_analytics.py` for statistics, CAGR, and scores.
- **Keep responses structured.** Provide a direct recommendation first, followed by key metrics and risk limitations.
- Read `wiki-market-research/references/metrics_guide.md` if you need to explain how metrics like Confidence Score were derived.
