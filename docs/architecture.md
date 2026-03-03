# SONARIS Project Architecture

**Full Name:** Ship-Ocean Noise Acoustic Radiated Intelligence System  
**License:** MIT  
**Python:** 3.10+

This document describes the complete folder structure of the SONARIS repository and the intended contents of every file.

---

## Folder Tree

```
sonaris/
|
|-- app.py                          # Streamlit entry point; assembles all module UIs into one application
|-- requirements.txt                # All Python dependencies, pinned with minimum version constraints
|-- .env.example                    # Template for environment variables (database path, API keys, debug flags)
|-- .gitignore                      # Ignores venv, __pycache__, .env, model weights, large data files
|-- LICENSE                         # MIT License text
|-- README.md                       # Project overview, architecture summary, setup instructions
|-- CONTRIBUTING.md                 # Contribution guidelines: code standards, PR process, scientific validation
|-- CHANGELOG.md                    # Version history and release notes
|
|-- docs/
|   |-- architecture.md             # This file: folder structure and per-file descriptions
|   |-- methodology.md              # Scientific methodology: FW-H equation, MFCC application, BIS scoring
|   |-- imo_guidelines.md           # Summary of IMO MEPC.1/Circ.906 Rev.1 (2024) limits used in Module 3
|   |-- datasets.md                 # Dataset descriptions, download instructions, and citation information
|   |-- api_reference.md            # Python API reference for headless use of each module
|   |-- deployment.md               # Instructions for deploying to Hugging Face Spaces and Streamlit Cloud
|
|-- sonaris/                        # Main Python package
|   |-- __init__.py                 # Package init; exposes URNPredictor, ComplianceChecker, BioacousticImpact
|   |
|   |-- module1_input/              # Module 1: Design Input Engine
|   |   |-- __init__.py
|   |   |-- input_schema.py         # Pydantic models defining and validating all vessel input parameters
|   |   |-- input_ui.py             # Streamlit UI component for Module 1: form fields, units, help tooltips
|   |   |-- parameter_utils.py      # Derived parameter calculations (e.g. advance ratio J from RPM and speed)
|   |   |-- validators.py           # Range checks and cross-parameter validation (e.g. propeller diameter vs draft)
|   |
|   |-- module2_urn/                # Module 2: URN Prediction Core
|   |   |-- __init__.py
|   |   |-- predictor.py            # Main URNPredictor class: orchestrates physics and AI layers, returns spectrum
|   |   |-- physics_layer.py        # OpenFOAM run management and libAcoustics FW-H post-processing wrapper
|   |   |-- ai_layer.py             # Loads trained model, runs inference, returns residual correction to physics output
|   |   |-- feature_engineering.py  # MFCC extraction, spectral envelope fitting, 1/3-octave band aggregation
|   |   |-- model_architecture.py   # PyTorch definition of the 1D-CNN + LSTM URN prediction network
|   |   |-- train.py                # Training script: data loading, loss function, optimizer, checkpoint saving
|   |   |-- evaluate.py             # Evaluation script: computes per-band MAE, RMSE against held-out test set
|   |   |-- uncertainty.py          # Monte Carlo dropout for prediction confidence interval estimation
|   |   |-- spectrum_utils.py       # Conversion utilities: Pa to dB, 1/1-octave to 1/3-octave, frequency array generation
|   |
|   |-- module3_compliance/         # Module 3: IMO Compliance Checker
|   |   |-- __init__.py
|   |   |-- checker.py              # ComplianceChecker class: loads limits, compares spectrum, returns verdict per band
|   |   |-- imo_limits.py           # Hard-coded URN limits from MEPC.1/Circ.906 Rev.1 by vessel type and frequency band
|   |   |-- report_generator.py     # Builds the downloadable PDF compliance report using ReportLab
|   |   |-- compliance_ui.py        # Streamlit UI component: compliance bar chart, pass/fail table, download button
|   |
|   |-- module4_bioacoustics/       # Module 4: Marine Bioacoustic Impact Module
|   |   |-- __init__.py
|   |   |-- impact_scorer.py        # BioacousticImpact class: computes BIS per species group from input spectrum
|   |   |-- audiograms.py           # Digitized hearing sensitivity curves for all 5 functional hearing groups
|   |   |-- masking_model.py        # Psychoacoustic masking model: excitation patterns, masking threshold calculation
|   |   |-- harmonic_overlap.py     # Finds ship tonal peaks within +/- 1/3 octave of published species call frequencies
|   |   |-- species_calls.py        # Published frequency ranges for vocalizations of each target species group
|   |   |-- bis_scoring.py          # BIS formula: integrates masked proportion of species frequency range (0-100 scale)
|   |   |-- bioacoustics_ui.py      # Streamlit UI: spectrogram overlay, BIS gauges, species selection panel
|   |
|   |-- module5_mitigation/         # Module 5: Mitigation Recommendation Engine
|   |   |-- __init__.py
|   |   |-- recommender.py          # MitigationRecommender class: takes compliance gaps and BIS, returns ranked actions
|   |   |-- speed_optimizer.py      # Predicts URN reduction as a function of speed reduction for given vessel type
|   |   |-- propeller_advisor.py    # Maps compliance gap magnitude to specific propeller geometry modification targets
|   |   |-- hull_treatment.py       # Recommends hull panel damping treatments based on dominant tonal frequencies
|   |   |-- routing_advisor.py      # Generates routing avoidance polygons around marine protected areas and known habitats
|   |   |-- mitigation_ui.py        # Streamlit UI: ranked recommendation cards with estimated dB reduction per action
|   |
|   |-- module6_database/           # Module 6: Open URN Database
|   |   |-- __init__.py
|   |   |-- models.py               # SQLAlchemy ORM models: Ship, URNRecord, Submission, UserContribution
|   |   |-- database.py             # Database engine setup, session factory, connection handling
|   |   |-- crud.py                 # Create, read, update, delete operations for all database tables
|   |   |-- submission_pipeline.py  # Validates, normalizes, and ingests community-submitted URN records
|   |   |-- quality_control.py      # Checks submissions against ShipsEar/QiandaoEar22 baseline distributions
|   |   |-- search.py               # Query functions: filter by vessel type, speed, frequency band, submission date
|   |   |-- database_ui.py          # Streamlit UI: search interface, submission form, record detail view
|   |   |-- migrations/             # Alembic migration scripts directory
|   |       |-- env.py              # Alembic environment configuration
|   |       |-- versions/           # Auto-generated migration version files go here
|   |
|   |-- shared/                     # Shared utilities used by more than one module
|       |-- __init__.py
|       |-- constants.py            # Physical constants, frequency band definitions, species group identifiers
|       |-- logging_config.py       # Loguru logger configuration applied consistently across all modules
|       |-- config.py               # Loads and exposes .env and config.yaml settings to all modules
|       |-- file_utils.py           # Helpers for reading/writing WAV, CSV, JSON, and HDF5 files
|       |-- plot_utils.py           # Shared Matplotlib/Plotly helper functions for consistent chart styling
|
|-- models/                         # Trained model weights and metadata (git-ignored for large files)
|   |-- urn_predictor_v1.pt         # Saved PyTorch model checkpoint after initial training run
|   |-- urn_predictor_v1_meta.json  # Training metadata: dataset split, hyperparameters, validation metrics
|
|-- data/                           # Local data storage (git-ignored except for structure and seed files)
|   |-- raw/                        # Raw downloaded datasets, unmodified
|   |   |-- shipsear/               # ShipsEar dataset audio files and metadata
|   |   |-- qiandaoear22/           # QiandaoEar22 dataset audio files and metadata
|   |   |-- audiograms/             # Published audiogram CSVs per species group
|   |
|   |-- processed/                  # Preprocessed features ready for model training
|   |   |-- mfcc_features.h5        # Extracted MFCC feature matrix for all training samples
|   |   |-- octave_spectra.h5       # 1/3-octave spectra computed from all training audio files
|   |   |-- labels.csv              # Vessel type labels and metadata for each training sample
|   |
|   |-- seed/                       # Small seed data committed to the repository
|       |-- imo_limits.json         # IMO MEPC.1/Circ.906 Rev.1 limit tables in machine-readable form
|       |-- species_audiograms.json # Digitized audiogram data for all 5 functional hearing groups
|       |-- species_calls.json      # Published vocalization frequency ranges per species group
|
|-- notebooks/                      # Research and development notebooks
|   |-- 01_dataset_exploration.ipynb       # Initial exploration of ShipsEar and QiandaoEar22 distributions
|   |-- 02_feature_engineering.ipynb       # MFCC pipeline development and 1/3-octave band analysis
|   |-- 03_model_training.ipynb            # URN prediction model training experiments and loss curves
|   |-- 04_compliance_validation.ipynb     # Verification of compliance checker against known test cases
|   |-- 05_bioacoustic_analysis.ipynb      # BIS scoring development and masking model calibration
|   |-- 06_mitigation_experiments.ipynb    # Speed-noise relationship analysis for mitigation module
|   |-- 07_database_schema_design.ipynb    # URN database schema development and query prototyping
|
|-- scripts/                        # Standalone scripts for data preparation and model management
|   |-- download_shipsear.py        # Downloads ShipsEar dataset from source and places it in data/raw/shipsear/
|   |-- download_qiandaoear.py      # Downloads QiandaoEar22 dataset and places it in data/raw/qiandaoear22/
|   |-- preprocess_audio.py         # Runs full audio-to-features pipeline and writes to data/processed/
|   |-- train_model.py              # CLI wrapper around module2_urn/train.py for scheduled training runs
|   |-- export_model.py             # Exports trained model to ONNX format for deployment environments
|   |-- init_database.py            # Creates database schema and loads seed data on first setup
|   |-- seed_database.py            # Populates URN database with curated example records for demonstration
|
|-- tests/                          # Test suite
|   |-- __init__.py
|   |-- conftest.py                 # Shared pytest fixtures: sample vessel parameters, synthetic spectra, db session
|   |
|   |-- test_module1/
|   |   |-- test_input_schema.py    # Tests that valid and invalid vessel parameter inputs are handled correctly
|   |   |-- test_validators.py      # Tests for all cross-parameter validation rules
|   |
|   |-- test_module2/
|   |   |-- test_feature_engineering.py   # Tests MFCC output shape, 1/3-octave band count, and numerical stability
|   |   |-- test_model_architecture.py    # Tests model forward pass shape and output range
|   |   |-- test_spectrum_utils.py        # Tests dB conversion, band aggregation, and frequency array generation
|   |
|   |-- test_module3/
|   |   |-- test_checker.py         # Tests compliance verdicts against known pass and fail spectra
|   |   |-- test_report_generator.py  # Tests PDF generation and checks that required sections are present
|   |
|   |-- test_module4/
|   |   |-- test_masking_model.py   # Tests masking threshold outputs against published psychoacoustic reference values
|   |   |-- test_bis_scoring.py     # Tests BIS edge cases: zero noise, full masking, single frequency input
|   |
|   |-- test_module5/
|   |   |-- test_recommender.py     # Tests that recommendations are ranked and non-empty for all compliance scenarios
|   |   |-- test_speed_optimizer.py # Tests speed-to-noise reduction curve against known ship data
|   |
|   |-- test_module6/
|       |-- test_crud.py            # Tests all database read and write operations against an in-memory SQLite instance
|       |-- test_quality_control.py # Tests rejection of out-of-distribution and malformed URN submissions
|
|-- config/
    |-- config.yaml                 # Default configuration: model paths, database URL, logging level, band definitions
    |-- logging.yaml                # Loguru handler configuration for file and console output
```

