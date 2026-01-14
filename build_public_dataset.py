"""Build the public format_training_dataset artifacts.

Outputs:
- format_training_dataset/train_pairs.csv
- format_training_dataset/test_pairs.csv
- format_training_dataset/video_metadata.csv
- format_training_dataset/videos/README.md
"""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from pathlib import Path

INPUT_JSONL = Path("format_training_20251212.jsonl")
OUTPUT_DIR = Path("format_training_dataset")
TRAIN_TARGET = 1400
TEST_TARGET = 300
SEED = 42
TRAIN_RATIO = 0.8


def load_formats(path: Path) -> list[dict]:
    formats: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            formats.append(json.loads(line))
    return formats


def normalize_videos(formats: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for entry in formats:
        for video in entry.get("videos", []):
            rows.append(
                {
                    "content_id": video.get("content_id"),
                    "format_id": entry.get("format_id"),
                    "format_name": entry.get("format_name"),
                    "hypothesis": entry.get("hypothesis"),
                    "platform": video.get("platform"),
                    "title": video.get("title"),
                    "description": video.get("description"),
                    "duration": video.get("duration"),
                    "created_at": video.get("created_at"),
                    "views_count": video.get("views_count"),
                    "likes_count": video.get("likes_count"),
                    "comments_count": video.get("comments_count"),
                    "shares_count": video.get("shares_count"),
                    "save_count": video.get("save_count"),
                    "views_to_follower_ratio": video.get("views_to_follower_ratio"),
                    "is_10x_content": video.get("is_10x_content"),
                    "creator_id": video.get("creator_id"),
                    "creator_name": video.get("creator_name"),
                    "creator_followers": video.get("creator_followers"),
                    "video_url": video.get("video_url"),
                    "media_url": video.get("media_url"),
                    "thumbnail_url": video.get("thumbnail_url"),
                    "view_tier": video.get("view_tier"),
                    "search_strategy": video.get("search_strategy"),
                    "human_verified_status": video.get("human_verified_status"),
                }
            )
    return rows


def split_format_ids(format_ids: list[str]) -> tuple[set[str], set[str]]:
    unique_ids = sorted(set(format_ids))
    rng = random.Random(SEED)
    rng.shuffle(unique_ids)
    split_index = int(len(unique_ids) * TRAIN_RATIO)
    train_ids = set(unique_ids[:split_index])
    test_ids = set(unique_ids[split_index:])
    return train_ids, test_ids


def build_pairs(videos_by_format: dict[str, list[dict]]) -> list[dict]:
    pairs: list[dict] = []
    for format_id, videos in videos_by_format.items():
        valid_videos = [v for v in videos if v.get("views_count") is not None]
        if len(valid_videos) < 2:
            continue
        for i in range(len(valid_videos)):
            for j in range(i + 1, len(valid_videos)):
                left = valid_videos[i]
                right = valid_videos[j]
                pairs.append(
                    {
                        "format_id": format_id,
                        "left_content_id": left["content_id"],
                        "right_content_id": right["content_id"],
                        "left_views": left["views_count"],
                        "right_views": right["views_count"],
                        "label": 1 if left["views_count"] >= right["views_count"] else 0,
                    }
                )
    return pairs


def sample_pairs(pairs: list[dict], target: int) -> list[dict]:
    if len(pairs) <= target:
        return pairs
    rng = random.Random(SEED)
    return rng.sample(pairs, target)


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    formats = load_formats(INPUT_JSONL)
    video_rows = normalize_videos(formats)
    video_rows = [
        row
        for row in video_rows
        if row.get("human_verified_status") == "correct"
    ]

    format_ids = [row["format_id"] for row in video_rows]
    train_ids, test_ids = split_format_ids(format_ids)

    videos_by_format: dict[str, list[dict]] = defaultdict(list)
    for row in video_rows:
        videos_by_format[row["format_id"]].append(row)

    train_formats = {fid: videos_by_format[fid] for fid in train_ids}
    test_formats = {fid: videos_by_format[fid] for fid in test_ids}

    train_pairs = build_pairs(train_formats)
    test_pairs = build_pairs(test_formats)

    train_pairs = sample_pairs(train_pairs, TRAIN_TARGET)
    test_pairs = sample_pairs(test_pairs, TEST_TARGET)

    pair_id = 1
    for pair in train_pairs:
        pair["pair_id"] = f"train_{pair_id}"
        pair_id += 1

    pair_id = 1
    for pair in test_pairs:
        pair.pop("label", None)
        pair["pair_id"] = f"test_{pair_id}"
        pair_id += 1

    train_pairs_fields = [
        "pair_id",
        "format_id",
        "left_content_id",
        "right_content_id",
        "left_views",
        "right_views",
        "label",
    ]
    test_pairs_fields = [
        "pair_id",
        "format_id",
        "left_content_id",
        "right_content_id",
        "left_views",
        "right_views",
    ]

    metadata_fields = [
        "content_id",
        "format_id",
        "format_name",
        "hypothesis",
        "platform",
        "title",
        "description",
        "duration",
        "created_at",
        "views_count",
        "likes_count",
        "comments_count",
        "shares_count",
        "save_count",
        "views_to_follower_ratio",
        "is_10x_content",
        "creator_id",
        "creator_name",
        "creator_followers",
        "video_url",
        "media_url",
        "thumbnail_url",
        "view_tier",
        "search_strategy",
        "human_verified_status",
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT_DIR / "train_pairs.csv", train_pairs, train_pairs_fields)
    write_csv(OUTPUT_DIR / "test_pairs.csv", test_pairs, test_pairs_fields)
    write_csv(OUTPUT_DIR / "video_metadata.csv", video_rows, metadata_fields)

    videos_dir = OUTPUT_DIR / "videos"
    videos_dir.mkdir(exist_ok=True)
    (videos_dir / "README.md").write_text(
        """# Video access

Videos are provided via the `video_url` (platform link) and `media_url` (direct file) columns in `video_metadata.csv`.
Download or stream using those URLs as needed.
""",
        encoding="utf-8",
    )

    print(f"Train pairs: {len(train_pairs)}")
    print(f"Test pairs: {len(test_pairs)}")
    print(f"Metadata rows: {len(video_rows)}")


if __name__ == "__main__":
    main()
