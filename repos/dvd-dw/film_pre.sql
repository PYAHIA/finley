DROP TABLE IF EXISTS dw.film_pre CASCADE;
CREATE TABLE dw.film_pre AS
SELECT * FROM public.film
;

DROP TABLE IF EXISTS dw.film_pre2;
CREATE TABLE dw.film_pre2 LIKE dw.film_pre INCLUDING PROJECTIONS;
INSERT /*+DIRECT*/ INTO dw.film_pre2;
SELECT * FROM public.film
;

