-- sql/velocity_fraud.sql

-- =========================================
-- Velocity Fraud Detection
-- Detect too many transactions in short time
-- =========================================

WITH rolling_counts AS (

    SELECT
        transaction_id,
        card_id,
        customer_id,
        amount,
        city,
        timestamp,

        -- Rolling transaction count in last 10 minutes
        COUNT(*) OVER (
            PARTITION BY card_id
            ORDER BY timestamp
            RANGE BETWEEN INTERVAL '10 minutes' PRECEDING AND CURRENT ROW
        ) AS txn_count_10min

    FROM transactions
),

flagged AS (

    SELECT *,
        
        -- Threshold = 5 transactions in 10 min
        CASE 
            WHEN txn_count_10min > 5 THEN 1
            ELSE 0
        END AS is_velocity_flag,

        -- Risk score scaling (simple)
        ROUND((txn_count_10min / 5.0) * 10, 2) AS risk_score

    FROM rolling_counts
)

SELECT *
FROM flagged
WHERE is_velocity_flag = 1;