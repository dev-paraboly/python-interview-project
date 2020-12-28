from typing import Dict, Callable
import pandas as pd
from io import BytesIO
from datetime import datetime

from src.db import DBModel
from .model import ReportParams
from .queries import QueryFactory

from src.utils import Utils


class _ReportService:
    def __init__(self):
        self.DB = DBModel.getInstance()
        self.Factory = QueryFactory()
        self.datetime_format = '%d-%m-%Y'
    
    def get_stop_ridership_report(self, params: ReportParams):
        report_as_dict = self.DB.run(
            self.Factory.get_stop_ridership_report(
                params.date,
                params.stop,
                params.line,
                params.ticket,
                params.start_hour,
                params.end_hour,
                params.preview,
            )
        )
        report_as_df = pd.DataFrame(report_as_dict)
        if (params.preview):
            report_as_df["ridership"] = "-"
        else:
            report_as_df = pd.DataFrame(report_as_df)
            ridership_sum = report_as_df["ridership"].sum()
            report_as_df = report_as_df.append({"line_id": "Toplam Biniş", "ridership": ridership_sum}, ignore_index=True)
        return report_as_df.fillna("")

    def get_ridership_by_tickets(self, params: ReportParams):
        riderships = self.DB.run(
            self.Factory.ridership_by_ticket_type(params.date, params.line, params.stop, params.preview)
        )
        ridership_df = pd.DataFrame(riderships)
        ridership_sum = ridership_df["ridership"].sum()
        ridership_df = ridership_df.append({"ticket_type": "Toplam Biniş", "ridership": ridership_sum}, ignore_index=True)
        return ridership_df.fillna("")

    def get_line_ridership(self, params: ReportParams):
        riderships = self.DB.run(
            self.Factory.ridership_by_lines(params.date, params.stop, params.ticket, params.preview)
        )
        return riderships

report_service = _ReportService()