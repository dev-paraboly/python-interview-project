import psycopg2
import os
from psycopg2 import pool, sql
from typing import List
from src.utils import AddFormatterToQuery
from .model import TicketType


class QueryFactory:
    def __init__(self):
        pass

    def get_tuple_params(self, param):
        return (param, tuple(param) if type(param) == list else tuple([None]))

    @AddFormatterToQuery(["stop_id", "line_id", "ridership", "stop_name", "direction", "stop_order", "latitude", "longitude"])
    def get_stop_ridership_report(self,
        dates: List[str],
        stops: List[str],
        lines: List[int],
        tickets: List[TicketType],
        start_time: str,
        end_time: str,
        preview: bool = True,
    ):
        inner_query = """
            SELECT
                "BOARDING",
                "LINE_NO" * 10 + "SUB_LINE_NO" ulid,
                count(*) usage
            FROM mock_schema.sc_with_stops_trips
                WHERE "BOARDING"<>'-1'
                    AND (%s is null or date IN %s)
                    AND (%s is null or "TICKET_TYPE" in %s)
                    AND (%s is null or time::time < %s)
                    AND (%s is null or time::time > %s)
                GROUP BY "BOARDING", "LINE_NO", "SUB_LINE_NO"
            {0}
        """.format("LIMIT 5" if preview else "")

        main_query = """
            SELECT
               stop_id,
               line_id,
               coalesce(usage, 0) as usage,
               stop_name,
               direction,
               stop_order,
               latitude,
               longitude
            FROM mock_schema.stop_seq
            FULL JOIN (
                {0}
            )analysis
            ON analysis."BOARDING"=stop_seq.stop_id AND analysis.ulid=stop_seq.line_id
            WHERE
                (%s is null or "line_id" in %s)
                AND (%s is null or "stop_id" in %s)
            ORDER BY usage
            {1}
        """.format(inner_query, "LIMIT 5" if preview else "")

        params = (
            *self.get_tuple_params(dates),
            *self.get_tuple_params(tickets),
            start_time, start_time,
            end_time, end_time,
            *self.get_tuple_params(lines),
            *self.get_tuple_params(stops),
        )
        return [sql.SQL(main_query), params]

    @AddFormatterToQuery(["ticket_type", "ridership"])
    def ridership_by_ticket_type(self,
        dates: List[str],
        lines: List[int],
        stops: List[str],
        preview: bool = True
    ):
        query = """
            SELECT islem_tipi, count(*) FROM mock_schema.ulasim_veri
            WHERE (%s is null or timestamp::date IN %s)
                AND (%s is null or hat_no * 10 + alt_hat_no IN %s)
            GROUP BY islem_tipi
        """

        params = (
            *self.get_tuple_params(dates),
            *self.get_tuple_params(lines),
        )
        return [query, params]

    @AddFormatterToQuery(["ulid", "ridership"])
    def ridership_by_lines(self,
        dates: List[str],
        stops: List[str],
        ticket_type: List[TicketType],
        preview: bool = True
    ):
        if (preview): dates = ["2019-04-10"]
        query = """
            SELECT
                hat_no * 10 + alt_hat_no as ulid,
                count(*) as ridership
            FROM mock_schema.ulasim_veri
            WHERE (%s is null or timestamp::date IN %s)
                AND (%s is null or islem_tipi IN %s)
            GROUP BY hat_no, alt_hat_no
        """.format("LIMIT 5" if preview else "")

        params = (
            *self.get_tuple_params(dates),
            *self.get_tuple_params(ticket_type),
        )

        return [query, params]