
CREATE SCHEMA IF NOT EXISTS staging;

DROP TABLE IF EXISTS staging.customers;

CREATE TABLE staging.customers AS
WITH cleaned AS (
    SELECT
        TRIM(customer_id) AS customer_id,
        INITCAP(TRIM(first_name)) AS first_name,
        INITCAP(TRIM(last_name)) AS last_name,
        LOWER(TRIM(email)) AS email,
        NULLIF(TRIM(phone), '') AS phone,
        INITCAP(TRIM(city)) AS city,
        INITCAP(TRIM(gender)) AS gender,
        date_of_birth,
        registration_date,
        loaded_at,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(customer_id)
            ORDER BY loaded_at DESC
        ) AS row_num
    FROM raw.customers
    WHERE customer_id IS NOT NULL
      AND TRIM(customer_id) <> ''
)
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    gender,
    date_of_birth,
    registration_date,
    loaded_at
FROM cleaned
WHERE row_num = 1;
