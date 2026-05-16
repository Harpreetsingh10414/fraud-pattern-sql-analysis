CREATE OR REPLACE VIEW amount_flags AS

WITH baselines AS (

    SELECT
        card_id,
        AVG(amount) AS avg_amount,
        STDDEV_SAMP(amount) AS std_amount,
        COUNT(*) AS txn_count

    FROM transactions
    GROUP BY card_id
    HAVING COUNT(*) >= 10
),

scored AS (

    SELECT
        t.*,
        b.avg_amount,
        b.std_amount,
        (t.amount - b.avg_amount) /
        NULLIF(b.std_amount, 0) AS z_score

    FROM transactions t
    JOIN baselines b
        ON t.card_id = b.card_id
),

flagged AS (

    SELECT *,
        CASE
            WHEN z_score > 5 THEN 'HIGH'
            WHEN z_score > 3 THEN 'MEDIUM'
            ELSE 'NORMAL'
        END AS risk_level,

        CASE
            WHEN z_score > 3 THEN 1
            ELSE 0
        END AS is_amount_fraud

    FROM scored
)

SELECT *
FROM flagged
WHERE is_amount_fraud = 1;