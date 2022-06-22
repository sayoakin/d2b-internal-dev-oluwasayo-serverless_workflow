import pyarrow as pa

SCHEMA = pa.schema([
    ('uuid', pa.string()),
    ('first_name', pa.string()),
    ('last_name', pa.string()),
    ('email_address', pa.string()),
    ('number_of_visits', pa.int8()),
    ('time_spent', pa.float64()),
    ('amount_spent', pa.float64()),
    ('date_of_visits', pa.date32()),
])
