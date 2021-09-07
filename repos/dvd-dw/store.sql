
DROP TABLE IF EXISTS dw.store CASCADE;
CREATE TABLE IF NOT EXISTS dw.store AS
with data as (
SELECT 
store_id,
COUNT(1) as inventory_count
FROM dw.inventory
GROUP BY 1
)
SELECT 
	s.*,
	x.inventory_count
FROM dw.store_pre s
JOIN data x on s.store_id = x.store_id