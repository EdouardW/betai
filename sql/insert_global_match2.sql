CREATE OR REPLACE FUNCTION ligue1.insert_global_match2()
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE
AS $BODY$

DECLARE
	p_result TEXT;
	p_nbre INTEGER;
	rawdata_cursor CURSOR FOR 
		(SELECT * FROM ligue1.essai);
	p_nb_insert NUMERIC;
	v_cnt NUMERIC;
BEGIN
FOR i in rawdata_cursor
	LOOP
		p_nb_insert := p_nb_insert + 1;
		INSERT INTO ligue1.essai2 (
			saison,
			ligue,
			journee,
			"date",
			id_match,
			team,
			lieu,
			adversaire,
			resultat,
			pour,
			contre,
			date_scrap)
		VALUES(
			i.saison,
			i.ligue,
			i.journee,
			i."date",
			i.id_match,
			i.hometeam,
			'D',
			i.awayteam,
			CASE 
				WHEN i."result"='1' THEN 'V' 
				WHEN i."result"='2' THEN 'D'
				WHEN i."result"='N' THEN 'N'
			END,
			i.home_score,
			i.away_score,
			i.date_scrap);
	GET DIAGNOSTICS v_cnt = ROW_COUNT;
	END LOOP;
RETURN ' nb_insert: ' || p_nb_insert::varchar;
EXCEPTION
WHEN OTHERS THEN
RETURN SQLERRM;
END;
$BODY$;