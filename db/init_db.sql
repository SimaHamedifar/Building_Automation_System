-- basic schema for storing energyplus outputs and setpoints
CREATE TABLE IF NOT EXISTS energyplus_timeseries (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMP NOT NULL,
  zone_name TEXT NOT NULL,
  outdoor_temp DOUBLE PRECISION,
  zone_air_temp DOUBLE PRECISION,
  hvac_power DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS setpoints (
  id SERIAL PRIMARY KEY,
  ts TIMESTAMP NOT NULL,
  zone_name TEXT NOT NULL,
  heating_setpoint DOUBLE PRECISION,
  cooling_setpoint DOUBLE PRECISION
);
