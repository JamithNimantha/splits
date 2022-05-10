CREATE TABLE IF NOT EXISTS public.nasdaq_daily
(
    symbol character varying(10) COLLATE pg_catalog."default" NOT NULL,
    update_date date NOT NULL,
    company_name character varying(250) COLLATE pg_catalog."default",
    last_sale numeric(12,2),
    net_change numeric(12,2),
    percent_change numeric(12,4),
    market_cap_m integer,
    volume_t integer,
    ipo_year smallint,
    country character varying(30) COLLATE pg_catalog."default",
    sector character varying(30) COLLATE pg_catalog."default",
    industry character varying(80) COLLATE pg_catalog."default",
    bnw_symbol character varying(10) COLLATE pg_catalog."default",
    zck_symbol character varying(10) COLLATE pg_catalog."default",
    prn_symbol character varying(10) COLLATE pg_catalog."default",
    update_time time without time zone,
    CONSTRAINT nasdaq_daily_pkey PRIMARY KEY (symbol, update_date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.nasdaq_daily
    OWNER to postgres;
-- Index: nasdaq_daily_bnw_symbol

-- DROP INDEX IF EXISTS public.nasdaq_daily_bnw_symbol;

CREATE INDEX IF NOT EXISTS nasdaq_daily_bnw_symbol
    ON public.nasdaq_daily USING btree
    (bnw_symbol COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: nasdaq_daily_prn_symbol

-- DROP INDEX IF EXISTS public.nasdaq_daily_prn_symbol;

CREATE INDEX IF NOT EXISTS nasdaq_daily_prn_symbol
    ON public.nasdaq_daily USING btree
    (prn_symbol COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: nasdaq_daily_udate_date

-- DROP INDEX IF EXISTS public.nasdaq_daily_udate_date;

CREATE INDEX IF NOT EXISTS nasdaq_daily_udate_date
    ON public.nasdaq_daily USING btree
    (update_date ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: nasdaq_daily_zck_symbol

-- DROP INDEX IF EXISTS public.nasdaq_daily_zck_symbol;

CREATE INDEX IF NOT EXISTS nasdaq_daily_zck_symbol
    ON public.nasdaq_daily USING btree
    (zck_symbol COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;