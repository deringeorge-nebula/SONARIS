# SONARIS System Architecture

This document describes the technical structure of the SONARIS codebase, the
purpose of every file in the repository, the data flow between modules, and
the design decisions made during Phase 0 setup. It serves as the primary
reference for contributors onboarding to the project and will be cited in the
SONARIS research paper as the system architecture reference.

The six core modules form a linear processing pipeline: user-supplied vessel
parameters enter Module 1 and are progressively transformed into an acoustic
spectrum (Module 2), a compliance verdict (Module 3), a biological impact score
(Module 4), and a set of mitigation recommendations (Module 5). Every record
produced or consumed by this pipeline can optionally be written to or read from
the Open URN Database (Module 6). No module performs computation before the
previous module's output is available, which keeps the data contract between
modules explicit and testable.

---

## Repository Tree
```
SONARIS/
├── app.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── .env.example
├── .gitignore
├── config/
│   └── settings.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── databases/
├── modules/
│   ├── __init__.py
│   ├── input_engine/
│   │   ├── __init__.py
│   │   └── design_input.py
│   ├── urn_prediction/
│   │   ├── __init__.py
│   │   ├── physics_layer.py
│   │   └── ai_layer.py
│   ├── imo_compliance/
│   │   ├── __init__.py
│   │   └── compliance_checker.py
│   ├── bioacoustic/
│   │   ├── __init__.py
│   │   ├── audiogram_data.py
│   │   └── bis_calculator.py
│   ├── mitigation/
│   │   ├── __init__.py
│   │   └── recommender.py
│   └── urn_database/
│       ├── __init__.py
│       └── db_manager.py
├── models/
│   ├── trained/
│   └── architectures/
├── notebooks/
│   └── 01_ShipsEar_EDA.ipynb
├── tests/
│   ├── __init__.py
│   └── test_modules.py
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   └── research_notes.md
├── ui/
│   ├── pages/
│   └── components/
└── .github/
    ├── pull_request_template.md
    ├── workflows/
    │   └── tests.yml
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        ├── feature_request.md
        └── data_contribution.md
```

---

## Per-File Descriptions

### Root

**app.py:** Entry point for the Streamlit application. Initialises the UI, routes
user interactions to the appropriate module calls, and renders output visualizations.

**requirements.txt:** Pinned list of all Python dependencies for the project.
Used by both local development setup and CI.

**README.md:** Public-facing project overview covering installation, usage, module
descriptions, and contribution instructions.

**CONTRIBUTING.md:** Contribution guide covering branch naming, commit conventions,
code style requirements, and the PR review process.

**CODE_OF_CONDUCT.md:** Contributor Covenant code of conduct for the SONARIS
open-source community.

**CHANGELOG.md:** Versioned log of all changes to the project, following Keep a
Changelog format.

**.env.example:** Template of all required environment variables with placeholder
values. Actual `.env` file is never committed.

**.gitignore:** Specifies files and directories excluded from version control,
including `.env`, trained model weights, raw datasets, and Python cache files.

### config/

**settings.py:** Central configuration for the application: database paths, model
paths, default operational parameters, and environment variable loading.

### data/

**raw/:** Storage directory for unprocessed source datasets (ShipsEar,
QiandaoEar22). Not committed to version control.

**processed/:** Storage directory for cleaned and feature-extracted datasets
ready for model training or evaluation.

**databases/:** Storage directory for the SQLite development database file.

### modules/

**modules/\_\_init\_\_.py:** Top-level package initialiser for the modules namespace.
Does not execute computation on import.

#### modules/input_engine/

**\_\_init\_\_.py:** Package initialiser for the Design Input Engine module.

**design_input.py:** Validates and structures all user-supplied vessel parameters
(hull coefficients, propeller geometry, engine type, speed) into a standardised
`VesselParameters` dataclass passed downstream.

#### modules/urn_prediction/

**\_\_init\_\_.py:** Package initialiser for the URN Prediction Core module.

**physics_layer.py:** Interfaces with OpenFOAM and libAcoustics to run
propeller cavitation simulations and extract the physics-based component of the
noise spectrum.

**ai_layer.py:** Loads the trained PyTorch neural network, runs inference on
the structured vessel parameters, and returns a predicted 1/3-octave band
spectrum in dB re 1 μPa at 1 m.

#### modules/imo_compliance/

**\_\_init\_\_.py:** Package initialiser for the IMO Compliance Checker module.

