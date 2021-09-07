create local temporary table tmp on commit preserve rows as 
WITH data AS (
	SELECT
	actor_id,
	film_id,
	row_number() over(PARTITION BY actor_id ORDER BY last_update) as i
	FROM film_actor
)
SELECT 
actor_id, title as last_title
FROM data x
join dw.film a on a.film_Id = x.film_id
WHERE i = 1
;

DROP TABLE IF EXISTS dw.actor CASCADE;
CREATE TABLE dw.actor AS
SELECT
	actor.actor_id,
	last_name || ', ' || first_name as name,
	last_title
FROM public.actor
JOIN tmp on actor.actor_id = tmp.actor_id
;