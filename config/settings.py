"""
config/settings.py

Single source of truth for all constants and configuration values used across
the SONARIS platform. Every module imports from here. No module should define
a scientific constant, regulatory parameter, processing default, or system path
locally. If a value might be reused anywhere else in the codebase, it belongs
in this file.
"""

import math
from typing import Dict, List, Tuple

# =============================================================================
# SECTION 1 - Acoustic Frequency Range
# =============================================================================

FREQ_MIN_HZ: int = 20
FREQ_MAX_HZ: int = 20_000

# Reference pressure for underwater acoustics: 1 micropascal.
# All dB values in SONARIS are expressed as dB re 1 uPa at 1m unless stated.
# This is the universal standard for underwater source levels (ISO 18405:2017).
FREQ_REF_UNDERWATER: float = 1e-6  # Pa

# Reference pressure for airborne acoustics: 20 micropascals.
# Included for comparison purposes only. All ship noise output is underwater.
# Standard defined in ISO 1683:2015.
FREQ_REF_AIRBORNE: float = 2e-5  # Pa


# =============================================================================
# SECTION 2 - 1/3 Octave Band Center Frequencies (ISO 266)
# =============================================================================

# Standard 1/3-octave band center frequencies from 20 Hz to 20 kHz.
# These are the exact preferred frequencies from ISO 266:1997.
# There are 31 bands in this range.
THIRD_OCTAVE_CENTER_FREQUENCIES: List[float] = [
    20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160,
    200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
    2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000,
    20000,
]

# Band edge calculation follows IEC 61260-1:2014.
# lower = f_center / 2^(1/6), upper = f_center * 2^(1/6)
_BAND_FACTOR: float = 2 ** (1 / 6)

THIRD_OCTAVE_LOWER_LIMITS: List[float] = [
    round(f / _BAND_FACTOR, 4) for f in THIRD_OCTAVE_CENTER_FREQUENCIES
]

THIRD_OCTAVE_UPPER_LIMITS: List[float] = [
    round(f * _BAND_FACTOR, 4) for f in THIRD_OCTAVE_CENTER_FREQUENCIES
]


# =============================================================================
# SECTION 3 - Marine Mammal Functional Hearing Groups
# =============================================================================
# Frequency ranges are based on NOAA/NMFS (2018) acoustic weighting functions
# and audiogram data compiled in Southall et al. (2019) "Marine Mammal Noise
# Exposure Criteria: Updated Scientific Recommendations for Residual Hearing
# Effects", Aquatic Mammals, 45(2).
#
# communication_freq_min/max represents the band where the species group
# primarily signals to conspecifics. This is the band used for BIS calculation.
# hearing_freq_min/max is the full audiometric range.

LOW_FREQUENCY_CETACEANS: Dict = {
    "name": "Low-Frequency Cetaceans (Baleen Whales)",
    "examples": ["Blue whale", "Fin whale", "Humpback whale", "Sei whale", "Minke whale"],
    "hearing_freq_min_hz": 7,
    "hearing_freq_max_hz": 35_000,
    "communication_freq_min_hz": 10,
    "communication_freq_max_hz": 1_000,
    # Fin whale 20 Hz calls and blue whale 17-20 Hz infrasonic pulses anchor
    # the lower bound. Upper bound follows NOAA LF weighting function.
    "imo_group": "LF",
}

MID_FREQUENCY_CETACEANS: Dict = {
    "name": "Mid-Frequency Cetaceans (Dolphins, Toothed Whales)",
    "examples": ["Bottlenose dolphin", "Sperm whale", "Killer whale", "Beluga whale"],
    "hearing_freq_min_hz": 150,
    "hearing_freq_max_hz": 160_000,
    "communication_freq_min_hz": 5_000,
    "communication_freq_max_hz": 80_000,
    # Bottlenose dolphin signature whistles peak 3-15 kHz. Sperm whale clicks
    # are broadband but centre around 15 kHz. Upper bound follows NOAA MF weighting.
    "imo_group": "MF",
}

HIGH_FREQUENCY_CETACEANS: Dict = {
    "name": "High-Frequency Cetaceans (Porpoises, Small Odontocetes)",
    "examples": ["Harbour porpoise", "Dall's porpoise", "Commerson's dolphin"],
    "hearing_freq_min_hz": 200,
    "hearing_freq_max_hz": 180_000,
    "communication_freq_min_hz": 100_000,
    "communication_freq_max_hz": 150_000,
    # Harbour porpoise echolocation clicks are narrowband around 130 kHz.
    # This group is the most sensitive to high-frequency shipping noise components.
    "imo_group": "HF",
}