**compliance_checker.py:** Compares the predicted URN spectrum against the
vessel-type-specific limit tables from IMO MEPC.1/Circ.906 Rev.1 (2024) and
returns a structured `ComplianceResult` with per-band pass/fail flags.

#### modules/bioacoustic/

**\_\_init\_\_.py:** Package initialiser for the Marine Bioacoustic Impact Module.

**audiogram_data.py:** Contains the published audiogram sensitivity curves for
five marine mammal functional hearing groups: low-frequency cetaceans, mid-frequency
cetaceans, high-frequency cetaceans, phocid pinnipeds in water, and otariid pinnipeds
in water.

**bis_calculator.py:** Applies MFCC decomposition and spectral masking analysis
to quantify the overlap between the ship noise spectrum and each species group's
hearing sensitivity range, producing a Biological Interference Score per group.

#### modules/mitigation/

**\_\_init\_\_.py:** Package initialiser for the Mitigation Recommendation Engine.

**recommender.py:** Receives upstream outputs (URN spectrum, compliance result,
BIS scores) and generates ranked mitigation recommendations with estimated noise
reduction in dB for each option.

#### modules/urn_database/

**\_\_init\_\_.py:** Package initialiser for the Open URN Database module.

**db_manager.py:** Handles all database operations: schema initialisation, record
insertion, querying by vessel type or frequency band, and export to JSON or CSV.

### models/

**trained/:** Storage directory for serialised trained model weights (`.pt` files).
Not committed to version control.

**architectures/:** Python files defining the PyTorch neural network architectures
used in Module 2.

### notebooks/

**01_ShipsEar_EDA.ipynb:** Exploratory data analysis notebook for the ShipsEar
dataset. Covers class distribution, spectrogram inspection, signal-to-noise
assessment, and feature extraction prototyping.

### tests/

**tests/\_\_init\_\_.py:** Makes the tests directory a Python package.

**test_modules.py:** pytest test suite covering unit tests for all six modules.
Integration tests covering the full pipeline are added here as modules mature.

### docs/

**architecture.md:** This file. Technical reference for the repository structure,
data flow, module interfaces, and design decisions.

**api_reference.md:** Auto-generated or manually maintained documentation of all
public functions and classes across the six modules.

**research_notes.md:** Running scientific journal for the project. Logs dataset
assessments, methodology decisions, and literature references that feed into the
eventual SONARIS research paper.

### ui/

**pages/:** Streamlit multi-page app files, one per major UI view.

**components/:** Reusable Streamlit UI components shared across pages.

### .github/

**pull_request_template.md:** Template automatically loaded when a contributor
opens a pull request, including the pre-merge checklist and scientific basis
section.

**workflows/tests.yml:** GitHub Actions workflow that runs the pytest test suite
on every push and every pull request targeting main.

**ISSUE_TEMPLATE/bug_report.md:** Structured template for reporting bugs.

**ISSUE_TEMPLATE/feature_request.md:** Structured template for proposing new
features.

**ISSUE_TEMPLATE/data_contribution.md:** Structured template for contributing
URN measurement records to the Open URN Database.

---

## Data Flow

1. The user supplies vessel parameters through the Streamlit UI or directly via
   the Python API. Inputs include hull form coefficients (Cb, Cp, L/B ratio),
   propeller geometry (blade count, pitch ratio, diameter), engine type, rated
   RPM, and operational speed in knots.

2. **Module 1 (Design Input Engine)** validates all inputs, applies physical
   plausibility checks, and packages them into a `VesselParameters` dataclass.
   This object is the sole input passed to Module 2.

3. **Module 2 (URN Prediction Core)** receives the `VesselParameters` object.
   The physics layer optionally runs an OpenFOAM simulation to produce a
   physics-derived partial spectrum. The AI layer runs the trained PyTorch
   model to produce a data-driven full spectrum. The two layers are fused into
   a single `URNSpectrum` object: a dict mapping each 1/3-octave band center
   frequency (Hz) to a level in dB re 1 μPa at 1 m.

4. **Module 3 (IMO Compliance Checker)** receives the `URNSpectrum` and the
   vessel type string from `VesselParameters`. It returns a `ComplianceResult`
   object containing a per-band pass/fail dict, an overall compliance flag, and
   the reference limit values used for comparison.

5. **Module 4 (Marine Bioacoustic Impact Module)** receives the `URNSpectrum`.
   It applies MFCC decomposition across the spectrum and computes spectral overlap
   against each of the five audiogram curves. It returns a `BISResult` object:
   a dict mapping each marine mammal group name to its Biological Interference
   Score (0 to 100) and the frequency bands driving the interference.

