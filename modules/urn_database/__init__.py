"""
Module 6: Open URN Database.

Manages the Open URN Database, the first open-source community-contributed
database of ship underwater radiated noise signatures. Each record stores vessel
metadata (IMO number, vessel type, length overall, beam, draft, propeller blade
count, engine type), measurement or prediction conditions (ship speed, loading
condition, water depth, measurement method), and the full 1/3-octave band
spectrum from 20 Hz to 20 kHz in dB re 1 μPa at 1 m. Records contributed by
the community are flagged with a provenance field indicating whether the spectrum
was measured at sea trial, predicted by SONARIS, or sourced from a published
dataset.

The development database is SQLite, stored locally under ``data/databases/``.
The production database targets PostgreSQL. The abstraction layer in
``db_manager.py`` uses connection strings compatible with both backends so that
the transition requires a single configuration change. All write operations
include input validation to enforce the schema before insertion. Query operations
support filtering by vessel type, IMO number, frequency band range, and date of
contribution, and return results as either Python dicts or Pandas DataFrames
depending on the caller's request.

Libraries: ``sqlite3`` (stdlib) for development, ``psycopg2`` for production,
``sqlalchemy`` for the abstraction layer, ``pandas`` for DataFrame output.

Pipeline position: Optional terminal stage that runs alongside or after Module 5.
Receives any combination of ``VesselParameters``, ``URNSpectrum``,
``ComplianceResult``, and ``BISResult`` objects for storage. Also serves as an
input source when Module 2 queries historical records for training data augmentation.
"""

from modules.urn_database.db_manager import DatabaseManager

__all__ = ["DatabaseManager"]