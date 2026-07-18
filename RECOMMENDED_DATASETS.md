# 10 Kaggle Datasets for Learning to Handle LARGE Data

## Intro

A curated set of 10 Kaggle datasets for a Georgia Tech MS Analytics student entering year 2 who wants to
grow from "fits-in-RAM pandas" work to genuinely **large-data** engineering: memory management, sampling,
chunked reads, columnar formats (Parquet/Arrow), and out-of-core tools (Polars, DuckDB, PySpark).

**Selection criteria**

- **Actually large** — from tens of MB up to tens of GB; millions of rows or thousands of columns.
- **Educational for large-data technique**s — each dataset forces a specific skill (chunking, dtype reduction,
  Parquet conversion, multi-table joins at scale, sampling for EDA, out-of-core aggregation, image-metadata
  pipelines, nested-JSON parsing, recommender feature engineering).
- **Domain diversity** — geospatial, multi-table tabular, time series, text, image metadata, recommender,
  wide/sparse manufacturing, click logs, nested web analytics, wide financial.
- **Mix of competitions and open datasets**, all verified on Kaggle with usable CLI slugs.

The list is ordered **1 (most approachable) → 10 (most advanced)**, roughly tracking: single CSV → multi-table
joins → time series + weather → image metadata → wide tabular → wide+sparse → very many rows → recommender
at scale → nested JSON chunking → multi-GB wide financial.

> Slugs use the `c/<slug>` form for competitions (works with `kaggle competitions download -c <slug>`).
> Sizes are approximate (on-disk uncompressed CSV unless noted) and were verified via search in Jul 2026.

---

## 1. New York City Taxi Trip Duration

- **Kaggle slug**: `c/nyc-taxi-trip-duration`
- **Approx. size**: ~1.46M train rows (+625k test); ~200 MB CSV
- **Domain & data type**: Geospatial tabular — NYC TLC yellow-cab trips with pickup/dropoff lat-lon, timestamps,
  passenger count, vendor id.
- **Why it's on the list**: The canonical "first big-ish dataset." Big enough that naive `pd.read_csv` feels slow
  but small enough to fit in memory, so it's a safe sandbox for chunking, sampling, and dtype downcasting before
  the data gets truly huge.
- **Suggested learning focus**: Practice chunked CSV reads with `pandas.read_csv(..., chunksize=...)`; downcast
  floats/ints; compute haversine distance as a feature; then re-do the same EDA in Polars and compare speed/memory.
  Try a DuckDB SQL aggregation (`SELECT ... GROUP BY`) directly on the CSV.
- **Difficulty**: Easy

## 2. Elo Merchant Category Recommendation

- **Kaggle slug**: `c/elo-merchant-category-recommendation`
- **Approx. size**: ~3 GB total; `historical_transactions.csv` ~1 GB with ~20M rows; `new_merchant_transactions.csv`
  ~20 MB; plus `merchants.csv` and train/test.
- **Domain & data type**: Multi-table relational tabular — card → merchant transactions, with merchant metadata.
- **Why it's on the list**: Forces you to **join multiple large tables** and engineer per-card aggregate features
  (counts, nunique, time-since-last) at scale — a core analytics-MS skill that single-CSV datasets don't teach.
- **Suggested learning focus**: Build per-card aggregation features with Polars `group_by` / DuckDB window
  functions; convert the 1 GB transactions CSV to Parquet and measure the speedup on re-reads; practice
  memory-safe joins and column pruning (read only needed columns).
- **Difficulty**: Medium

## 3. ASHRAE Great Energy Predictor III

- **Kaggle slug**: `c/ashrae-energy-prediction`
- **Approx. size**: ~20.2M train rows (~2 GB) + ~41M test rows; ~62M hourly measurements across 1,448 buildings /
  16 sites; plus `building_metadata.csv` and `weather_[train/test].csv`.
- **Domain & data type**: Time series + weather + building metadata (multi-table).
- **Why it's on the list**: Classic time-series-at-scale problem. You must merge meter readings with building
  metadata and hourly weather, then lag/roll features without blowing memory — a realistic analytics pipeline.
- **Suggested learning focus**: Use Parquet partitioned by `building_id` (or by month) for fast columnar reads;
  compute rolling/lag features with Polars lazy frames or PySpark window functions; sample buildings for EDA,
  then scale up. Practice time-based (not random) train/val splits to avoid leakage.
- **Difficulty**: Medium

## 4. Jigsaw Toxic Comment Classification Challenge

