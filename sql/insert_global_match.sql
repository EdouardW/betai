CREATE OR REPLACE FUNCTION ligue1.insert_global_match()
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE
AS $BODY$

DECLARE
	p_result TEXT;
	p_nbre INTEGER;
	rawdata_cursor CURSOR FOR 
		(SELECT * FROM ligue1.sas_global_match WHERE status = 'ATRT');
	p_nb_insert NUMERIC;
	p_nb_existing NUMERIC;
	p_nb_atrt NUMERIC;
	v_cnt NUMERIC;
BEGIN
	p_nb_insert := 0 ;
	p_nb_existing := 0;
	p_nb_atrt := 0;
FOR i in rawdata_cursor
	LOOP
		IF i.home_score <> 'Reporté' THEN
			p_nb_atrt := p_nb_atrt + 1;
			SELECT count(*) INTO p_nbre FROM ligue1.global_match WHERE (id_match = i.id_match);
			IF p_nbre = 0 THEN
				p_nb_insert := p_nb_insert + 1;
				INSERT INTO ligue1.global_match (
					saison,
					ligue,
					journee,
					"date",
					id_match,
					"result",
					hometeam,
					awayteam,
					home_score,
					away_score,
					date_scrap)
				VALUES(
					i.saison,
					i.ligue,
					i.journee,
					i."date",
					i.id_match,
					i."result",
					i.hometeam,
					i.awayteam,
					i.home_score,
					i.away_score,
					i.date_scrap);
			ELSE
				p_nb_existing := p_nb_existing + 1;
			GET DIAGNOSTICS v_cnt = ROW_COUNT;
			END IF;
		END IF;
	UPDATE ligue1.sas_global_match SET status = 'TRT' WHERE CURRENT OF rawdata_cursor;
END LOOP;
RETURN 'nb_select: ' || p_nb_atrt::varchar || ' nb_existing: ' || p_nb_existing::varchar || ' nb_insert: ' || p_nb_insert::varchar;
EXCEPTION
WHEN OTHERS THEN
RETURN SQLERRM;
END;
$BODY$;