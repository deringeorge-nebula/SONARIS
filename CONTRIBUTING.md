# Contributing to SONARIS

SONARIS is an open-source platform for predicting ship underwater radiated noise, verifying IMO compliance, and quantifying acoustic harm to marine mammals. It is student-led, research-grade, and built to be used by shipyards, classification societies, environmental NGOs, naval engineers, and ocean researchers worldwide. Every meaningful contribution, whether code, data, documentation, or scientific critique, directly improves a tool that has real environmental consequences.

Contributors from any background are welcome. You do not need to be a software engineer. Naval architects, acousticians, marine biologists, oceanographers, and data scientists all have things to contribute here that a programmer alone cannot.

---

## Types of Contributions

### Code

- New features within any of the six modules
- Bug fixes with a clear description of the problem being solved
- Tests that cover untested behavior in existing code
- Performance improvements to signal processing pipelines or model inference
- Refactoring that improves readability or reduces technical debt without changing behavior

### Data

- Measured URN spectra for any vessel type, submitted to the Open URN Database (Module 6)
- Published audiogram data for marine mammal species not currently covered in Module 4
- Validation datasets that can be used to benchmark the URN prediction model against real measurements
- Marine protected area boundary files or shipping lane data for the routing avoidance module

### Documentation

- Corrections or clarifications to existing docs
- API reference entries for undocumented functions
- Tutorials showing how to use SONARIS for a specific task
- Research notes that explain the scientific background behind a module

### Scientific Contributions

- Methodology improvements backed by published literature
- Challenges to existing algorithms, including the BIS scoring formula, the MFCC feature pipeline, or the masking model
- Literature reviews that identify gaps or errors in the current approach
- Validation studies comparing SONARIS predictions to measured data

### Bug Reports

If something is broken or produces incorrect results, filing a clear bug report is a contribution. Instructions are in the Reporting Bugs section below.

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/deringeorge-nebula/SONARIS.git
cd SONARIS

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note on mSOUND:** The mSOUND acoustic simulation library is not available via pip and must be integrated manually from source. This is only required for Phase 3 work on the physics simulation layer. If you are not working on OpenFOAM or wave propagation components, you do not need it.

**Note on pyaudio:** pyaudio has been removed from requirements.txt due to a wheel incompatibility with Python 3.14. It is not required for any current development work. All audio processing uses librosa and scipy.

After installation, verify your setup:

```bash
pytest tests/ -v
```

All tests should pass before you begin making changes.

---

## Contribution Workflow

### 1. Fork and branch

Fork the repository on GitHub, then create a branch from `main` using the naming conventions below.

```
feat/module-name-description     # new features
fix/issue-description            # bug fixes
data/dataset-name                # data contributions
docs/topic                       # documentation changes
```

Examples:

```
feat/module4-porpoise-audiogram
fix/module2-mfcc-window-overlap
data/shipsear-bulk-carrier-records
docs/bis-scoring-methodology
```

### 2. Make your changes

Keep commits focused. One logical change per commit. Write commit messages in the imperative: `Add porpoise audiogram to Module 4` not `Added porpoise audiogram`.

### 3. Run tests

```bash
pytest tests/ -v
```

If your change touches a specific module, run only that module's tests first:

```bash
pytest tests/test_module4/ -v
```

Add new tests for any new behavior you introduce. Untested code will not be merged.

### 4. Submit a pull request

Open a pull request against the `main` branch. In the description:

- State what the change does and why it is needed
- Reference any related issue with `Closes #issue-number` if applicable
- For scientific changes, cite the source that justifies the approach
- For data contributions, include metadata as described in the Data Contribution Guidelines below

PRs will be reviewed for correctness, code quality, and scientific validity. Reviews may take time. If you do not hear back within two weeks, comment on the PR to follow up.

---

## Code Standards

**Style:** Follow PEP 8. Line length maximum is 100 characters. Use `black` for formatting and `isort` for import ordering. Both are in requirements.txt.

```bash
black sonaris/
isort sonaris/
```

**Type hints:** All functions in the six core module directories (`sonaris/module1_input/` through `sonaris/module6_database/`) must include type hints on all parameters and return values. Shared utilities in `sonaris/shared/` should also have type hints but may have exceptions for highly dynamic functions.

**Docstrings:** Use Google-style docstrings. Every public function and class needs a docstring that states what it does, what the parameters are, and what it returns. For functions that implement a specific algorithm or formula, include a reference to the source.

Example:

