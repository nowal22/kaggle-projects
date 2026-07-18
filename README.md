# Kaggle Projects — Data Science Practice

A personal workspace for working through Kaggle datasets and building small
projects and notebooks, with a focus on learning to handle **large datasets**
efficiently (memory, I/O, out-of-core processing, columnar formats, etc.).

## Context

I'm an MS Analytics student at Georgia Tech entering my second year. This repo
is a sandbox for practicing end-to-end data-science workflows on real Kaggle
datasets — from downloading and inspecting data, to cleaning, modeling, and
writing up what I learned.

## Repository Structure

```
kaggle-projects/
├── projects/        # One subfolder per Kaggle dataset/project
│   └── <dataset>/   #   each with its own notebook + notes.md
├── data/
│   ├── raw/         # Downloaded, unmodified data (gitignored contents)
│   └── processed/   # Cleaned/feature-engineered data (gitignored contents)
├── notebooks/       # Shared exploratory notebooks (not tied to one dataset)
├── src/             # Reusable helper code (loaders, transformers, utils)
├── utils/           # Scripts: data loading, kaggle download helpers
├── docs/            # Notes, learning logs, references
├── .gitignore
├── requirements.txt
├── RECOMMENDED_DATASETS.md
└── README.md
```

> `data/raw/` and `data/processed/` contents are gitignored (datasets are
> large). The directories themselves are kept in git via `.gitkeep` files.

## Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url> kaggle-projects
cd kaggle-projects
```

### 2. Create a virtual environment

Using the standard library:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Or using [`uv`](https://github.com/astral-sh/uv) (faster, recommended):

```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# or, with uv:
uv pip install -r requirements.txt
```

### 4. Set up the Kaggle API

1. Sign in at <https://www.kaggle.com/> and go to **Account → API → Create New Token**.
   This downloads a `kaggle.json` file containing your username and API key.
2. On macOS, place it at `~/.kaggle/kaggle.json` and restrict its permissions:

```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

3. Verify the CLI works:

```bash
kaggle datasets list -s "titanic"
```

> **Never commit `kaggle.json`.** It is gitignored in this repo.

## Adding a New Kaggle Project

Use **one folder per dataset** under `projects/`. A typical project layout:

```
projects/<dataset-slug>/
├── <dataset-slug>.ipynb   # Main analysis/modeling notebook
├── notes.md               # Short write-up: goal, approach, findings, next steps
└── (optional) src/        # Project-specific helpers if needed
```

Convention:

- Name the folder using the Kaggle dataset slug (e.g. `titanic`,
  `new-york-city-taxi-fare-prediction`).
- Keep the notebook focused on that dataset; put reusable logic in the
  top-level `src/` or `utils/` folders so other projects can import it.
- Download raw data into `data/raw/<dataset-slug>/` (gitignored) using the
  helper in `utils/kaggle_download.py` so you don't store large files in git.
- Write a short `notes.md` per project capturing what you tried and learned.

## Datasets to Work On

See [RECOMMENDED_DATASETS.md](RECOMMENDED_DATASETS.md) for a curated list of
datasets — including several chosen specifically for practicing techniques
that matter when working with large datasets (chunking, sampling, columnar
formats, out-of-core processing with Polars/DuckDB/PySpark).

## License

MIT — see [LICENSE](LICENSE) (placeholder).
