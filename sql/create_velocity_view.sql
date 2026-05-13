CREATE OR REPLACE VIEW velocity_flags AS

WITH rolling_counts AS (

    SELECT
        transaction_id,
        card_id,
        customer_id,
        amount,
        city,
        timestamp,

        COUNT(*) OVER (
            PARTITION BY card_id
            ORDER BY timestamp
            RANGE BETWEEN INTERVAL '10 minutes' PRECEDING AND CURRENT ROW
        ) AS txn_count_10min

    FROM transactions
),

flagged AS (

    SELECT *,
        CASE 
            WHEN txn_count_10min > 5 THEN 1
            ELSE 0
        END AS is_velocity_flag,
        ROUND((txn_count_10min / 5.0) * 10, 2) AS risk_score
    FROM rolling_counts
)

SELECT *
FROM flagged
WHERE is_velocity_flag = 1;