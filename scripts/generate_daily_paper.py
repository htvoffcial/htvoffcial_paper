#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import random
from pathlib import Path
from typing import Iterable

TEMPLATES: list[tuple[int, str]] = [
    (2, "本研究では{0}と{1}の関連性を再検討した。"),
    (2, "先行研究に基づき、{0}は{1}として再定義される。"),
    (2, "実験の結果、{0}は{1}より有意に増加した。"),
    (2, "この枠組みは{0}を通じて{1}を説明する。"),
    (2, "理論的には{0}が{1}の前提条件となる。"),
    (2, "観測データは{0}と{1}の同時変動を示した。"),
    (2, "補助解析では{0}が{1}に先行する傾向を確認した。"),
    (2, "以上より、{0}は{1}の頑健な指標である。"),
    (3, "本稿の仮説は、{0}が{1}を介して{2}に影響するというものである。"),
    (3, "方法論として、{0}・{1}・{2}の三層モデルを採用した。"),
    (3, "結果は{0}、{1}、{2}の順に収束した。"),
    (3, "追加検証により、{0}と{1}の相互作用が{2}を増幅した。"),
    (3, "解析過程で{0}が{1}へ転移し、最終的に{2}へ統合された。"),
    (3, "比較群では{0}、対照群では{1}、追跡群では{2}が卓越した。"),
    (3, "議論では{0}を起点に{1}を経由して{2}へ接続した。"),
    (3, "この知見は{0}・{1}・{2}の整合的理解を要求する。"),
    (4, "初期条件{0}のもとで{1}を導入すると、{2}が抑制され{3}が顕在化した。"),
    (4, "まず{0}を固定し、次に{1}を変化させることで{2}から{3}への遷移を観測した。"),
    (4, "統合モデルでは{0}と{1}を独立変数、{2}と{3}を評価指標とした。"),
    (4, "頑健性評価の結果、{0}に対する{1}の効果は{2}および{3}でも再現された。"),
    (4, "理論節では{0}を仮定し、{1}・{2}・{3}を段階的に導出した。"),
    (4, "観測系列{0}を分解すると、{1}、{2}、{3}の三成分が得られた。"),
    (4, "この設計により{0}から{1}、さらに{2}を経て{3}へ至る因果連鎖を示した。"),
    (4, "最終的に{0}と{1}の同時最適化が{2}と{3}の安定化に寄与した。"),
]

SENTENCE_ENDINGS = ("。", "!", "?", ".")
SECTION_HEADER = "## Daily Nonsense Paper"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily nonsense paper text from CSV words and append to README.md"
    )
    parser.add_argument(
        "--csv-path",
        default="data/words.csv",
        type=Path,
        help="Path to CSV file containing words",
    )
    parser.add_argument(
        "--readme-path",
        default="README.md",
        type=Path,
        help="Path to README file",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Date in YYYY-MM-DD format (default: UTC today)",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print generated paragraph only; do not update README",
    )
    return parser.parse_args()


def load_words(csv_path: Path) -> list[str]:
    words: list[str] = []
    with csv_path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.reader(fp)
        for row in reader:
            for cell in row:
                token = cell.strip()
                if token:
                    words.append(token)
    if not words:
        raise ValueError(f"No words found in {csv_path}")
    return words


def pick_daily_words(words: list[str], day_key: str, count: int = 10) -> list[str]:
    rng = random.Random(day_key)
    if len(words) >= count:
        return rng.sample(words, count)
    return [rng.choice(words) for _ in range(count)]


def chunk_templates(rng: random.Random, total_words: int) -> Iterable[tuple[int, str]]:
    remaining = total_words
    min_slots = min(size for size, _ in TEMPLATES)

    while remaining > 0:
        choices = [
            tpl
            for tpl in TEMPLATES
            if tpl[0] <= remaining and (remaining - tpl[0] == 0 or remaining - tpl[0] >= min_slots)
        ]
        if not choices:
            choices = [tpl for tpl in TEMPLATES if tpl[0] <= remaining]
        chosen = rng.choice(choices)
        yield chosen
        remaining -= chosen[0]


def build_paragraph(words: list[str], day_key: str) -> str:
    rng = random.Random(f"templates:{day_key}")
    cursor = 0
    sentences: list[str] = []

    for slot_count, template in chunk_templates(rng, len(words)):
        args = words[cursor : cursor + slot_count]
        cursor += slot_count
        sentences.append(template.format(*args))

    return " ".join(sentences)


def ensure_section(readme_content: str) -> str:
    if SECTION_HEADER in readme_content:
        return readme_content
    if not readme_content.endswith("\n"):
        readme_content += "\n"
    return f"{readme_content}\n{SECTION_HEADER}\n"


def normalize_trailing_sentence(readme_content: str) -> str:
    stripped = readme_content.rstrip()
    if not stripped:
        return readme_content
    if stripped.endswith(SENTENCE_ENDINGS):
        return readme_content
    last_line = stripped.splitlines()[-1].strip()
    if not last_line:
        return readme_content
    if last_line.startswith((SECTION_HEADER, "#", "-", "*", ">", "`")):
        return readme_content

    return stripped + "。\n"


def append_daily_entry(readme_path: Path, day_key: str, paragraph: str) -> bool:
    original = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    if f"### {day_key}" in original:
        return False

    content = ensure_section(normalize_trailing_sentence(original))
    if not content.endswith("\n"):
        content += "\n"

    content += f"\n### {day_key}\n{paragraph}\n"

    readme_path.write_text(content, encoding="utf-8")
    return True


def resolve_date(day_arg: str | None) -> str:
    if day_arg is None:
        return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    try:
        parsed = dt.date.fromisoformat(day_arg)
    except ValueError as exc:
        raise ValueError("--date must be YYYY-MM-DD") from exc
    return parsed.isoformat()


def main() -> int:
    args = parse_args()
    day_key = resolve_date(args.date)

    words = load_words(args.csv_path)
    daily_words = pick_daily_words(words, day_key, 10)
    paragraph = build_paragraph(daily_words, day_key)

    if args.print_only:
        print(paragraph)
        return 0

    updated = append_daily_entry(args.readme_path, day_key, paragraph)
    if updated:
        print(f"Updated {args.readme_path} for {day_key}")
    else:
        print(f"Entry for {day_key} already exists in {args.readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