PHOCID_PINNIPEDS_UNDERWATER: Dict = {
    "name": "Phocid Pinnipeds in Water (True Seals)",
    "examples": ["Harbour seal", "Grey seal", "Weddell seal", "Ringed seal"],
    "hearing_freq_min_hz": 50,
    "hearing_freq_max_hz": 86_000,
    "communication_freq_min_hz": 1_000,
    "communication_freq_max_hz": 50_000,
    # Phocids hear well underwater; audiogram peak sensitivity is around 10-30 kHz.
    # Communication calls (e.g. Weddell seal trills) fall 1-10 kHz.
    "imo_group": "PPW",
}

OTARIID_PINNIPEDS_UNDERWATER: Dict = {
    "name": "Otariid Pinnipeds in Water (Sea Lions, Fur Seals)",
    "examples": ["California sea lion", "Northern fur seal", "Steller sea lion"],
    "hearing_freq_min_hz": 60,
    "hearing_freq_max_hz": 39_000,
    "communication_freq_min_hz": 1_000,
    "communication_freq_max_hz": 30_000,
    # Otariids have narrower underwater hearing than phocids. California sea lion
    # audiogram shows best sensitivity around 1-16 kHz (Kastak & Schusterman 1998).
    "imo_group": "OW",
}

# Ordered list consumed by Module 4's BIS calculator. Order is preserved
# in all output tables and visualizations.
MARINE_MAMMAL_GROUPS: List[Dict] = [
    LOW_FREQUENCY_CETACEANS,
    MID_FREQUENCY_CETACEANS,
    HIGH_FREQUENCY_CETACEANS,
    PHOCID_PINNIPEDS_UNDERWATER,
    OTARIID_PINNIPEDS_UNDERWATER,
]


# =============================================================================
# SECTION 4 - Biological Interference Score (BIS) Thresholds
# =============================================================================
# BIS is a SONARIS-defined metric: 0 to 100, representing the fraction of a
# species group's communication band that is energetically masked by ship noise.
# Thresholds are defined by analogy with audiological masking literature and
# calibrated to the frequency resolution of 1/3-octave bands.
# "Critical" at 75% is grounded in the observation that communication
# success in cetaceans drops sharply when SNR falls below -6 dB across
# more than 3/4 of the call bandwidth (Erbe et al., 2016, "The effects of
# ship noise on marine mammals", Frontiers in Marine Science).

BIS_THRESHOLDS: Dict[str, Tuple[float, float]] = {
    "negligible": (0.0, 10.0),   # < 10% of communication band masked
    "low":        (10.0, 25.0),  # 10 to 25%
    "moderate":   (25.0, 50.0),  # 25 to 50%
    "high":       (50.0, 75.0),  # 50 to 75%
    "critical":   (75.0, 100.0), # > 75%: species group is functionally deaf
                                 # to conspecific signals in this environment
}

# Standalone threshold used in Module 3 and Module 5 logic.
BIS_CRITICAL_THRESHOLD: float = 75.0


# =============================================================================
# SECTION 5 - IMO Vessel Type Categories
# =============================================================================
# Vessel type codes follow the categorization in IMO MEPC.1/Circ.906 Rev.1.
# These codes are used as keys in the URN limit tables below and in database
# records. Short codes are snake_case for use as dict keys and URL parameters.

IMO_VESSEL_TYPES: Dict[str, str] = {
    "bulk_carrier":  "Bulk Carrier",
    "tanker":        "Tanker (Oil / Chemical / LNG)",
    "container":     "Container Ship",
    "general_cargo": "General Cargo Ship",
    "roro":          "Ro-Ro Cargo Ship",
    "passenger":     "Passenger Ship",
    "cruise":        "Cruise Ship",
    "ferry":         "Ferry",
    "naval":         "Naval Vessel",
    "research":      "Research Vessel",
    "offshore":      "Offshore Support Vessel",
    "tug":           "Tug",
    "fishing":       "Fishing Vessel",
    "icebreaker":    "Icebreaker",
}


# =============================================================================
# SECTION 6 - IMO URN Limit Tables
# =============================================================================
# Source level limits by vessel type and 1/3-octave band center frequency.
# Units: dB re 1 uPa at 1m.
# Reference: IMO MEPC.1/Circ.906 Rev.1 (2024), Annex, Table 1.
#
# TODO (Phase 1): Digitize the full limit table from the official IMO document
# for all vessel types and all 31 bands. The three container ship values below
# are representative placeholders derived from the published figure in
# MEPC.1/Circ.906 Rev.1 and should be replaced with exact table values
# once the document is formally acquired.

