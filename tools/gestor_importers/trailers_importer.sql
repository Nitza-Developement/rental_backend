SELECT
    -- 0
    t.vin,
    -- 1
    t.year,
    -- 2
    t.plate,
    -- 3
    t.type,
    -- 4
    t.active,
    -- 5
    m.brand_name

FROM rent_trailer as t
LEFT JOIN rent_manufacturer as m on m.id = t.manufacturer_id
