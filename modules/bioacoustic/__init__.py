"""
Module 4: Marine Bioacoustic Impact Module.

Maps the predicted ship noise spectrum against the published audiogram
sensitivity curves of five marine mammal functional hearing groups and
quantifies the biological interference caused by the ship at each frequency band.
The five groups follow the NOAA/NMFS (2018) marine mammal acoustic weighting
function classification: low-frequency cetaceans (baleen whales), mid-frequency
cetaceans (dolphins and most toothed whales), high-frequency cetaceans (porpoises
and some small odontocetes), phocid pinnipeds in water, and otariid pinnipeds in
water.

The core method borrows two techniques from audio signal processing. First,
Mel-Frequency Cepstral Coefficient (MFCC) decomposition is applied to the ship
noise spectrum to extract a perceptually weighted frequency representation aligned
with the non-linear frequency sensitivity of the mammal ear. Second, spectral
masking analysis quantifies how much of the ship noise spectrum overlaps with and
energetically masks the frequency bands where each species group communicates and
echolocates. The combination of these two analyses produces the Biological
Interference Score (BIS), a value from 0 to 100 for each species group, where
100 represents complete masking of the group's functional hearing range. The BIS
is not a standardised regulatory metric; it is a SONARIS-defined index intended
to rank relative biological harm across design alternatives and routing scenarios.

Libraries: ``librosa`` for MFCC extraction, ``scipy.signal`` for spectral
masking computation, ``numpy``, ``matplotlib`` and ``plotly`` for spectrogram
overlay visualization.

Pipeline position: Fourth stage, running in parallel with Module 3. Receives
``URNSpectrum`` from Module 2. Outputs a ``BISResult`` object consumed by
Module 5.
"""

from modules.bioacoustic.audiogram_data import AUDIOGRAM_CURVES
from modules.bioacoustic.bis_calculator import calculate_bis, BISResult

__all__ = ["AUDIOGRAM_CURVES", "calculate_bis", "BISResult"]