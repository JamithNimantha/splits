-- Don't Insert / Update if not in base_min_vol_prc
CREATE TABLE IF NOT EXISTS public.splits
(
-- Benzinga Ticker
-- Briefing Co:
    symbol character varying(20) COLLATE pg_catalog."default" NOT NULL,
-- Nasdaq: annoucedDate
-- If not available in case of Nasadq & not in database already
-- put Today - 6 Months (If the symbol is not already in the Table)
-- update note column with "announcement_date invalid"
-- Briefing Announced:
-- Benzinga: date_annouced    
    announcement_date date NOT NULL,
-- IF split_from > split_to 
--  	--> RSPLIT|FRM:<split_from>|TO:<split_to>|DT:<announcement_date>|REC:<record_date>|EX:<ex_date>
-- ELSE
--  	--> SPLIT|FRM:<split_from>|TO:<split_to>|DT:<announcement_date>|REC:<record_date>|EX:<ex_date>	
    split_label character varying(150) COLLATE pg_catalog."default",
-- Benzinga Exchange
-- Else get from base_min_vol_prc
    exchange character varying(10) COLLATE pg_catalog."default",
    country character varying(10) COLLATE pg_catalog."default",
-- Benzinga ratio, Nasdaq ratio: 4:01 --> 1
-- Briefing Ratio, 2-1 --> 1
    split_from numeric(10,4),
-- Benzinga ratio, Nasdaq ratio: 4:01 --> 4
-- Briefing Ratio, 2-1 --> 2    
    split_to numeric(10,4),
-- Nasdaq payableDate    
-- Briefing Payable 
-- Benzinga date_distribution
    payable_date date,
-- Benzinga date_recorded
    record_date date,
-- Nasdaq executionDate
-- Briefing Ex-Date
-- Benzinga date_ex 
    ex_date date,
-- Benzinga Name
-- Nasdaq Name
-- Briefing After Co: first value
    co_name character varying(150) COLLATE pg_catalog."default",
-- Briefing: Yes --> True, No --> False
-- Benzinga: optionable
    optionable boolean,
-- NASDAQ; If annoucement_date not available & not in database already
-- put Jan 1 of current year
-- update note column with "announcement_date invalid"
-- If annoucement date becomes available later, remove the note
-- Benzinga notes    
    note character varying(25) COLLATE pg_catalog."default",
-- Benzinga updated Convert from UNIX Timestamp
-- (Benzinga updated/86400)+DATE(1970,1,1)
    updated_timestamp timestamp without time zone, 
-- System Date
    update_date date,
-- System Time
    update_time time without time zone,
    CONSTRAINT splits_pkey PRIMARY KEY (symbol, announcement_date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.splits
    OWNER to postgres;