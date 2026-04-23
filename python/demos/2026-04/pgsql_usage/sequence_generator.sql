CREATE TABLE IF NOT EXISTS serial_sequence
(
    site_code     VARCHAR(1) not null,
    year_week     VARCHAR(4) not null,
    current_value INTEGER    not null,
    PRIMARY KEY (site_code, year_week)
);

CREATE OR REPLACE FUNCTION get_next_serial_sequence(p_site VARCHAR, p_yw VARCHAR)
    RETURNS INTEGER AS
$$
DECLARE
    v_next_val INTEGER;
BEGIN
    INSERT INTO serial_sequence (site_code, year_week, current_value)
    VALUES (p_site, p_yw, 1)
    ON CONFLICT (site_code, year_week)
        DO UPDATE SET current_value = serial_sequence.current_value + 1
    RETURNING current_value INTO v_next_val;

    RETURN v_next_val;
END;
$$ LANGUAGE plpgsql;
