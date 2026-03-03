# SONARIS Research Notes

This file is a running scientific journal for the SONARIS project. Every
significant research finding, dataset assessment, methodology decision, and
literature reference is logged here during development. Entries feed directly
into the methodology and literature review sections of the SONARIS research paper.

**Usage rules:**
- New entries go at the top of the file, below this header.
- Each entry must carry a date in ISO format (YYYY-MM-DD).
- If an entry is based on published literature, include the full reference at the
  bottom of that entry.
- Write for a technical reader who is encountering this topic for the first time
  in this project's context.

---

## 2026-03-03 — IMO MEPC.1/Circ.906 Rev.1 (2024): Regulatory Gap and Project Motivation

### What the guidelines require

IMO MEPC.1/Circ.906 Rev.1 (2024) is the current iteration of the IMO's voluntary
guidelines for the reduction of underwater noise from commercial shipping. The
circular applies to all new-build vessels and requests that shipowners and operators
monitor, manage, and where practicable reduce underwater radiated noise (URN) across
the ship's operational speed range. The guidelines specify that URN should be
characterized using 1/3-octave band measurements and reported in dB re 1 μPa at 1 m,
covering the frequency range relevant to marine mammal hearing (approximately 10 Hz
to 20 kHz depending on species). Vessels are categorised by type (bulk carrier,
container ship, tanker, passenger vessel, and others), and the guidelines provide
recommended management practices for each category. Crucially, the 2024 revision
sharpened the language from the 2014 original: shipyards and operators are now
explicitly encouraged to apply URN prediction tools at the design stage, not only
during sea trials.

### The gap: no open-source design-phase tool exists

The IMO GloNoise Partnership Programme conducted a structured gap analysis in October
2025. Its finding was direct: while IMO mandates URN management and design-stage
assessment, no open-source prediction or compliance-checking tool exists for
shipyards and researchers to use during the design phase. The only tools capable
of performing full-spectrum URN prediction (dBSea, ANSYS Fluent with acoustic
modules, GL ShipNoise) are commercial, proprietary, and priced out of reach for
most of the world's shipyards. A small shipyard in Southeast Asia, a research
institution in West Africa, or a student designing a vessel for a class project
cannot access these tools. This is not a niche gap: the IMO GloNoise report
notes that the majority of the global shipbuilding output by vessel count comes
from yards in developing economies where no licensed acoustic software is in use.

The consequence of this gap is that URN compliance is assessed, when it is assessed
at all, only at the sea trial stage. By that point the hull form is fixed, the
propeller is installed, and the engine mounts are set. Retrofitting for noise
reduction at sea trial is expensive and typically limited to operational adjustments
(speed reduction, routing) rather than design-level changes. The entire value of
design-stage prediction is lost.

### The frequency bands that matter

The IMO guidelines and the underlying marine bioacoustics literature converge on
three frequency bands of primary concern:

**Low frequency: 10 Hz to 1000 Hz.** This is the primary hearing range of baleen
whales (mysticetes), including blue, fin, sei, minke, and humpback whales.
Commercial shipping noise is dominated in this band by engine tonal components,
propeller shaft harmonics, and hull flow noise. The overlap is severe: fin whale
20 Hz calls sit directly in the band occupied by machinery noise from large
slow-speed diesel engines. This band is the primary driver of the chronic acoustic
masking problem for large whales in shipping lanes.

**Mid frequency: 1 kHz to 10 kHz.** This is the primary communication and
echolocation range of dolphins, porpoises, and toothed whales (odontocetes).
Propeller cavitation noise, which typically peaks between 1 kHz and 5 kHz
depending on ship speed and propeller design, falls directly in this band.
Bottlenose dolphin signature whistles, which are critical for individual
identification and group cohesion, occupy 3 kHz to 20 kHz. The interference
in this band is intermittent (tied to cavitation onset at specific speeds) but
acoustically intense.

**The blade-pass overlap zone: 50 Hz to 500 Hz.** The propeller blade-pass
frequency (BPF) is calculated as RPM/60 × blade count. For a typical
large commercial vessel running at 100 RPM with a 5-blade propeller, BPF is
approximately 8.3 Hz, with harmonics at 16.6 Hz, 25 Hz, and so on. At higher
shaft speeds typical of medium vessels, these harmonics fall squarely in the
50 Hz to 500 Hz range where both baleen whale low-frequency calls and toothed
whale social calls are concentrated. This harmonic overlap is what makes the
SONARIS Module 4 BIS calculation non-trivial: it is not sufficient to compare
broadband levels. Tonal interference at specific harmonics must be resolved.
This is precisely where the audio-engineering concept of spectral masking, as
used in perceptual audio codecs and MFCC-based speech analysis, applies directly
to the bioacoustic problem.

### Industry confirmation of demand

In October 2024, BIMCO (Baltic and International Maritime Council) and ICS
(International Chamber of Shipping), the two largest shipping industry bodies by
member tonnage, published a joint URN Management Guide. The guide explicitly
recommends that all member operators implement URN monitoring and compliance
workflows and calls on the industry to develop accessible tools for design-stage
prediction. This is the clearest statement from industry itself that demand for
a tool like SONARIS exists and that the current commercial tool landscape does not
meet it.

### Connection to SONARIS modules

Module 2 (URN Prediction Core) closes the prediction gap identified by the IMO
GloNoise analysis by producing a full 1/3-octave band spectrum at design stage
from vessel geometry and operational parameters alone, without requiring a physical
prototype or sea trial.

Module 3 (IMO Compliance Checker) closes the compliance assessment gap by
directly mapping the Module 2 output against the MEPC.1/Circ.906 Rev.1 (2024)
limit tables and issuing a structured pass/fail report, formatted for inclusion
in a ship's technical documentation package.

Module 4 (Marine Bioacoustic Impact Module) goes beyond what IMO currently
requires. The BIS metric provides a species-specific, frequency-resolved measure
of biological harm that the IMO guidelines acknowledge in principle but do not
operationalize. This positions SONARIS as a tool not just for compliance but for
genuine environmental assessment.

### References

- IMO MEPC.1/Circ.906 Rev.1 (2024). *2024 Guidelines for the Reduction of
  Underwater Noise from Commercial Shipping to Address Adverse Impacts on Marine
  Life.* International Maritime Organization, London.
- IMO GloNoise Partnership Programme (October 2025). *Gap Analysis: Underwater
  Radiated Noise Management Tools for Design-Phase Application.* International
  Maritime Organization, London.
- BIMCO and ICS (October 2024). *URN Management Guide for Shipping Operators.*
  Baltic and International Maritime Council / International Chamber of Shipping.