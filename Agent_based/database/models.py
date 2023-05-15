from sqlalchemy import Column, String, DateTime, Text, Integer
import json

from .database import Base


class ScanResult(Base):
    __tablename__ = "scan_results"

    scan_id = Column(Integer, primary_key=True)
    scan_time = Column(DateTime)
    results = Column(Text)

    def __init__(self, scan_id, scan_time, results):
        self.scan_id = scan_id
        self.scan_time = scan_time
        self.results = json.dumps(results.to_dict())

    def to_dict(self):
        return {
            'scanId': self.scanId,
            'scanTime': self.scanTime,
            'results': json.loads(self.results)
        }

    def __repr__(self):
        return f"<ScanResult(scan_id={self.scan_id}, scan_time={self.scan_time}, results={self.results})>"
