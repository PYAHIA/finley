DROP TABLE IF EXISTS dw.film_pre CASCADE;
CREATE TABLE dw.film_pre AS
SELECT * FROM public.film
;