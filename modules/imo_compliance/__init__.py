"""
Module 3: IMO Compliance Checker.

Receives the predicted URN spectrum from Module 2 and the vessel type string
from the ``VesselParameters`` object produced by Module 1. Checks each 1/3-octave
band level against the vessel-type-specific limit values defined in IMO
MEPC.1/Circ.906 Rev.1 (2024) and returns a structured compliance result. The
result includes a per-band pass/fail flag, the limit value applied at each band,
the measured (predicted) level, and the exceedance in dB where a band fails.
An overall compliance flag aggregates the per-band results. The module can also
generate a formatted compliance report suitable for inclusion in a vessel's
technical documentation package.

The limit tables are encoded directly in this module as Python dicts keyed by
vessel type and center frequency. When IMO updates its guidelines, these tables
are the only code that requires updating.

Libraries: Internal lookup tables only. ``fpdf2`` or ``reportlab`` for PDF
report generation (added in Phase 2).

Pipeline position: Third stage. Receives ``URNSpectrum`` from Module 2 and
vessel type from Module 1. Outputs a ``ComplianceResult`` object consumed by
Module 5 and optionally written to Module 6.
"""

from modules.imo_compliance.compliance_checker import check_compliance, ComplianceResult

__all__ = ["check_compliance", "ComplianceResult"]