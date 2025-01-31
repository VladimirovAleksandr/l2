from django.db import connection
from laboratory.settings import TIME_ZONE
from utils.db import namedtuplefetchall


def monitoring_sql_by_all_hospital(
    monitoring_research=None,
    type_period=None,
    period_param_hour=None,
    period_param_day=None,
    period_param_month=None,
    period_param_quarter=None,
    period_param_halfyear=None,
    period_param_year=None,
    period_param_week_date_start=None,
    period_param_week_date_end=None,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                hospitals_hospitals.short_title,
                directions_monitoringresult.hospital_id,
                directions_monitoringresult.napravleniye_id,
                directions_monitoringresult.issledovaniye_id,
                to_char(directions_issledovaniya.time_confirmation AT TIME ZONE %(tz)s, 'DD.MM.YYYY HH24:MI') as confirm,
                directions_monitoringresult.research_id,
                directions_monitoringresult.group_id,
                directory_paraclinicinputgroups.title as group_title,
                directory_paraclinicinputgroups.order as group_order,
                directions_monitoringresult.field_id,
                directory_paraclinicinputfield.title as field_title,
                directory_paraclinicinputfield.order as field_order,
                directions_monitoringresult.field_type,
                directions_monitoringresult.value_aggregate,
                directions_monitoringresult.value_text,
                directions_monitoringresult.type_period,
                directions_monitoringresult.period_param_hour,
                directions_monitoringresult.period_param_day,
                directions_monitoringresult.period_param_week_description,
                directions_monitoringresult.period_param_week_date_start,
                directions_monitoringresult.period_param_week_date_end,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_quarter,
                directions_monitoringresult.period_param_halfyear,
                directions_monitoringresult.period_param_year
            FROM directions_monitoringresult
            LEFT JOIN directory_paraclinicinputgroups
            ON directory_paraclinicinputgroups.id = directions_monitoringresult.group_id
            LEFT JOIN directory_paraclinicinputfield
            ON directory_paraclinicinputfield.id = directions_monitoringresult.field_id
            LEFT JOIN hospitals_hospitals
            ON hospitals_hospitals.id = directions_monitoringresult.hospital_id
            LEFT JOIN directions_issledovaniya
            ON directions_issledovaniya.id = directions_monitoringresult.issledovaniye_id
            WHERE
            CASE 
            WHEN %(type_period)s = 'PERIOD_HOUR' THEN 
                directions_monitoringresult.type_period = 'PERIOD_HOUR' AND
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_hour=%(period_param_hour)s  AND
                directions_monitoringresult.period_param_day=%(period_param_day)s  AND
                directions_monitoringresult.period_param_month=%(period_param_month)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            WHEN %(type_period)s = 'PERIOD_DAY' THEN
                directions_monitoringresult.type_period = 'PERIOD_DAY' AND
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_day=%(period_param_day)s  AND
                directions_monitoringresult.period_param_month=%(period_param_month)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            WHEN %(type_period)s = 'PERIOD_WEEK' THEN 
                directions_monitoringresult.type_period = 'PERIOD_WEEK' AND
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_monitoringresult.period_param_week_date_start=%(period_param_week_date_start)s AND
                directions_monitoringresult.period_param_week_date_end=%(period_param_week_date_end)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            WHEN %(type_period)s = 'PERIOD_MONTH' THEN 
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_month=%(period_param_month)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            WHEN %(type_period)s = 'PERIOD_QUARTER' THEN 
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_quarter=%(period_param_quarter)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            WHEN %(type_period)s = 'PERIOD_HALFYEAR' THEN 
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_halfyear=%(period_param_halfyear)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            WHEN %(type_period)s = 'PERIOD_YEAR' THEN 
                directions_monitoringresult.research_id=%(monitoring_research)s AND
                directions_monitoringresult.period_param_year=%(period_param_year)s AND
                directions_issledovaniya.time_confirmation is NOT NULL
            END 
                
            ORDER BY hospital_id, directions_monitoringresult.napravleniye_id, group_order, field_order
            """,
            params={
                'tz': TIME_ZONE,
                'monitoring_research': monitoring_research,
                'type_period': type_period,
                'period_param_hour': period_param_hour,
                'period_param_day': period_param_day,
                'period_param_month': period_param_month,
                'period_param_quarter': period_param_quarter,
                'period_param_halfyear': period_param_halfyear,
                'period_param_year': period_param_year,
                'period_param_week_date_start': period_param_week_date_start,
                'period_param_week_date_end': period_param_week_date_end,
            },
        )
        rows = namedtuplefetchall(cursor)
    return rows


def dashboard_sql_by_day(charts_id=None, start_date=None, end_date=None):
    # в разрезе По всем МО за даты
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
            DISTINCT ON (
                directions_dashboardcharts.id,
                directions_monitoringresult.hospital_id,
                directions_dashboardchartfields.order,
                directions_dashboardchartfields.field_id,
                directions_monitoringresult.period_param_day,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_year
            )
            
                directions_dashboardcharts.id as chart_id,
                directions_dashboardcharts.order as chart_order,
                directions_dashboardcharts.title as chart_title,
                directions_dashboardcharts.default_type as default_type,
                directions_dashboardcharts.is_full_width as is_full_width,
                directions_monitoringresult.hospital_id,
                hospitals_hospitals.short_title as hosp_short_title,
                hospitals_hospitals.title as hosp_title,
                directions_dashboardchartfields.order as order_field, 
                directions_dashboardchartfields.field_id,
                title_for_field,
                directory_paraclinicinputfield.title as field_title,
                directions_monitoringresult.value_aggregate,
                directions_monitoringresult.period_param_hour,
                directions_monitoringresult.period_param_day,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_year,
                directions_monitoringresult.period_date as date
                
            
            FROM public.directions_dashboardchartfields
            LEFT JOIN directions_dashboardcharts
            ON directions_dashboardcharts.id = directions_dashboardchartfields.charts_id
            
            LEFT JOIN directory_paraclinicinputfield
            ON directory_paraclinicinputfield.id = directions_dashboardchartfields.field_id
            
            LEFT JOIN directions_monitoringresult
            ON directions_monitoringresult.field_id = directions_dashboardchartfields.field_id
            
            LEFT JOIN hospitals_hospitals
            ON hospitals_hospitals.id = directions_monitoringresult.hospital_id

            WHERE
                directions_dashboardcharts.id = ANY(ARRAY[%(charts_id)s]) AND 
                directions_monitoringresult.period_date
                BETWEEN %(start_date)s::date
                AND
                %(end_date)s::date

            ORDER BY
                directions_dashboardcharts.id, 
                directions_monitoringresult.hospital_id,
                directions_monitoringresult.period_param_year,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_day,
                directions_dashboardchartfields.order,
                directions_dashboardchartfields.field_id,
                directions_monitoringresult.period_param_hour DESC                
            """,
            params={
                'tz': TIME_ZONE,
                'charts_id': charts_id,
                'start_date': start_date,
                'end_date': end_date,
            },
        )
        rows = namedtuplefetchall(cursor)
    return rows


