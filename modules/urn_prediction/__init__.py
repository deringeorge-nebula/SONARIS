"""
Module 2: URN Prediction Core.

Predicts a ship's underwater radiated noise spectrum from the vessel parameters
produced by Module 1. The prediction is hybrid: a physics layer and an AI layer
run in sequence, and their outputs are fused into a single spectrum.

The physics layer interfaces with OpenFOAM and libAcoustics to simulate propeller
cavitation and hull-induced turbulence noise. This layer is computationally
intensive and optional during development; it can be bypassed to run the AI layer
alone. The AI layer is a deep neural network implemented in PyTorch, trained on
the ShipsEar dataset (Santos-Dominguez et al., 2016) and the QiandaoEar22 dataset.
The network takes the structured ``VesselParameters`` object as input features
and returns a predicted noise level for each 1/3-octave band from 20 Hz to 20 kHz.
Output levels are in dB re 1 μPa at 1 m, the standard reference for underwater
source levels used in IMO MEPC.1/Circ.906 Rev.1 (2024).

Libraries: ``torch``, ``numpy``, ``scipy.signal``. OpenFOAM is invoked as a
subprocess via the physics layer; it is not a Python dependency.

Pipeline position: Second stage. Receives ``VesselParameters`` from Module 1.
Outputs a ``URNSpectrum`` object (a dict mapping Hz to dB re 1 μPa at 1 m)
consumed by Module 3 and Module 4.
"""

from modules.urn_prediction.physics_layer import run_physics_prediction
from modules.urn_prediction.ai_layer import run_ai_prediction, fuse_spectra

__all__ = ["run_physics_prediction", "run_ai_prediction", "fuse_spectra"]