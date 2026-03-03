---
name: Data Contribution
description: Submit URN measurements, audiogram data, or acoustic datasets for the Open URN Database
title: "[DATA] "
labels: ["data-contribution", "urn-database"]
assignees: []
---

Thank you for contributing to the Open URN Database. SONARIS depends on real-world acoustic measurements to train better models and validate its predictions. Every submission is reviewed for format and quality before being merged. Please fill in as much detail as you can.

---

## Data Type

Select all that apply.

- [ ] Underwater Radiated Noise (URN) spectrum measurements
- [ ] Marine mammal audiogram data
- [ ] Propeller cavitation noise recordings
- [ ] Hull vibration measurements
- [ ] Ambient ocean noise baseline data
- [ ] Other (describe below):

---

## Ship Details (for URN submissions)

Leave blank if not applicable to your data type.

| Field | Your value |
|---|---|
| Vessel type | cargo / tanker / passenger / container / bulk carrier / naval / research / ferry / other |
| Approximate LOA (m) | |
| Propulsion type | diesel / diesel-electric / gas turbine / other |
| Number of propeller blades | |
| Fixed or controllable pitch propeller | FPP / CPP / unknown |
| Ship speed during measurement (knots) | |
| Engine RPM during measurement | |

---

## Measurement Details

| Field | Your value |
|---|---|
| Measurement standard used | ISO 17208 / ANSI/ASA S12.64 / DNV / other / unknown |
| Hydrophone depth (m) | |
| Distance from ship (m) | |
| Sea state (Beaufort scale) | |
| Water depth at measurement location (m) | |

---

## Data Format

| Field | Your value |
|---|---|
| File format | WAV / CSV / MAT / HDF5 / other |
| Sampling rate (Hz) | |
| Frequency resolution | 1/3-octave / 1/1-octave / narrowband / other |
| Number of recordings or records | |

---

## Data Source and Rights

- [ ] This is my own original measurement data
- [ ] This data is from a published paper or public dataset

If from a published source, provide the full citation or DOI (e.g. https://doi.org/10.xxxx/xxxxx):



- [ ] I confirm I have the right to release this data under MIT License or CC BY 4.0 or an equivalent open license.

---

## Quality Notes

Describe any known limitations: calibration status, background noise conditions, measurement uncertainty, equipment used, or reasons a record might be considered low-confidence.

---

## Submission Method

- [ ] I will attach files directly to this issue
- [ ] I will submit a pull request to data/contributions/
- [ ] The data is available at a public URL (provide link below)
- [ ] I need help with the submission format first

**Link or notes:**

---

- [ ] I have read the Data Contribution Guidelines in CONTRIBUTING.md and confirm this submission meets the format and licensing requirements described there.