def dashboard_sql_by_day_filter_hosp(charts_id=None, start_date=None, end_date=None, filter_hospitals=None):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
            DISTINCT ON (
                directions_dashboardcharts.id,
                directions_monitoringresult.hospital_id,
                directions_dashboardchartfields.order,
                directions_dashboardchartfields.field_id,
                directions_monitoringresult.period_param_day,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_year
            )

                directions_dashboardcharts.id as chart_id,
                directions_dashboardcharts.order as chart_order,
                directions_dashboardcharts.title as chart_title,
                directions_dashboardcharts.default_type as default_type,
                directions_dashboardcharts.is_full_width as is_full_width,
                directions_monitoringresult.hospital_id,
                hospitals_hospitals.short_title as hosp_short_title,
                hospitals_hospitals.title as hosp_title,
                directions_dashboardchartfields.order as order_field, 
                directions_dashboardchartfields.field_id,
                title_for_field,
                directory_paraclinicinputfield.title as field_title,
                directions_monitoringresult.value_aggregate,
                directions_monitoringresult.period_param_hour,
                directions_monitoringresult.period_param_day,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_year,
                directions_monitoringresult.period_date as date

            FROM public.directions_dashboardchartfields
            LEFT JOIN directions_dashboardcharts
            ON directions_dashboardcharts.id = directions_dashboardchartfields.charts_id

            LEFT JOIN directory_paraclinicinputfield
            ON directory_paraclinicinputfield.id = directions_dashboardchartfields.field_id

            LEFT JOIN directions_monitoringresult
            ON directions_monitoringresult.field_id = directions_dashboardchartfields.field_id

            LEFT JOIN hospitals_hospitals
            ON hospitals_hospitals.id = directions_monitoringresult.hospital_id

            WHERE
                directions_dashboardcharts.id = ANY(ARRAY[%(charts_id)s]) AND 
                directions_monitoringresult.hospital_id = ANY(ARRAY[%(filter_hospitals)s]) AND  
                directions_monitoringresult.period_date
                BETWEEN %(start_date)s::date
                AND
                %(end_date)s::date
            ORDER BY 
                directions_dashboardcharts.id, 
                directions_monitoringresult.hospital_id,
                directions_dashboardchartfields.order,
                directions_dashboardchartfields.field_id,
                directions_monitoringresult.period_param_day,
                directions_monitoringresult.period_param_month,
                directions_monitoringresult.period_param_year,
                directions_monitoringresult.period_param_hour DESC               
            """,
            params={
                'tz': TIME_ZONE,
                'charts_id': charts_id,
                'filter_hospitals': filter_hospitals,
                'start_date': start_date,
                'end_date': end_date,
            },
        )
        rows = namedtuplefetchall(cursor)
    return rows

