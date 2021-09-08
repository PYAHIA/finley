DROP TABLE IF EXISTS dw.store_pre CASCADE;
CREATE TABLE IF NOT EXISTS DW.STORE_pre AS
SELECT * FROM public.store;

select pg_sleep(30)       