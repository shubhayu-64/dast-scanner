from . import models, schemas
from .database import SessionLocal, engine, Base


class Database:
    def __init__(self) -> None:
        models.Base.metadata.create_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def create_scan_result(self, scan_result: schemas.ScanResultsBase):
        db_scan_result = models.ScanResult(
            scan_id=scan_result.scan_id,
            scan_time=scan_result.scan_time,
            results=scan_result.results,
        )
        self.db.add(db_scan_result)
        self.db.commit()
        self.db.refresh(db_scan_result)
        return db_scan_result

    def read_all_scan_results(self):
        return self.db.query(models.ScanResult).all()

    def read_scan_result(self, scan_id: int):
        return self.db.query(models.ScanResult).filter(models.ScanResult.scan_id == scan_id).first()

    def fetch_latest_scan_id(self):
        return self.db.query(models.ScanResult).order_by(models.ScanResult.scan_time.desc()).first().scan_id

    def fetch_scan_count(self):
        return self.db.query(models.ScanResult).count()
