-- sql/geo_fraud.sql

-- =========================================
-- Geographic Fraud Detection
-- Detect impossible travel between cities
-- =========================================

WITH txn_with_prev AS (

    SELECT
        transaction_id,
        card_id,
        customer_id,
        city,
        timestamp,
        amount,

        LAG(city) OVER (
            PARTITION BY card_id
            ORDER BY timestamp
        ) AS prev_city,

        LAG(timestamp) OVER (
            PARTITION BY card_id
            ORDER BY timestamp
        ) AS prev_timestamp

    FROM transactions
),

time_diff AS (

    SELECT *,

        DATEDIFF('minute', prev_timestamp, timestamp) AS time_diff_minutes

    FROM txn_with_prev
    WHERE prev_city IS NOT NULL
),

joined AS (

    SELECT
        t.*,
        d.min_travel_minutes

    FROM time_diff t
    LEFT JOIN read_csv_auto('data/city_distances.csv') d
        ON t.prev_city = d.city_from
        AND t.city = d.city_to
),

flagged AS (

    SELECT *,

        CASE
            WHEN prev_city != city
                 AND min_travel_minutes IS NOT NULL
                 AND time_diff_minutes < min_travel_minutes
            THEN 1
            ELSE 0
        END AS is_geo_fraud,

        ROUND(
            (min_travel_minutes - time_diff_minutes) / 10.0,
            2
        ) AS risk_score

    FROM joined
)

SELECT *
FROM flagged
WHERE is_geo_fraud = 1;