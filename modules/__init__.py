"""
SONARIS top-level modules package.

This package contains the six core processing modules that form the SONARIS
pipeline: Design Input Engine, URN Prediction Core, IMO Compliance Checker,
Marine Bioacoustic Impact Module, Mitigation Recommendation Engine, and Open
URN Database. Importing this package makes the module namespace available but
executes no computation. Each sub-module must be imported explicitly by the
caller.

Libraries: None at this level. Dependencies are declared within each sub-module.

Pipeline position: This is the root of the processing pipeline. Nothing feeds
into this package; it exposes the six modules to app.py and to the test suite.
"""