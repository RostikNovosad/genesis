#!/usr/bin/env python3
"""
Script to generate visual charts from Wikipedia analytics JSON data using matplotlib and pandas.
"""

import argparse
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def load_data(json_path: str) -> dict:
    """Load JSON data from file."""
    path = Path(json_path)
    if not path.exists():
        sys.stderr.write(f"Error: File {json_path} not found.\n")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def plot_analytics(data: dict, output_dir: str = "."):
    """Generate line chart for daily trends and bar chart for average views."""
    articles = data.get("articles_analytics", {})
    if not articles:
        print("No article data found in JSON.")
        return

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Графік тренду щоденних переглядів (Daily Views Trend)
    plt.figure(figsize=(12, 6))

    for key, info in articles.items():
        daily = info.get("daily_views", [])
        if not daily:
            continue
        df = pd.DataFrame(daily)
        df["date"] = pd.to_datetime(df["date"])
        plt.plot(
            df["date"],
            df["views"],
            label=f"{info['lang'].upper()}: {info['title']}",
            linewidth=2,
            marker="o" if len(df) < 35 else None,
            markersize=3,
        )

    plt.title("Daily Wikipedia Pageviews Comparison (30 Days)", fontsize=14, pad=15)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Pageviews", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=10)
    plt.tight_layout()

    trend_chart_path = out_path / "pageviews_trend.png"
    plt.savefig(trend_chart_path, dpi=300)
    plt.close()
    print(f"✓ Trend chart saved to: {trend_chart_path}")

    # 2. Гістограма середньодобового трафіку (Average Daily Views)
    labels = []
    averages = []
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for i, (key, info) in enumerate(articles.items()):
        labels.append(f"{info['lang'].upper()}\n{info['title']}")
        averages.append(info.get("aggregates", {}).get("daily_average", 0))

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, averages, color=colors[: len(labels)], width=0.5)

    plt.title("Average Daily Pageviews by Language/Article", fontsize=14, pad=15)
    plt.ylabel("Avg Daily Views", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + (max(averages) * 0.015),
            f"{yval:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    avg_chart_path = out_path / "average_views.png"
    plt.savefig(avg_chart_path, dpi=300)
    plt.close()
    print(f"✓ Average views chart saved to: {avg_chart_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate analytics charts from Wikipedia JSON data.")
    parser.add_argument("--input", required=True, help="Path to analytics JSON file")
    parser.add_argument("--output-dir", default="./charts", help="Directory to save output PNGs")

    args = parser.parse_args()
    raw_data = load_data(args.input)
    plot_analytics(raw_data, args.output_dir)


if __name__ == "__main__":
    main()