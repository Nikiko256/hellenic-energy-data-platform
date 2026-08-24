# Architecture Decisions

## Local-first impementation

The authoritative platform runs locally so it remains reproductive without Fabric or other cloud services

## Raw-data preservation

Original XML and JSON responses are retained in Bronze to support auditing, debugging and reprocessing.

## UTC time policy 

Bronze and Silver use UTC. Conversion to `Europe/Athens` occurs only when Gold business dates are calculated.

## Source interval preservation

ENTSO-E observations retain their original 15-minute or 60-minute duration. They are not artificially converted into hourly records.

# Silver storage 

Silver uses Parquet because it provides typed compressed and column-oriented analytical storage.

# Gold processing

DuckDB performs the main relational transformations, dimensional modelling and analytical SQL.

## Selected-city weather

Weather data covers five modeled locations. Their equal-weight aggregate is not describedas as national Greek weather.

## Technology scope

Streaming, Kafka, Airflow, Kubernetes and machine learning are excluded because this project is a batch data-engineering platform and does not require them.