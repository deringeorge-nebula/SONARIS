"""
Module 1: Design Input Engine.

Accepts all user-supplied vessel parameters required for URN prediction and
validates them against physical plausibility bounds before passing them
downstream. Inputs include hull form coefficients (block coefficient Cb,
prismatic coefficient Cp, length-to-beam ratio L/B), propeller geometry (blade
count, pitch ratio P/D, diameter in meters), engine type (slow-speed diesel,
medium-speed diesel, gas turbine), rated shaft RPM, and operational speed in
knots. All inputs are validated and packaged into a ``VesselParameters``
dataclass. If any input falls outside physically meaningful bounds, this module
raises a descriptive ``ValidationError`` before any computation reaches Module 2.
No acoustic prediction logic lives here; the sole responsibility of this module
is input integrity.

Libraries: ``dataclasses`` (stdlib), ``typing`` (stdlib). Optional use of
``pydantic`` for schema validation if added in a later phase.

Pipeline position: First stage. Receives raw user input from the Streamlit UI
or from a direct Python API call. Outputs a ``VesselParameters`` object consumed
by the URN Prediction Core (Module 2).
"""

from modules.input_engine.design_input import VesselParameters, validate_inputs

__all__ = ["VesselParameters", "validate_inputs"]