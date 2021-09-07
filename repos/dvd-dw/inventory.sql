DROP TABLE IF EXISTS dw.inventory cascade;
CREATE TABLE IF NOT EXISTS DW.inventory AS 
SELECT
title, s.store_id, inventory_id, category_name
FROM public.Inventory i
JOIN dw.film f on f.film_id = i.film_id
JOIN dw.store_pre s on s.store_id = i.store_id