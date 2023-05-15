from pydantic import BaseModel, HttpUrl


class ScanModel(BaseModel):
    target: HttpUrl
    canActiveScan: bool = False
