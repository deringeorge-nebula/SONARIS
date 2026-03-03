# Changelog

All notable changes to SONARIS are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### In Progress

- ShipsEar dataset exploratory data analysis (01_ShipsEar_EDA.ipynb)
- QiandaoEar22 dataset acquisition and initial inspection
- Marine mammal audiogram data collection for all 5 functional hearing groups
- IMO MEPC.1/Circ.906 Rev.1 (2024) URN limit table digitization into machine-readable JSON

---

## [0.1.0] - 2026-03-03

### Added

- Full repository folder structure scaffolded across all 6 core modules: Design Input Engine, URN Prediction Core, IMO Compliance Checker, Marine Bioacoustic Impact Module, Mitigation Recommendation Engine, and Open URN Database
- Python 3.14 virtual environment with 60+ dependencies installed including PyTorch, Streamlit, librosa, scipy, Plotly, ReportLab, SQLAlchemy, and scikit-learn
- README.md with full project mission, system architecture (Mermaid diagram), module descriptions, roadmap, tech stack table, dataset citations, and getting started instructions
- CONTRIBUTING.md with contribution workflows for five distinct contributor disciplines: naval architects, acousticians, marine biologists, machine learning engineers, and oceanographers
- CODE_OF_CONDUCT.md adapted from Contributor Covenant v2.1 with enforcement ladder and SONARIS-specific framing
- MIT License
- .gitignore configured for Python bytecode, virtual environment directories, PyTorch model weight files, and raw audio datasets
- Jupyter notebook pipeline initialized with librosa and matplotlib for acoustic data analysis

### Changed

- mSOUND removed from pip requirements due to PyPI package naming inconsistencies. Manual source integration from the mSOUND MATLAB/Python repository is planned for Phase 3 physics modeling work.
- pyaudio and spectrum removed from requirements.txt due to wheel unavailability on Python 3.14. Audio I/O and spectral estimation are handled by librosa and scipy.signal throughout the project.

### Notes

- Development environment: Windows, Windsurf IDE, Python 3.14
- pip upgraded to 26.0.1 during initial environment setup

[Unreleased]: https://github.com/deringeorge-nebula/SONARIS/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/deringeorge-nebula/SONARIS/releases/tag/v0.1.0