IMO_URN_LIMITS: Dict[str, Dict[int, float]] = {
    "container": {
        # Freq (Hz): max allowed source level (dB re 1 uPa at 1m)
        100:  149.0,  # placeholder — confirm against MEPC.1/Circ.906 Rev.1 Annex Table 1
        315:  144.0,  # placeholder
        1000: 136.0,  # placeholder
    },
    # TODO: populate all vessel types from the official IMO document
    "bulk_carrier":  {},
    "tanker":        {},
    "general_cargo": {},
    "roro":          {},
    "passenger":     {},
    "cruise":        {},
    "ferry":         {},
    "naval":         {},
    "research":      {},
    "offshore":      {},
    "tug":           {},
    "fishing":       {},
    "icebreaker":    {},
}


# =============================================================================
# SECTION 7 - Signal Processing Configuration
# =============================================================================

# Default sample rate for librosa operations.
# 22050 Hz is librosa's default and covers the full 20 Hz to 10 kHz range
# at Nyquist. For analysis above 10 kHz, resample to 44100 Hz before processing.
SAMPLE_RATE: int = 22_050  # Hz

# FFT window size. 2048 samples at 22050 Hz gives ~93 ms windows,
# which resolves frequency to ~10.8 Hz per bin. Adequate for 1/3-octave grouping.
N_FFT: int = 2048

# Hop length: number of samples between consecutive STFT frames.
# 512 gives ~75% overlap with a 2048-point window, standard for acoustic analysis.
HOP_LENGTH: int = 512

# Number of MFCC coefficients. 40 resolves the 20 Hz to 20 kHz range
# across the Mel scale without redundancy. Matching the standard used in
# the ShipsEar dataset feature extraction pipeline keeps the AI layer consistent.
N_MFCC: int = 40

# Hann window is the default for acoustic STFT analysis. It minimises spectral
# leakage without excessive main-lobe broadening (Harris, 1978).
WINDOW_FUNCTION: str = "hann"

# Alias so module code can reference CENTER_FREQUENCIES without importing
# the full list name, which is verbose in signal processing loops.
CENTER_FREQUENCIES: List[float] = THIRD_OCTAVE_CENTER_FREQUENCIES


# =============================================================================
# SECTION 8 - OpenFOAM Simulation Defaults
# =============================================================================

# Number of parallel MPI processes for OpenFOAM runs.
# 4 cores is a safe default for development machines. Override in .env for HPC.
OPENFOAM_DEFAULT_CORES: int = 4

# End time for cavitation transient simulation in seconds.
# 0.5 s captures several propeller blade-pass cycles at typical shaft speeds
# without excessive computation.
SIMULATION_END_TIME: float = 0.5  # seconds

# Time step for the simulation. 1e-5 s satisfies the Courant condition for
# typical ship speeds and mesh resolutions used in propeller cavitation cases.
SIMULATION_TIMESTEP: float = 1e-5  # seconds

# Write OpenFOAM results to disk every 100 time steps.
# At 1e-5 s per step, this gives output every 1 ms of simulated time.
OUTPUT_WRITE_INTERVAL: int = 100  # time steps


# =============================================================================
# SECTION 9 - Database Configuration
# =============================================================================

# SQLite connection strings for development and test environments.
# Format follows SQLAlchemy engine URL syntax so switching to PostgreSQL
# requires only changing this string, not the query logic in db_manager.py.
DATABASE_DEV: str = "sqlite:///data/databases/sonaris_dev.db"
DATABASE_TEST: str = "sqlite:///data/databases/sonaris_test.db"

# PostgreSQL connection string template for production.
# Actual credentials are loaded from .env; this is the format reference only.
DATABASE_PROD_TEMPLATE: str = "postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Table name for the URN signature records in both SQLite and PostgreSQL.
URN_DATABASE_TABLE: str = "urn_signatures"

# Minimum fields required for a valid URN database contribution.
# Records missing any of these fields are rejected at the write layer.
MIN_REQUIRED_FIELDS: List[str] = [
    "vessel_type",
    "loa_m",
    "speed_knots",
    "propulsion_type",
    "blade_count",
    "measurement_standard",
    "spectrum_data",
]


# =============================================================================
# SECTION 10 - Project Metadata
# =============================================================================

PROJECT_NAME: str = "SONARIS"
PROJECT_FULL_NAME: str = "Ship-Ocean Noise Acoustic Radiated Intelligence System"
PROJECT_VERSION: str = "0.1.0"
PROJECT_LICENSE: str = "MIT"
PROJECT_GITHUB: str = "https://github.com/deringeorge-nebula/SONARIS"

# The specific IMO circular version this codebase implements.
# Update this string whenever a new revision of the guidelines is adopted.
IMO_GUIDELINES_VERSION: str = "MEPC.1/Circ.906 Rev.1 (2024)"

SUPPORTED_PYTHON: str = ">=3.11"