from fastapi import APIRouter, HTTPException, Query, Depends, Path, Response
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict, Union, Any, Optional

from .service import report_service
from .model import ReportParams
from .utils import ReturnsDataframeAsJson

router = APIRouter()

@router.get('/stop/ridership')
@ReturnsDataframeAsJson
def _(report_params: ReportParams = Depends()):
    '''Get ridership report based on given query parameters'''
    return report_service.get_stop_ridership_report(report_params)

@router.get("/ticket-distribution")
@ReturnsDataframeAsJson
def _(report_params: ReportParams = Depends()):
    '''Get ridership by ticket types'''
    return report_service.get_ridership_by_tickets(report_params)

@router.get("/line/ridership")
def _(report_params: ReportParams = Depends()):
    '''Get ridership by line'''
    return report_service.get_line_ridership(report_params)
