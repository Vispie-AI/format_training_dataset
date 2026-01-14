"""Split the format training JSONL into train/test splits by format_id.

Usage:
    python split_dataset.py \
        --input format_training_20251212.jsonl \
        --train-output format_training_20251212.train.jsonl \
        --test-output format_training_20251212.test.jsonl \
        --seed 42 \
        --train-ratio 0.8
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input JSONL file where each line is a format-level record.",
    )
    parser.add_argument(
        "--train-output",
        type=Path,
        required=True,
        help="Output JSONL file for training split.",
    )
    parser.add_argument(
        "--test-output",
        type=Path,
        required=True,
        help="Output JSONL file for testing split.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used to shuffle format_ids.",
    )
    parser.add_argument(
        "--train-ratio",
        type=float,
        default=0.8,
        help="Fraction of format_ids assigned to the training split.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    records: list[str] = []
    with args.input.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(line)

    if not records:
        raise SystemExit("Input file is empty.")

    format_ids = [json.loads(line)["format_id"] for line in records]
    unique_ids = sorted(set(format_ids))
    rng = random.Random(args.seed)
    rng.shuffle(unique_ids)

    split_index = int(len(unique_ids) * args.train_ratio)
    train_ids = set(unique_ids[:split_index])
    test_ids = set(unique_ids[split_index:])

    train_lines: list[str] = []
    test_lines: list[str] = []
    for line in records:
        format_id = json.loads(line)["format_id"]
        if format_id in train_ids:
            train_lines.append(line)
        else:
            test_lines.append(line)

    args.train_output.write_text("\n".join(train_lines) + "\n", encoding="utf-8")
    args.test_output.write_text("\n".join(test_lines) + "\n", encoding="utf-8")

    print(f"Total formats: {len(unique_ids)}")
    print(f"Train formats: {len(train_ids)}")
    print(f"Test formats: {len(test_ids)}")
    print(f"Train lines: {len(train_lines)}")
    print(f"Test lines: {len(test_lines)}")


if __name__ == "__main__":
    main()
