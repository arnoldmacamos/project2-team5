
-- Table: public.parties

-- DROP TABLE public.parties;

CREATE TABLE public.parties
(
    party_id integer NOT NULL,
    party_code character varying(12) COLLATE pg_catalog."default" NOT NULL,
    party_name text COLLATE pg_catalog."default" NOT NULL,
    pro_brexit character varying(2) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT parties_pkey PRIMARY KEY (party_id)
)

TABLESPACE pg_default;

ALTER TABLE public.parties
    OWNER to postgres;



-- Table: public.constituencies

-- DROP TABLE public.constituencies;

CREATE TABLE public.constituencies
(
    const_id integer NOT NULL,
    ons_code character varying(12) COLLATE pg_catalog."default" NOT NULL,
    constituency_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT constituencies_pkey PRIMARY KEY (const_id)
)

TABLESPACE pg_default;

ALTER TABLE public.constituencies
    OWNER to postgres;
	
	


-- Table: public.brexit_results

-- DROP TABLE public.brexit_results;

CREATE TABLE public.brexit_results
(
    id integer NOT NULL,
    const_id integer NOT NULL,
    probrexit_share numeric NOT NULL,
    antibrexit_share numeric NOT NULL,
    year integer NOT NULL,
    CONSTRAINT brexit_results_pkey PRIMARY KEY (id),
    CONSTRAINT "FK_brexit_results_const_id" FOREIGN KEY (const_id)
        REFERENCES public.constituencies (const_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.brexit_results
    OWNER to postgres;



-- Table: public.election_results

-- DROP TABLE public.election_results;

CREATE TABLE public.election_results
(
    id integer NOT NULL,
    const_id integer NOT NULL,
    party_id integer NOT NULL,
    votes_share numeric NOT NULL,
    year integer NOT NULL,
    CONSTRAINT election_results_pkey PRIMARY KEY (id),
    CONSTRAINT "FK_election_results_const_id" FOREIGN KEY (const_id)
        REFERENCES public.constituencies (const_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "FK_election_results_party_id" FOREIGN KEY (party_id)
        REFERENCES public.parties (party_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.election_results
    OWNER to postgres;	
	
	