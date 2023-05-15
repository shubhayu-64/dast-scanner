import requests
from scanners import NMapScanner
from database.schemas import ScanResultsBase, ResultsBase
from database.crud import *
from datetime import datetime
from pprint import pprint


class TestClass:
    def __init__(self) -> None:
        self.baseUrl = 'http://localhost:5000/'
        self.testTarget = "https://public-firing-range.appspot.com"

    def ping_server(self):
        """Tests if the server is running
        """
        response = requests.get(self.baseUrl)
        try:
            assert response.status_code == 200
            print("Server is running")
        except AssertionError:
            print("Server is not running")

    def test_scan(self):
        """Tests the scan endpoint
        """
        response = requests.post(
            self.baseUrl + 'api/v1/scan', json={"target": self.testTarget, "canActiveScan": False})
        try:
            assert response.status_code == 200
            print(response.json())
            print("Scan endpoint is working")
        except AssertionError:
            print("Scan endpoint is not working")

    def test_nmap(self):
        scanner = NMapScanner()
        scanner.scan()
        scanner.read_scan_results()

    def test_write_db(self):
        """Tests the database
        """

        scanId = Database.fetch_scan_count() + 1
        print(scanId)
        data = ScanResultsBase(
            scan_id=scanId, scan_time=datetime.now(), results=ResultsBase(nmap_results={"nmap_test": "test_result"}))

        response = Database.create_scan_result(data)
        pprint(response)

    def test_read_db(self):
        """Tests the database
        """
        response = Database.read_all_scan_results()
        pprint(response)

    def run_tests(self):
        """Runs all tests
        """
        # self.ping_server()
        # time.sleep(5)
        # self.test_nmap()
        self.test_write_db()
        self.test_read_db()


if __name__ == '__main__':
    print("Starting Tests")
    test = TestClass()
    test.run_tests()
    print("Tests Completed")
