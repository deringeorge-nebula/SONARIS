"""
Module 5: Mitigation Recommendation Engine.

Generates ranked mitigation recommendations based on the upstream outputs of
Modules 2, 3, and 4. Each recommendation addresses either a compliance failure
identified by Module 3 or a high Biological Interference Score identified by
Module 4, or both. Recommendations span two categories: operational (speed
reduction targets expressed in knots and the corresponding predicted dB
reduction, geographic routing avoidance zones keyed to known cetacean habitat
polygons) and design-level (hull coating options with published noise reduction
coefficients, propeller geometry modifications including skew angle adjustments
and blade count changes with expected BPF harmonic shifts). Each recommendation
is returned as a ``MitigationRecommendation`` object carrying a description,
the expected noise reduction in dB across affected frequency bands, the
species groups that benefit, and a confidence level based on how well the
recommendation type is supported by the available literature.

Recommendations are ranked by total expected noise reduction weighted by the
BIS scores of the affected species groups, so recommendations that reduce noise
in the most biologically sensitive frequency bands rank above those that reduce
broadband levels without addressing critical masking zones.

Libraries: ``numpy`` for ranking arithmetic. No external ML dependencies; the
recommendation logic is a rule-based system operating on structured inputs.

Pipeline position: Fifth and final computation stage. Receives ``URNSpectrum``
from Module 2, ``ComplianceResult`` from Module 3, and ``BISResult`` from
Module 4. Outputs a ranked list of ``MitigationRecommendation`` objects
rendered by the Streamlit UI and optionally stored in Module 6.
"""

from modules.mitigation.recommender import generate_recommendations, MitigationRecommendation

__all__ = ["generate_recommendations", "MitigationRecommendation"]