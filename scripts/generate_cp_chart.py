import re
from pathlib import Path
from html import escape

README = Path("README.md")
OUTPUT = Path("assets/cp-percentiles.svg")

text = README.read_text(encoding="utf-8")

platforms = [
    ("LeetCode", "LeetCode"),
    ("Codeforces", "Codeforces"),
    ("AtCoder", "AtCoder"),
    ("CodeChef", "CodeChef"),
]

data = []

for platform, pattern in platforms:
    match = re.search(
        rf"- {re.escape(pattern)}/.*?\(Top ([0-9]+(?:\.[0-9]+)?)%\)",
        text,
    )

    if not match:
        raise ValueError(f"Could not find percentile for {platform}")

    percentile = float(match.group(1))
    fill = 100 - percentile

    data.append((platform, percentile, fill))


WIDTH = 900
HEIGHT = 230

BAR_X = 150
BAR_WIDTH = 560
BAR_HEIGHT = 14

SVG = f"""<svg width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
xmlns="http://www.w3.org/2000/svg">

<style>
    .name {{
        font: 600 14px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        fill: #24292f;
    }}

    .pct {{
        font: 600 13px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        fill: #57606a;
    }}

    .track {{
        fill: #eaeef2;
    }}

    .fill {{
        fill: #2da44e;
    }}

    @media (prefers-color-scheme: dark) {{
        .name {{
            fill: #f0f6fc;
        }}

        .pct {{
            fill: #8b949e;
        }}

        .track {{
            fill: #30363d;
        }}

        .fill {{
            fill: #3fb950;
        }}
    }}
</style>
"""

for i, (platform, percentile, fill) in enumerate(data):
    y = 35 + i * 45

    fill_width = BAR_WIDTH * fill / 100

    SVG += f"""
    <text
        x="30"
        y="{y + 13}"
        class="name"
    >{escape(platform)}</text>

    <rect
        x="{BAR_X}"
        y="{y}"
        width="{BAR_WIDTH}"
        height="{BAR_HEIGHT}"
        rx="7"
        class="track"
    />

    <rect
        x="{BAR_X}"
        y="{y}"
        width="{fill_width:.2f}"
        height="{BAR_HEIGHT}"
        rx="7"
        class="fill"
    />

    <text
        x="{BAR_X + BAR_WIDTH + 20}"
        y="{y + 13}"
        class="pct"
    >Top {percentile:.2f}%</text>
    """

SVG += "</svg>\n"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(SVG, encoding="utf-8")

print("Generated", OUTPUT)