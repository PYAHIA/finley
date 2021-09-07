DROP TABLE IF EXISTS dw.film cascade;
CREATE TABLE IF NOT EXISTS DW.film AS 
SELECT 
	f.*, 
	category.name as category_name
FROM public.film_category c
	JOIN public.category on c.category_id = category.category_id
	JOIN dw.film_pre f on f.film_id =c.film_id
;