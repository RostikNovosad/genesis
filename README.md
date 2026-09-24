# Wiki Market Research: Аналіз попиту на тему «Інтервальне голодування»

Проект призначений для аналізу органічного інтересу та порівняння попиту на тему **Intermittent Fasting (Інтервальне голодування)** у трьох мовних сегментах Вікіпедії (**EN**, **UK**, **PL**) за 30 днів.

Датасет формується автоматично через **Wikimedia REST API** та **MediaWiki Action API**.

---

## 🏗️ Структура проекту

```text
wiki-market-research/
├── scripts/
│   ├── search_topics.py     # Пошук та міжмовний мапінг тем через Wikidata
│   ├── fetch_analytics.py    # Збір даних з Wikimedia API та збереження у JSON
│   └── generate_charts.py    # Побудова лінійних графіків і гістограм (Pandas/Matplotlib)
├── .gitignore                # Конфігурація ігнорування артефактів Git
├── pyproject.toml            # Конфігурація проекту та залежностей Python
├── analytics.json            # Згенерований датасет (в .gitignore)
├── charts/                   # Згенеровані графіки (в .gitignore)
│   ├── pageviews_trend.png
│   └── average_views.png
└── README.md                 # Підсумковий звіт та документація
```

---

## 📚 Джерела та документація API

- [Wikimedia REST API (Pageviews Metrics)](https://wikimedia.org/api/rest_v1/)
- [MediaWiki Action API (Redirects & Search)](https://www.mediawiki.org/wiki/API:Main_page)
- [Wikimedia User-Agent Policy](https://meta.wikimedia.org/wiki/User-Agent_policy)

```

```