---

## File Count Summary

| Directory | Files |
|---|---|
| Root | 8 |
| docs/ | 6 |
| sonaris/ (package) | 52 |
| models/ | 2 |
| data/ | 9 |
| notebooks/ | 7 |
| scripts/ | 8 |
| tests/ | 17 |
| config/ | 2 |
| **Total** | **111** |

---

## Module to Directory Mapping

| Module | Directory |
|---|---|
| Module 1: Design Input Engine | `sonaris/module1_input/` |
| Module 2: URN Prediction Core | `sonaris/module2_urn/` |
| Module 3: IMO Compliance Checker | `sonaris/module3_compliance/` |
| Module 4: Marine Bioacoustic Impact | `sonaris/module4_bioacoustics/` |
| Module 5: Mitigation Recommendation Engine | `sonaris/module5_mitigation/` |
| Module 6: Open URN Database | `sonaris/module6_database/` |
| Shared Utilities | `sonaris/shared/` |

---

## Key Design Decisions

**Single package, modular internals.** All six modules live inside the `sonaris/` package. This means the Python API (`from sonaris import URNPredictor`) works without any knowledge of the internal module structure, while the internals remain cleanly separated.

**Seed data is version-controlled; raw audio is not.** The `data/seed/` directory (IMO limits, audiograms, species call ranges) is committed to the repository so the tool works out of the box. Raw audio datasets are large and externally hosted; the download scripts in `scripts/` handle retrieval.

**Model weights are not committed.** Trained `.pt` files live in `models/` which is git-ignored. The `scripts/train_model.py` script reproduces them from the processed dataset. A pre-trained checkpoint will be hosted separately on Hugging Face Hub.

**Migrations directory is tracked.** The `sonaris/module6_database/migrations/` directory and its `env.py` are committed. Individual migration version files are generated by Alembic as the schema evolves and should also be committed.

**One UI file per module.** Each module has a `_ui.py` file that defines its Streamlit component as a callable function. `app.py` imports and assembles these into a single multi-page application. This keeps UI logic out of the scientific core.