- **Kaggle slug**: `c/jigsaw-toxic-comment-classification-challenge`
- **Approx. size**: ~159,571 train rows + ~153,164 test rows; ~131 MB uncompressed (~48 MB compressed).
- **Domain & data type**: Text — Wikipedia talk-page comments with 6 multi-label toxicity flags.
- **Why it's on the list**: Smaller in rows, but **text feature matrices explode** (huge vocabularies / TF-IDF
  / hashing), so it teaches memory-aware text vectorization — a different flavor of "large" driven by width
  rather than row count. Good domain diversity (NLP) before the heavier datasets.
- **Suggested learning focus**: Use `HashingVectorizer` (fixed-memory, no vocab store) vs `TfidfVectorizer`;
  stream text with chunked reads; compare sparse-matrix memory footprints; try `sklearn`'s `partial_fit`
  (SGDClassifier) for out-of-core text learning.
- **Difficulty**: Medium

## 5. RSNA Pneumonia Detection Challenge

- **Kaggle slug**: `c/rsna-pneumonia-detection-challenge`
- **Approx. size**: ~26,684 train + ~9,668 test DICOM images at 1024×1024; several GB on disk; plus
  `stage_2_train_labels.csv` and `stage_2_detailed_class_info.csv` metadata.
- **Domain & data type**: Image metadata + DICOM binary files — chest radiographs with bounding-box labels.
- **Why it's on the list**: Teaches the **many-files / binary-blob** large-data pattern that pure CSV datasets
  miss: streaming thousands of DICOMs, extracting pixel metadata, and building a metadata index without loading
  all images into memory.
- **Suggested learning focus**: Use `pydicom` to stream image metadata into a Parquet index; build a lazy
  `Dataset`/generator that yields decoded arrays on demand; practice sampling thumbnails for EDA; compare
  reading via file paths vs a Parquet-backed manifest. (Optional: object detection with a sampled subset.)
- **Difficulty**: Medium/Hard

## 6. Jane Street Market Prediction

- **Kaggle slug**: `c/jane-street-market-prediction`
- **Approx. size**: ~2.39M rows, 130 anonymized features + meta; `train.csv` ~5.8 GB.
- **Domain & data type**: Wide tabular financial — high-frequency market features, time-ordered by `ts_id`,
  500 days.
- **Why it's on the list**: A wide, medium-heavy dataset where **dtype reduction and Parquet conversion pay off
  massively** (float64 → float16 can cut memory ~4×). The classic "reduce_mem_usage" exercise.
- **Suggested learning focus**: Convert CSV to Parquet with optimal dtypes; benchmark Polars vs pandas read
  times; do feature selection on a time-based sample, then scale; practice weighted utility-based evaluation
  and time-grouped CV (no forward peeking).
- **Difficulty**: Hard

## 7. Bosch Production Line Performance

- **Kaggle slug**: `c/bosch-production-line-performance`
- **Approx. size**: ~14.3 GB total; ~1.18M train rows × **4,265 anonymized features** split across
  `train_numeric.csv`, `train_categorical.csv`, `train_date.csv` (each ~2.8 GB); extremely imbalanced target.
- **Domain & data type**: Wide + sparse manufacturing tabular (numerical / categorical / date-station features).
- **Why it's on the list**: One of the widest Kaggle datasets ever hosted. Forces **sparsity handling, column
  pruning, and feature selection at scale** — you cannot just load it all. Teaches the manufacturing
  (rare-failure) analytics use case.
- **Suggested learning focus**: Read per-file with chunking; drop near-constant / all-null columns first;
  store as sparse CSR or Parquet with dictionary encoding; use LightGBM on a sampled, feature-pruned subset;
  explore feature-name structure (`L#_S#_F#`) to engineer station-level aggregates.
- **Difficulty**: Hard

## 8. TalkingData AdTracking Fraud Detection

- **Kaggle slug**: `c/talkingdata-adtracking-fraud-detection`
- **Approx. size**: ~184.9M train rows; `train.csv` ~7 GB (a `train_sample.csv` ~4 MB is provided for EDA);
  test ~863 MB.
- **Domain & data type**: Massive-row click logs — ip, app, device, os, channel, click_time, is_attributed
  (highly imbalanced).
- **Why it's on the list**: Teaches **row-count scale**: ~185M rows won't fit in RAM on a laptop, so you must
  sample, chunk, or go out-of-core. Also a textbook imbalanced-classification problem.
- **Suggested learning focus**: Start with `train_sample.csv` for EDA, then scale with chunked reads +
  incremental aggregations (ip counts, hour-of-day); use Polars lazy / DuckDB to group-by 185M rows without
  loading all; practice negative-downsampling and frequency encoding; consider PySpark for the full pipeline.
- **Difficulty**: Hard

## 9. H&M Personalized Fashion Recommendations

- **Kaggle slug**: `c/h-and-m-personalized-fashion-recommendations`
- **Approx. size**: ~31.8M transaction rows + 1.37M customers + 105k articles; ~35 GB total (incl. ~105k
  product images).
