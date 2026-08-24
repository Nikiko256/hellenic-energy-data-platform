# Data Dictionary

## Silver Tables

| Table | Grain | Natural key |
|---|---|---|
| `silver_load_inernal` | One Greek load observation per source interval | `area_code, interval_start_utc` |
| `silver_price_interval` | One Greek day-ahead price per market interval | ` area_code, interval_start_utc` |
| `silver_weather_interval` | One weather observation per location and hour | `location_id, interval_start_utc` |

## Gold Tables

| Table | Grain |
|---|---|
| `dim_date` | One Greek local calendar date |
| `dim_location` | One configured weather location |
| `fact_energy_market_daily` | One Greek bidding zone and local date |
| `fact_weather_daily` | One location and local date |
| `fact_selected_city_weather_daily` | One local date aggregated across the five selected cities |
| `mart_daily_energy_selected_city_weather` | One local date combining electricity and selected-city weather metrics |

## Units

| Field | Unit |
|---|---|
| `load_mw` | Megawatts |
| `load_mwh` | Megawatt-hours |
| `price_eur_mwh` | Euros per megawatt-hour |
| `temperature_c` | Degrees Celsius |
| `precipitation_mm` | Millimetres |
| `wind_speed_kmh` | Kilometres per hour |
| `duration_minutes` | Minutes |