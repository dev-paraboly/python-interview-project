from functools import wraps
import pandas as pd
from io import BytesIO
from fastapi import Response
import json

def ReturnsDataframeAsExcel(func):
    @wraps(func)
    def formatter(*args, **kwargs):
        report_as_df = func(*args, **kwargs)
        in_memory_fp = BytesIO()
        report_as_df.to_excel(in_memory_fp)
        in_memory_fp.seek(0,0)
        data_buffer = in_memory_fp.read()
        return Response(content=data_buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return formatter

def ReturnsDataframeAsJson(func):
    @wraps(func)
    def formatter(*args, **kwargs):
        report_as_df = func(*args, **kwargs)
        as_json = report_as_df.to_json(orient="records")
        return json.loads(as_json)
    return formatter