- **Domain & data type**: Recommender — customer–article transactions, article/customer metadata, product
  images.
- **Why it's on the list**: A large **recommender / sequence** problem combining a big transactions table with
  image metadata — teaches candidate generation + ranking feature engineering at scale, plus handling an
  image-folder side dataset.
- **Suggested learning focus**: Build co-occurrence / last-purchased baselines with DuckDB on the 31.8M-row
  table; engineer per-customer recency/frequency features in Polars; sample negative items efficiently; manage
  the image folder with a Parquet manifest (cf. dataset #5); try a LightGBM ranker on a time-based split.
- **Difficulty**: Hard

## 10. Ubiquant Market Prediction

- **Kaggle slug**: `c/ubiquant-market-prediction`
- **Approx. size**: ~3.14M rows × 300 anonymized features; `train.csv` ~18 GB (community "low-mem" Parquet
  versions drop it to ~1.9 GB with float16).
- **Domain & data type**: Very large + wide financial — investment returns with `time_id`, `investment_id`,
  300 anonymized `f_0..f_299`, target.
- **Why it's on the list**: The capstone "big + wide" dataset. Combines everything: 18 GB CSV, 300 columns,
  time-series API constraints, and the need for serious dtype/format engineering. A natural finale after the
  earlier datasets.
- **Suggested learning focus**: Full out-of-core pipeline — convert to float16 Parquet partitioned by
  `time_id`; do EDA with DuckDB `SELECT ... WHERE time_id BETWEEN ...`; train with PySpark or Polars +
  LightGBM on sampled time slices; respect the time-series API (no forward peeking) and use time-based CV.
- **Difficulty**: Hard

---

## Suggested order to tackle them

1. **NYC Taxi Trip Duration** — warm-up: get comfortable with chunking, dtypes, and Polars on data that still
   fits in RAM.
2. **Jigsaw Toxic Comment** — switch axis to width: learn memory-aware text vectorization (hashing, sparse,
   `partial_fit`).
3. **Elo Merchant Category** — graduate to multi-table joins and per-group aggregate feature engineering.
4. **ASHRAE Great Energy Predictor III** — add time series: lag/rolling features, weather joins, time-based
   splits, Parquet partitioning.
5. **RSNA Pneumonia Detection** — learn the many-binary-files pattern: DICOM streaming + Parquet manifest.
6. **Jane Street Market Prediction** — master dtype reduction and CSV→Parquet conversion on a wide dataset.
7. **Bosch Production Line** — tackle extreme width + sparsity: column pruning, sparse storage, feature
   selection at scale.
8. **TalkingData AdTracking** — tackle extreme row count (~185M): sampling, chunked aggregation,
   out-of-core group-bys.
9. **H&M Personalized Fashion** — combine a 31.8M-row transactions table with image metadata for a full
   recommender pipeline.
10. **Ubiquant Market Prediction** — capstone: 18 GB + 300 columns + time-series constraints, tying together
    Parquet, DuckDB/Polars, sampling, and PySpark.

## Tooling notes

- **Pandas chunking**: `pd.read_csv(path, chunksize=100_000, usecols=[...], dtype={...})` — always pass `usecols`
  and `dtype` to cut memory; accumulate statistics across chunks rather than concatenating frames.
- **Parquet / Arrow**: Convert CSVs to Parquet once (with optimal dtypes: `int8/16/32`, `float32/16`,
  `category` for low-cardinality strings). Re-reads are 5–20× faster and far smaller; column pruning is free.
  Partition by a filter column (e.g., `time_id`, `building_id`, month) so you can read only the slice you need.
- **Polars lazy frames**: Use `pl.scan_parquet(...)` / `scan_csv(...)` and `.collect()` — the query optimizer
  pushes selections/projections down, so you only read what you need. Great for group-bys on millions of rows
  in memory or streaming.
- **DuckDB**: `duckdb.sql("SELECT ... FROM 'data.parquet' WHERE ...")` — query Parquet/CSV directly with SQL,
  no loading step. Excellent for fast ad-hoc aggregation and joins; pairs well with Arrow zero-copy to pandas/
  Polars.
- **PySpark**: Reach for it when data exceeds RAM across many files / partitions (e.g., TalkingData, Ubiquant,
  H&M). Use `spark.read.parquet`, `repartition`, and `cache` deliberately; prefer Parquet + column pruning over
  CSV; watch out for shuffles in wide group-bys.
- **Sampling strategies**: For EDA, take a **stratified** or **time-aware** sample rather than the first N rows
  (which are often chronologically sorted and biased). For imbalanced targets (TalkingData, Bosch), downsample
  the majority class; for time series, split by time, never randomly. Always validate that a small sample's
  distributions match the full data before trusting models trained on it.
