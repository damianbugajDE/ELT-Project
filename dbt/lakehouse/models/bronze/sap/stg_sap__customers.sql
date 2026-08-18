-- To jest treść Twojego modelu
SELECT
    customer_id,
    customer_name,
    country,
    created_at
FROM {{ source('main', 'raw_customers') }}