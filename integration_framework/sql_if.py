from django.db import connection

from laboratory.settings import TIME_ZONE


def direction_collect(d_s, researches, is_research, limit):
    """
    парам: d_s - date-start, researches - списко исследований которые требуются

    Вернуть:
    Направления, в к-рых все исследования подтверждены, и подтверждены после определенной даты

    в SQL:
    t_iss - это временная таблица запроса для направлений в к-рых есть подтвержденные исследований (Направления уникальны)
    t_iss_null - это временная таблица запроса направлений, у к-рых есть неподтвержденные исследования
    t_all - это готовая выборка направлений, где подтверждены ВСЕ исследования в определенном направлении
    SELECT research_id FROM integration_framework_integrationresearches WHERE
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """WITH
        t_iss AS 
            (SELECT distinct on (napravleniye_id) napravleniye_id, research_id, time_confirmation AT TIME ZONE %(tz)s AS time_confirmation,
             to_char(directions_issledovaniya.time_confirmation AT TIME ZONE %(tz)s, 'YYYY-MM-DD HH24:MI:SS.US') AS t_confirm
             FROM public.directions_issledovaniya
             WHERE
             CASE 
             WHEN %(is_research)s = -1 THEN
                 time_confirmation > %(d_start)s::timestamp AT TIME ZONE %(tz)s
             ELSE
                 time_confirmation > %(d_start)s::timestamp AT TIME ZONE %(tz)s AND (research_id=ANY(ARRAY[%(researches)s]))
             END
             order by napravleniye_id),
        t_iss_null AS
            (SELECT distinct on (napravleniye_id) napravleniye_id as napr_null FROM public.directions_issledovaniya
                   WHERE time_confirmation is null 
            order by napravleniye_id),
        t_all AS 
            (SELECT * FROM t_iss LEFT JOIN t_iss_null ON t_iss.napravleniye_id = t_iss_null.napr_null)
            
            SELECT napravleniye_id, research_id, time_confirmation, t_confirm FROM t_all WHERE napr_null IS NULL
            ORDER BY time_confirmation LIMIT %(limit)s """,
            params={'d_start': d_s if str(d_s) != 'None' else '2018-01-01', 'tz': TIME_ZONE, 'researches': researches, 'is_research': is_research, 'limit': limit},
        )

        row = cursor.fetchall()
    return row


def direction_resend_amd(limit):
    """
    Вернуть:
    Направления, в к-рых все исследования подтверждены, и подтверждены после определенной даты
    в SQL:
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
        SELECT id FROM public.directions_napravleniya
            WHERE need_resend_amd = True
            ORDER BY id DESC LIMIT %(limit)s """,
            params={'limit': limit},
        )

        row = cursor.fetchall()
    return row


def direction_resend_n3(limit):
    """
    Вернуть:
    Направления, в к-рых все исследования подтверждены, и подтверждены после определенной даты
    в SQL:
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
        SELECT id FROM public.directions_napravleniya
            WHERE need_resend_n3 = True
            ORDER BY id DESC LIMIT %(limit)s """,
            params={'limit': limit},
        )

        row = cursor.fetchall()
    return row


def direction_resend_l2(limit):
    """
    Вернуть:
    Направления, в к-рых все исследования подтверждены, и подтверждены после определенной даты
    в SQL:
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
        SELECT id FROM public.directions_napravleniya
            WHERE need_resend_l2 = True
            ORDER BY id DESC LIMIT %(limit)s """,
            params={'limit': limit},
        )

        row = cursor.fetchall()
    return row


def direction_resend_crie(limit):
    """
    Вернуть:
    Направления, в к-рых все исследования подтверждены, и подтверждены после определенной даты
    в SQL:
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
        SELECT id FROM public.directions_napravleniya
            WHERE need_resend_crie = True
            ORDER BY id DESC LIMIT %(limit)s """,
            params={'limit': limit},
        )

        row = cursor.fetchall()
    return row
