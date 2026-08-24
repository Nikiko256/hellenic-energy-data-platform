# Architecture

## Objective

Build a local-first batch data platform that processes Greek electricity-market and historical weather data.

## Data Flow 

```text 
ENTSO-E XML + Open-Meteo JSON
               |
        Python ingestion
               |
               v
      Bronze raw storage
               |
               v
      Silver Parquet data
               |
               v
     DuckDB Gold model
               |
               v
           Power BI
```

## Bronze

Bronze preserves original XML and JSON responses with request metadata and checksums.

## Silver

Silver contains typed, validated and deduplicated Parquet data.

All timestamps remain in UTC. Each electricity record preserves:

- `interval_start_utc`
- `interval_end_utc`
- `duration_minutes`

## Gold

Gold uses DuckDB and SQL to create dimensions, daily facts and analytical tables.

UTC timestamps are converted to `Europe/Athens` when assigning business dates.

## Main Datasets

- Greek actual electricity load
- Greek day-ahead electricity prices
- Historical weather for five selected Greek cities

## Important Limitation

The five-city weather aggregate is created only for exploratory comparison with national electricity metrics. It does not represent weather conditions for all of Greece.
4. Create the initial data dictionary