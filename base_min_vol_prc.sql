CREATE OR REPLACE VIEW public.base_min_vol_prc
 AS
 SELECT nasdaq_daily.symbol,
    nasdaq_daily.update_date,
    nasdaq_daily.company_name,
    nasdaq_daily.last_sale,
    nasdaq_daily.net_change,
    nasdaq_daily.percent_change,
    nasdaq_daily.market_cap_m,
    nasdaq_daily.volume_t,
    nasdaq_daily.ipo_year,
    nasdaq_daily.country,
    nasdaq_daily.sector,
    nasdaq_daily.industry,
    nasdaq_daily.update_time
   FROM nasdaq_daily
  WHERE NOT (length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%WS'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%U'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%R'::text OR nasdaq_daily.company_name::text ~~* '%BENEFICIAL%'::text OR nasdaq_daily.company_name::text ~~* '%TRUST%'::text OR nasdaq_daily.company_name::text ~~* '%ETF'::text OR nasdaq_daily.company_name::text ~~* '% ETF %'::text OR nasdaq_daily.company_name::text ~~* '%PREFERRED%'::text OR nasdaq_daily.company_name::text ~~* '%NTS'::text OR nasdaq_daily.company_name::text ~~* '%WARRANT'::text OR nasdaq_daily.company_name::text ~~* '%UNIT'::text OR nasdaq_daily.company_name::text ~~* '%UNITS'::text OR nasdaq_daily.company_name::text ~~* '%FUND%'::text OR nasdaq_daily.company_name::text ~~* '%WTS'::text OR nasdaq_daily.company_name::text ~~* '%UTS'::text OR nasdaq_daily.company_name::text ~~* 'ABERDEEN%'::text OR nasdaq_daily.company_name::text ~~* 'ADVISOR%'::text OR nasdaq_daily.company_name::text ~~* '%DEBS'::text) AND nasdaq_daily.symbol::text ~ '^[^0-9]*$'::text AND nasdaq_daily.company_name::text ~ '^[^0-9]*$'::text AND nasdaq_daily.volume_t > 15 AND nasdaq_daily.last_sale > 0.85 AND nasdaq_daily.update_date = (( SELECT max(nasdaq_daily_1.update_date) AS max
           FROM nasdaq_daily nasdaq_daily_1))
UNION
 SELECT nasdaq_daily.bnw_symbol AS symbol,
    nasdaq_daily.update_date,
    nasdaq_daily.company_name,
    nasdaq_daily.last_sale,
    nasdaq_daily.net_change,
    nasdaq_daily.percent_change,
    nasdaq_daily.market_cap_m,
    nasdaq_daily.volume_t,
    nasdaq_daily.ipo_year,
    nasdaq_daily.country,
    nasdaq_daily.sector,
    nasdaq_daily.industry,
    nasdaq_daily.update_time
   FROM nasdaq_daily
  WHERE NOT (length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%WS'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%U'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%R'::text OR nasdaq_daily.company_name::text ~~* '%BENEFICIAL%'::text OR nasdaq_daily.company_name::text ~~* '%TRUST%'::text OR nasdaq_daily.company_name::text ~~* '%ETF'::text OR nasdaq_daily.company_name::text ~~* '% ETF %'::text OR nasdaq_daily.company_name::text ~~* '%PREFERRED%'::text OR nasdaq_daily.company_name::text ~~* '%NTS'::text OR nasdaq_daily.company_name::text ~~* '%WARRANT'::text OR nasdaq_daily.company_name::text ~~* '%UNIT'::text OR nasdaq_daily.company_name::text ~~* '%UNITS'::text OR nasdaq_daily.company_name::text ~~* '%FUND%'::text OR nasdaq_daily.company_name::text ~~* '%WTS'::text OR nasdaq_daily.company_name::text ~~* '%UTS'::text OR nasdaq_daily.company_name::text ~~* 'ABERDEEN%'::text OR nasdaq_daily.company_name::text ~~* 'ADVISOR%'::text OR nasdaq_daily.company_name::text ~~* '%DEBS'::text) AND nasdaq_daily.symbol::text ~ '^[^0-9]*$'::text AND nasdaq_daily.company_name::text ~ '^[^0-9]*$'::text AND nasdaq_daily.volume_t > 15 AND nasdaq_daily.last_sale > 0.85 AND nasdaq_daily.update_date = (( SELECT max(nasdaq_daily_1.update_date) AS max
           FROM nasdaq_daily nasdaq_daily_1))
