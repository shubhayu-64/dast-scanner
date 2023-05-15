from pydantic import BaseModel
from datetime import datetime


class ResultsBase(BaseModel):
    nmap_results: dict = None
    clamav_results: dict = None
    havoc_results: dict = None

    def to_dict(self):
        return {
            'nmap_results': self.nmap_results,
            'clamav_results': self.clamav_results,
            'havoc_results': self.havoc_results
        }


class ScanResultsBase(BaseModel):
    scan_id: int
    scan_time: datetime
    results: ResultsBase
