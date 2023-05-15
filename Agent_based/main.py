from scanners import NMapScanner, ClamAVScanner
from database import ScanResultsBase, ResultsBase, Database
from datetime import datetime


class AgentBasedScanner:
    def __init__(self):
        self.nmapScanner = NMapScanner()
        self.clamavScanner = ClamAVScanner()
        self.havocScanner = None
        self.db = Database()

    def scan(self):
        # Start NMap Scan
        nmapScanResponse = self.nmapScanner.scan()

        # Start ClamAV Scan
        print(self.clamavScanner.ping())
        print(self.clamavScanner.reload())
        # self.clamavScanner.scan_directory()

    def save_scan_results(self):
        # Save the scan results to a file
        nmap_results = self.nmapScanner.get_scan_results()
        # clamav_results = self.clamavScanner.get_scan_results()

        results = ResultsBase(
            nmap_results=nmap_results,
            clamav_results=None,
            havoc_results=None
        )

        scanId = self.db.fetch_scan_count() + 1

        scanData = ScanResultsBase(
            scan_id=scanId, scan_time=datetime.now(), results=results)

        response = self.db.create_scan_result(scanData)
        print(response)


def main():
    agentScanner = AgentBasedScanner()
    agentScanner.scan()
    agentScanner.save_scan_results()


if __name__ == '__main__':
    main()
