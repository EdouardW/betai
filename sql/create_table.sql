CREATE TABLE ligue1.essai2(
	saison character varying(20),
	ligue character varying(20),
	journee integer,
	date date, 
	id_match  character varying(20),
	team  character varying(50),
	lieu  character varying(10),
	adversaire  character varying(50),
	resultat  character varying(10),
	pour  character varying(10),
	contre  character varying(10),
	date_scrap  timestamp
)
