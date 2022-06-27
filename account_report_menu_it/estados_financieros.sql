CREATE OR REPLACE FUNCTION public.get_eeff(
	date_from date,
	date_to date,
	company_id integer)
    RETURNS TABLE(rubro_id integer, balance numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
	RETURN QUERY 

select a4.id as rubro_id,sum(a1.balance) as balance
from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
left join account_account a3 on a3.id=a1.account_id
left join account_type_it a4 on a4.id=a3.account_type_it_id
where 
(a2.date between $1 and $2) 
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.company_id=$3
group by a4.id
order by a4.id;
  END;
$BODY$;

-------------------------------------------------------------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS public.get_sumas_mayor_f1(date, date, integer) CASCADE;

CREATE OR REPLACE FUNCTION public.get_sumas_mayor_f1(
	date_from date,
	date_to date,
	company_id integer)
    RETURNS TABLE(account_id integer, debe numeric, haber numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
	RETURN QUERY 

select a1.account_id,sum(a1.debit) as debe,sum(a1.credit) as haber
from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
where 
(a2.date between $1 and $2) 
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.company_id=$3
group by a1.account_id;
  END;
$BODY$;
-----------------------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS public.get_sumas_balance_f1(date, date, integer) CASCADE;

CREATE OR REPLACE FUNCTION public.get_sumas_balance_f1(
	date_from date,
	date_to date,
	company_id integer)
    RETURNS TABLE(account_id integer, debe numeric, haber numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
	RETURN QUERY 

select a4.id as account_id,sum(a1.debit) as debe,sum(a1.credit) as haber
from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
left join account_account a3 on a3.id=a1.account_id
left join account_group a4 on a4.id=a3.group_id
where 
(a2.date between $1 and $2) 
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.company_id=$3
group by a4.id;
  END;
$BODY$;
--------------------------------------------------------------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS public.get_sumas_mayor_f2(date, date, integer) CASCADE;

CREATE OR REPLACE FUNCTION public.get_sumas_mayor_f2(
	date_from date,
	date_to date,
	company_id integer)
    RETURNS TABLE(account_id integer, si_debe numeric, si_haber numeric, debe numeric, haber numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
	RETURN QUERY 

select b1.account_id,coalesce(b2.si_debe,0) as si_debe,coalesce(b2.si_haber,0) as si_haber,
coalesce(b3.debe,0) as debe,coalesce(b3.haber,0) as haber from
(
select distinct a1.account_id from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
where (a2.date between $1 and $2)
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.company_id=$3
)b1

left join 
(
select a1.account_id,sum(a1.debit) as si_debe,sum(a1.credit) as si_haber from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
where a2.date=$1
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.is_opening_close=TRUE
and a2.company_id=$3
group by a1.account_id
)b2 on b2.account_id=b1.account_id

left join 
(
select a1.account_id,sum(a1.debit) as debe,sum(a1.credit) as haber from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
where (a2.date between  $1 and $2)
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.is_opening_close<>TRUE
and a2.company_id=$3
group by a1.account_id
)b3 on b3.account_id=b1.account_id;
  END;
$BODY$;

--------------------------------------------------------------------------------------------------------------------------------------------

-- FUNCTION: public.get_sumas_balance_f2(date, date, integer)

DROP FUNCTION IF EXISTS public.get_sumas_balance_f2(date, date, integer) CASCADE;

CREATE OR REPLACE FUNCTION public.get_sumas_balance_f2(
	date_from date,
	date_to date,
	company_id integer)
    RETURNS TABLE(account_id integer, si_debe numeric, si_haber numeric, debe numeric, haber numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
	RETURN QUERY 

select b1.account_id,coalesce(b2.si_debe,0) as si_debe,coalesce(b2.si_haber,0) as si_haber,
coalesce(b3.debe,0) as debe,coalesce(b3.haber,0) as haber from
(
select distinct a4.id as account_id from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
left join account_account a3 on a3.id=a1.account_id
left join account_group a4 on a4.id=a3.group_id
where (a2.date between $1 and $2)  -- aca va la fecha inicial y finnal 
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.company_id=$3
)b1

left join 
(
select a4.id as account_id,sum(a1.debit) as si_debe,sum(a1.credit) as si_haber from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
left join account_account a3 on a3.id=a1.account_id
left join account_group a4 on a4.id=a3.group_id
where a2.date=$1--  esta es la fecha inicial 
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.is_opening_close=TRUE
and a2.company_id=$3
group by a4.id
)b2 on b2.account_id=b1.account_id

left join 
(
select a4.id as account_id,sum(a1.debit) as debe,sum(a1.credit) as haber from account_move_line a1
left join account_move a2 on a2.id=a1.move_id
left join account_account a3 on a3.id=a1.account_id
left join account_group a4 on a4.id=a3.group_id

where (a2.date between  $1 and $2)--  aca va la fecha inicial y la final 
and a1.display_type is null 
and a1.account_id is not null
and a2.state='posted'
and a2.is_opening_close<>TRUE
and a2.company_id=$3
group by a4.id
)b3 on b3.account_id=b1.account_id;
  END;
$BODY$;
-------------------------------------------------------------------------------------------------------------------------

DROP FUNCTION IF EXISTS public.get_efective_flow(character varying,character varying,character varying, integer) CASCADE;

CREATE OR REPLACE FUNCTION public.get_efective_flow(
	periodo_ini character varying,
	periodo_fin character varying,
	period_saldo_inicial character varying,
	company integer)
    RETURNS TABLE(name character varying, efective_group character varying, total numeric, efective_order integer) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
BEGIN

RETURN QUERY

SELECT T.* FROM (SELECT aet.name, aet.group as efective_group, SUM(aml.balance)*-1 as total, aet.order as efective_order FROM account_move_line aml
LEFT JOIN account_account aa ON aa.id = aml.account_id
LEFT JOIN account_efective_type aet ON aet.id = aa.account_type_cash_id
WHERE LEFT(aa.code,2) <> '10' AND aa.account_type_cash_id IS NOT NULL AND aml.move_id in (
SELECT
DISTINCT ON (aml.move_id) move_id
FROM account_move_line aml
LEFT JOIN account_account aa ON aa.id = aml.account_id
LEFT JOIN account_move am ON am.id = aml.move_id
WHERE am.state = 'posted' AND am.company_id = $4 AND aml.display_type IS NULL AND am.is_opening_close <> TRUE
AND (am.date BETWEEN $1::date AND $2::date)
AND LEFT(aa.code,2) = '10')
GROUP BY aet.name, aet.group, aet.order

UNION ALL

SELECT 'Saldo EFECT y EQUIV de EFECT al inicio del Ejercicio' as name, 'E7' as efective_group, SUM(aml.balance) as total, -1 as efective_order FROM account_move_line aml
LEFT JOIN account_account aa ON aa.id = aml.account_id
LEFT JOIN account_move am ON am.id = aml.move_id
LEFT JOIN account_efective_type aet ON aet.id = aa.account_type_cash_id
WHERE LEFT(aa.code,2) = '10' AND am.state = 'posted' AND aml.company_id = $4 AND aml.display_type IS NULL
AND (CASE
		WHEN am.is_opening_close = true AND to_char(am.date::timestamp with time zone, 'mmdd'::text) = '0101'::text THEN to_char(am.date::timestamp with time zone, 'yyyy'::text) || '00'::text
		WHEN am.is_opening_close = true AND to_char(am.date::timestamp with time zone, 'mmdd'::text) = '1231'::text THEN to_char(am.date::timestamp with time zone, 'yyyy'::text) || '13'::text
		ELSE to_char(am.date::timestamp with time zone, 'yyyymm'::text)
	END = $3)
				)T
ORDER BY T.efective_order;

END;
$BODY$;