UNION
 SELECT nasdaq_daily.zck_symbol AS symbol,
    nasdaq_daily.update_date,
    nasdaq_daily.company_name,
    nasdaq_daily.last_sale,
    nasdaq_daily.net_change,
    nasdaq_daily.percent_change,
    nasdaq_daily.market_cap_m,
    nasdaq_daily.volume_t,
    nasdaq_daily.ipo_year,
    nasdaq_daily.country,
    nasdaq_daily.sector,
    nasdaq_daily.industry,
    nasdaq_daily.update_time
   FROM nasdaq_daily
  WHERE NOT (length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%WS'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%U'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%R'::text OR nasdaq_daily.company_name::text ~~* '%BENEFICIAL%'::text OR nasdaq_daily.company_name::text ~~* '%TRUST%'::text OR nasdaq_daily.company_name::text ~~* '%ETF'::text OR nasdaq_daily.company_name::text ~~* '% ETF %'::text OR nasdaq_daily.company_name::text ~~* '%PREFERRED%'::text OR nasdaq_daily.company_name::text ~~* '%NTS'::text OR nasdaq_daily.company_name::text ~~* '%WARRANT'::text OR nasdaq_daily.company_name::text ~~* '%UNIT'::text OR nasdaq_daily.company_name::text ~~* '%UNITS'::text OR nasdaq_daily.company_name::text ~~* '%FUND%'::text OR nasdaq_daily.company_name::text ~~* '%WTS'::text OR nasdaq_daily.company_name::text ~~* '%UTS'::text OR nasdaq_daily.company_name::text ~~* 'ABERDEEN%'::text OR nasdaq_daily.company_name::text ~~* 'ADVISOR%'::text OR nasdaq_daily.company_name::text ~~* '%DEBS'::text) AND nasdaq_daily.symbol::text ~ '^[^0-9]*$'::text AND nasdaq_daily.company_name::text ~ '^[^0-9]*$'::text AND nasdaq_daily.volume_t > 15 AND nasdaq_daily.last_sale > 0.85 AND nasdaq_daily.update_date = (( SELECT max(nasdaq_daily_1.update_date) AS max
           FROM nasdaq_daily nasdaq_daily_1))
UNION
 SELECT nasdaq_daily.prn_symbol AS symbol,
    nasdaq_daily.update_date,
    nasdaq_daily.company_name,
    nasdaq_daily.last_sale,
    nasdaq_daily.net_change,
    nasdaq_daily.percent_change,
    nasdaq_daily.market_cap_m,
    nasdaq_daily.volume_t,
    nasdaq_daily.ipo_year,
    nasdaq_daily.country,
    nasdaq_daily.sector,
    nasdaq_daily.industry,
    nasdaq_daily.update_time
   FROM nasdaq_daily
  WHERE NOT (length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%WS'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%U'::text OR length(nasdaq_daily.symbol::text) >= 5 AND nasdaq_daily.symbol::text ~~ '%R'::text OR nasdaq_daily.company_name::text ~~* '%BENEFICIAL%'::text OR nasdaq_daily.company_name::text ~~* '%TRUST%'::text OR nasdaq_daily.company_name::text ~~* '%ETF'::text OR nasdaq_daily.company_name::text ~~* '% ETF %'::text OR nasdaq_daily.company_name::text ~~* '%PREFERRED%'::text OR nasdaq_daily.company_name::text ~~* '%NTS'::text OR nasdaq_daily.company_name::text ~~* '%WARRANT'::text OR nasdaq_daily.company_name::text ~~* '%UNIT'::text OR nasdaq_daily.company_name::text ~~* '%UNITS'::text OR nasdaq_daily.company_name::text ~~* '%FUND%'::text OR nasdaq_daily.company_name::text ~~* '%WTS'::text OR nasdaq_daily.company_name::text ~~* '%UTS'::text OR nasdaq_daily.company_name::text ~~* 'ABERDEEN%'::text OR nasdaq_daily.company_name::text ~~* 'ADVISOR%'::text OR nasdaq_daily.company_name::text ~~* '%DEBS'::text) AND nasdaq_daily.symbol::text ~ '^[^0-9]*$'::text AND nasdaq_daily.company_name::text ~ '^[^0-9]*$'::text AND nasdaq_daily.volume_t > 15 AND nasdaq_daily.last_sale > 0.85 AND nasdaq_daily.update_date = (( SELECT max(nasdaq_daily_1.update_date) AS max
           FROM nasdaq_daily nasdaq_daily_1));

ALTER TABLE public.base_min_vol_prc
    OWNER TO postgres;
COMMENT ON VIEW public.base_min_vol_prc
    IS 'Base for all Symbols derived from Nasdaq_daily.
Sy,bols with special character separators are included in all forms';