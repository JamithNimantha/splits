CREATE TABLE IF NOT EXISTS public.splits
(
    symbol character varying(20) COLLATE pg_catalog."default" NOT NULL,
    split_from numeric(10,4) NOT NULL,
    split_to numeric(10,4) NOT NULL,
    ex_date date,
    country character varying(10) COLLATE pg_catalog."default",
	announcement_date date,
	payable_date date,
    record_date date,
    split_label character varying(150) COLLATE pg_catalog."default",
    exchange character varying(10) COLLATE pg_catalog."default",
    co_name character varying(150) COLLATE pg_catalog."default",
    optionable boolean,
    note character varying(25) COLLATE pg_catalog."default",
--    updated_timestamp timestamp without time zone,	
    update_date date NOT NULL,
    update_time time without time zone NOT NULL,
    CONSTRAINT splits_pkey PRIMARY KEY (symbol, split_from, split_to, ex_date, country)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.splits
    OWNER to postgres;