6. **Module 5 (Mitigation Recommendation Engine)** receives the `URNSpectrum`,
   the `ComplianceResult`, and the `BISResult`. It returns a ranked list of
   `MitigationRecommendation` objects, each containing a description, the
   expected noise reduction in dB, and the applicable species groups or
   frequency bands.

7. All outputs can optionally be written to **Module 6 (Open URN Database)** as
   a structured record containing vessel metadata, measurement conditions, and
   the full `URNSpectrum`. Records are also queryable from the database to
   populate the community dataset.

---

## Module Interfaces

**Module 1: Design Input Engine**
Input: Raw user-supplied values via form or dict. Hull coefficients, propeller
geometry, engine type, RPM, speed in knots.
Output: `VesselParameters` dataclass with validated and typed fields.
Key dependencies: `pydantic` or `dataclasses`, `scipy` for range validation.

**Module 2: URN Prediction Core**
Input: `VesselParameters` dataclass.
Output: `URNSpectrum` — dict mapping 1/3-octave band center frequencies (Hz)
to levels in dB re 1 μPa at 1 m, covering 20 Hz to 20 kHz.
Key dependencies: `torch`, `numpy`, `scipy`, OpenFOAM CLI (optional physics layer).

**Module 3: IMO Compliance Checker**
Input: `URNSpectrum`, vessel type string.
Output: `ComplianceResult` — overall pass/fail flag, per-band results, limit
values from IMO MEPC.1/Circ.906 Rev.1 (2024).
Key dependencies: Internal lookup tables encoding IMO limit values by vessel type.

**Module 4: Marine Bioacoustic Impact Module**
Input: `URNSpectrum`.
Output: `BISResult` — per-species-group Biological Interference Score and
contributing frequency band list. Spectrogram overlay data for visualization.
Key dependencies: `librosa`, `scipy.signal`, `numpy`, `matplotlib`.

**Module 5: Mitigation Recommendation Engine**
Input: `URNSpectrum`, `ComplianceResult`, `BISResult`.
Output: List of `MitigationRecommendation` objects ranked by expected dB
reduction.
Key dependencies: Internal rule engine and lookup tables. No external ML.

**Module 6: Open URN Database**
Input (write): Vessel metadata dict + `URNSpectrum` + measurement conditions dict.
Input (read): Query parameters (vessel type, IMO number, frequency range, date range).
Output (read): List of matching database records as dicts or Pandas DataFrames.
Key dependencies: `sqlite3` (development), `psycopg2` (production), `pandas`.

---

## Design Decisions

**1. mSOUND removed from pip, manual source integration planned for Phase 3.**
mSOUND is not available as a pip-installable package compatible with the project's
Python environment. Rather than vendor an untested integration in Phase 0, the
physics simulation layer is scoped to OpenFOAM plus libAcoustics for Phases 1 and 2.
mSOUND will be integrated manually from source in Phase 3 once the core pipeline
is stable.

**2. pyaudio and spectrum removed due to Python 3.14 wheel unavailability.**
Neither `pyaudio` nor `spectrum` publish binary wheels for Python 3.14 on Windows
as of Phase 0. Both would require a local C++ build toolchain. All audio processing
and spectral estimation needed for the MFCC pipeline is available through `librosa`
and `scipy.signal`, which do provide 3.14-compatible wheels. The two packages were
removed from `requirements.txt` with no loss of required functionality.

**3. MFCC pipeline uses librosa and scipy only.**
The bioacoustic masking and MFCC analysis in Module 4 are implemented entirely
with `librosa` for feature extraction and `scipy.signal` for spectral processing.
This keeps the dependency count low, avoids binary-only packages, and gives full
access to the intermediate signal representations needed for the BIS calculation.

**4. CI uses Python 3.11 while local development uses Python 3.14.**
GitHub Actions Ubuntu runners have stable binary wheel availability for all SONARIS
dependencies on Python 3.11. Python 3.14 is used locally on Windows because it is
the active development environment, but forcing 3.14 in CI would require compiling
several packages from source and would make CI fragile. The API surface used by
SONARIS does not differ between 3.11 and 3.14 for any dependency in scope.

**5. SQLite used for development, PostgreSQL targeted for production.**
SQLite requires no server process and works identically across all developer
machines. The `db_manager.py` abstraction layer uses SQLAlchemy-compatible
connection strings so that switching to PostgreSQL in production requires changing
one configuration value, not the query logic.