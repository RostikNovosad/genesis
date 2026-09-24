---
name: wiki-market-research
description: Analyze Wikipedia pageviews to help founders, product managers, and researchers validate market interest across topics, industries, and languages. Generates data-driven charts and structured analytical insights.
---

# Wikipedia Market Research Skill

Use this skill when users ask to analyze, compare, or validate market demand, course subjects, product features, or cultural trends across different language regions using Wikipedia traffic data.

## Workflow Execution Steps

When a user provides an analytical or market research query, follow these steps strictly:

### Step 1: Disambiguate Topics & Map Languages

Translate the user's raw topic query into exact target Wikipedia article titles for each requested language using Wikidata mapping.

When searching for broad domain concepts (e.g., Astronomy, Finance), search using the primary English topic name first to accurately retrieve the high-level Wikidata QID, then map to target languages.

`python wiki-market-research/scripts/search_topics.py --query "<User Topic>" --languages uk,pl,cs,en`

_Output: JSON mapping query terms to exact Wikipedia article titles in each target language via Wikidata QID._

### Step 2: Fetch Traffic & Compute Metrics

Fetch pageview data for the resolved articles over the target timeframe (e.g., `--days 30`).

`python wiki-market-research/scripts/fetch_analytics.py --articles "<lang1:Title1,lang2:Title2>" --days 30 --output wiki-market-research/analytics.json`

This script automatically calculates metrics and saves the output JSON. Always read the generated `analytics.json` file to extract exact numbers (total_views, daily_average, max/min spikes) for your report.

### Step 3: Generate Visual Charts

Generate trend lines and comparative bar charts using matplotlib and pandas.

`python wiki-market-research/scripts/generate_charts.py --input wiki-market-research/analytics.json --output-dir wiki-market-research/charts`

### Step 4: Interpret Results & Formulate Business Takeaways

Analyze the generated data and output structured, action-oriented recommendations:

1. **Demand Volume & Scalability**: High total/average views signal established organic interest.
2. **Trend Stability vs Spikes**: Smooth lines indicate steady interest; sudden isolated spikes suggest hype or news events.
3. **Regional Prioritization**: Rank target languages/regions by organic volume to guide product launch or localization decisions.

## Guidelines for AI Execution

- **Do NOT calculate math manually.** Always rely on `fetch_analytics.py` for statistics and averages.
- **Maintain neutrality.** Mention limitations (e.g., Wikipedia traffic represents search interest/curiosity, not necessarily willingness to pay).
- **Structure outputs cleanly.** Lead with a clear direct verdict/recommendation, followed by key metrics and supporting chart references.
