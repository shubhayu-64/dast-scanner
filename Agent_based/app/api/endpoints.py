from fastapi import APIRouter
from scanners import OWASPScanner
from app.models import ScanModel

scanRouter = APIRouter()


@scanRouter.post("/scan")
async def scan(targetDetails: ScanModel):
    print("Scanning: " + targetDetails.target)
    result = {"Scan Results": {}}

    owasp_scanner = OWASPScanner(targetDetails.target)
    spiderResults = owasp_scanner.spider()
    result["Scan Results"]["spider_results"] = spiderResults

    if targetDetails.canActiveScan:
        activeScanResults = OWASPScanner.active_scan()
        result["Scan Results"]["active_scan_results"] = activeScanResults

    return result
