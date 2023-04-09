-- SQLite
-- SELECT * FROM price_data
-- WHERE symbol = 'dogecoin' AND date = '2013-12-15 01:00:00';

UPDATE price_data
SET open = round(open, 2),
    high = round(high, 2),
    low = round(low, 2),
    volume = round(volume, 2),
    close = round(close, 2);
