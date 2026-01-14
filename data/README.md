# Format Training Dataset (Public Export)

## Files

- `train_pairs.csv`: paired video comparisons with ground-truth labels.
- `test_pairs.csv`: paired video comparisons **without** labels.
- `video_metadata.csv`: per-video metadata (format, duration, views, URLs, etc.).
- `videos/README.md`: video access instructions.

## Pair format

`train_pairs.csv` columns:
- `pair_id`
- `format_id`
- `left_content_id`
- `right_content_id`
- `left_views`
- `right_views`
- `label` (1 if `left_views >= right_views`, else 0)

`test_pairs.csv` columns:
- `pair_id`
- `format_id`
- `left_content_id`
- `right_content_id`
- `left_views`
- `right_views`

## Video access

Use `video_metadata.csv` to resolve each `content_id` to `video_url` (platform link) or `media_url` (direct file). See `videos/README.md` for details.