```python
def compute_bis(
    ship_spectrum_db: np.ndarray,
    audiogram_db: np.ndarray,
    frequency_bands: np.ndarray
) -> float:
    """Compute the Biological Interference Score for a single species group.

    Calculates the proportion of the species' audible frequency range where
    ship noise exceeds the masking threshold, normalized to a 0-100 scale.
    Based on the masking model described in Moore (2012), Chapter 3.

    Args:
        ship_spectrum_db: Received ship noise level in dB re 1 uPa, one value
            per 1/3-octave band.
        audiogram_db: Hearing threshold in dB re 1 uPa for the species group,
            aligned to the same frequency bands.
        frequency_bands: Center frequencies of each 1/3-octave band in Hz.

    Returns:
        BIS score from 0.0 (no interference) to 100.0 (complete masking).
    """
```

**Inline comments:** Write comments to explain why, not what. If the code is readable and the comment just restates what the line does, delete the comment.

**Tests:** Use pytest. Test files go in `tests/test_moduleN/` matching the module being tested. Test functions should have names that describe the specific scenario being tested, not just the function name.

---

## Data Contribution Guidelines

Measured or published URN data can be contributed directly to the Open URN Database (Module 6). Data contributions are valuable even if you cannot contribute code.

### Required metadata for each record

| Field | Description |
|---|---|
| `vessel_type` | IMO vessel type category (cargo, tanker, container, bulk, passenger, etc.) |
| `length_m` | Length between perpendiculars in meters |
| `speed_knots` | Ship speed during measurement |
| `engine_type` | Diesel, diesel-electric, gas turbine, or other |
| `propeller_type` | FPP, CPP, or other, with blade count if known |
| `measurement_method` | How the data was acquired: sea trial, tank test, model prediction, published paper |
| `frequency_resolution` | 1/3-octave, 1/1-octave, or narrowband |
| `source_reference` | DOI, report number, or dataset name |
| `license` | Confirm the data can be shared under CC BY 4.0 or equivalent |

### Format

Submit spectra as a CSV with columns `frequency_hz` and `spl_db` (dB re 1 µPa @ 1m). Include a JSON sidecar file with the metadata fields above. See `data/seed/` for examples of the expected format.

### How to submit

For small submissions (fewer than 10 records), include the CSV and JSON files in a pull request under `data/contributions/`. For larger datasets, open a GitHub issue with the label `data-contribution` and describe the dataset. We will coordinate the ingestion process.

Data contributed to SONARIS must be yours to share, or from a published source with a license that permits redistribution. Do not submit proprietary or confidential data.

---

## Reporting Bugs

Before filing a bug report, check whether the issue already exists in the [GitHub Issues](https://github.com/deringeorge-nebula/SONARIS/issues) list.

When filing a new issue, use the Bug Report template and include:

- **What you expected to happen**, stated specifically
- **What actually happened**, with the full error message or incorrect output
- **Steps to reproduce the issue**, as minimal as possible
- **Your environment:** operating system, Python version, relevant package versions
- **Which module** the bug is in, if known

If the bug produces incorrect scientific output (wrong URN values, wrong compliance verdict, wrong BIS score), that is a high-priority issue. Flag it clearly and include the input parameters that produced the wrong result.

---

## Scientific Contributions

SONARIS's methodology is not fixed. The BIS scoring formula, the psychoacoustic masking model, the MFCC feature pipeline, and the compliance interpretation logic are all open to scrutiny and improvement.

To propose a methodology change:

1. Open a thread in [GitHub Discussions](https://github.com/deringeorge-nebula/SONARIS/discussions) under the "Science" category
2. State the current approach and what you believe is wrong or suboptimal about it
3. Propose an alternative, with citations to published literature that support it
4. If you have validation data that demonstrates the improvement, include it or describe how to obtain it

Scientific disagreement is welcome and expected. A methodology that has been challenged and defended is more credible than one that has not been examined. If you believe a part of the platform produces results that are scientifically indefensible, say so clearly and explain why.

For literature contributions, you can open a Discussion thread or submit a PR adding references to `docs/datasets.md` or `docs/methodology.md`. Include the full citation and a one-paragraph summary of how the source is relevant.

---

## Contact

Open a [GitHub Discussion](https://github.com/deringeorge-nebula/SONARIS/discussions) for questions, ideas, or anything that does not fit into an issue. For bugs and specific technical problems, file a [GitHub Issue](https://github.com/deringeorge-nebula/SONARIS/issues).