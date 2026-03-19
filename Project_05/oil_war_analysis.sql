CREATE TABLE country_impact(
Country TEXT,
Region TEXT,
Oil_Import_Pct FLOAT,
GDP_Impact_Pct FLOAT,
Inflation_Risk TEXT,
Stock_Market_Change FLOAT,
Currency_Pressure TEXT,
Policy_Response TEXT,
Vulnerability TEXT,
Population_M INT
);

CREATE TABLE oil_prices(
Date DATE,
Brent_USD FLOAT,
WTI_USD FLOAT,
Brent_Change_Pct FLOAT,
WTI_Change_Pct FLOAT,
Phase TEXT,
Strait_Hormuz TEXT
);

CREATE TABLE petrol_prices(
Country TEXT,
ISO TEXT,
Region TEXT,
Currency TEXT,
Before_War_Price FLOAT,
Mar7_Price FLOAT,
Unit TEXT,
Amount_Change FLOAT,
Pct_Increase FLOAT,
Trend TEXT,
Before_War_USD FLOAT,
Mar7_USD FLOAT,
Oil_Import_Dep TEXT
);

CREATE TABLE pros_cons(
Category TEXT,
Type TEXT,
Title TEXT,
Description TEXT,
Impact_Level TEXT,
Affected TEXT,
Source TEXT
);

CREATE TABLE war_events(
Date DATE,
Event TEXT,
Description TEXT,
Location TEXT,
Category TEXT
);

SELECT *
FROM country_impact;

SELECT *
FROM oil_prices;

SELECT *
FROM petrol_prices;

SELECT *
FROM pros_cons;

SELECT *
FROM war_events;

SELECT "Country", COUNT(*)
FROM country_impact
GROUP BY "Country"
HAVING COUNT(*) > 1;

SELECT *
FROM oil_prices
WHERE "Brent_USD" IS NULL;

ALTER TABLE oil_prices
ALTER COLUMN "Date" TYPE DATE
USING "Date"::DATE;

--Market Shock Analysis---

-- q1 : Did oil prices increase after the conflict?

SELECT "Phase", AVG("Brent_USD"),AVG("WTI_USD")
FROM oil_prices
GROUP BY "Phase";

--q2 : Which event triggered oil spike?

SELECT 
w."Date",
w."Event",
o."Brent_USD",
o."Brent_Change_Pct"
FROM war_events AS w
JOIN oil_prices AS o
ON TO_DATE(w."Date", 'YYYY-MM-DD') = o."Date";

SELECT c."Country",c."Oil_Import_Pct",
c."GDP_Impact_Pct",
c."Inflation_Risk",
p."Pct_Increase"
FROM country_impact AS c
JOIN petrol_prices AS p
ON c."Country" = p."Country";

SELECT
c."Country",
c."Population_M",
p."Pct_Increase"
FROM country_impact c
JOIN petrol_prices p
ON c."Country" = p."Country";

