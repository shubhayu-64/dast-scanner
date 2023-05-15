from datetime import datetime
from config import Config
import nmap
import shutil
import json
import os

import xmltodict


class NMapScanner:
    def __init__(self):
        # Check if script is run as root
        assert os.geteuid() == 0, "This script must be run as root"

        # Check if nmap is installed
        assert shutil.which(
            "nmap") is not None, "Nmap is not installed on your system."

        self.target = Config().target
        now = datetime.now()
        self.filename = Config().scan_results_directory + \
            f"/nmap_scan_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"
        self.nm = nmap.PortScanner()

    def scan(self):
        # Scans the target with nmap
        # -sV : Probe open ports to determine service/version info
        # -O : Enable OS detection
        # -p- : Scan all ports
        # -sC : Scan with default NSE scripts
        # -vv : Verbose output
        # --script=vuln : Run NSE scripts against found services
        print("Starting Nmap scan...")
        # self.nm.scan(hosts=self.target,
        #              arguments='-sV -O -p- -sC -vv --script=vuln')
        self.nm.scan(hosts=self.target,
                     arguments='-sV -O -p- -sC -vv --script=vuln')
        return self.nm.scanstats()

    def save_scan_results(self):
        # Saves the scan results to a json file
        if os.path.exists(Config().scan_results_directory):
            with open(self.filename, 'w') as outfile:
                xml_output = self.nm.get_nmap_last_output().decode('utf-8')
                dict_output = xmltodict.parse(xml_output)
                json.dump(dict_output, outfile)

        else:
            os.mkdir(Config().scan_results_directory)
            self.save_scan_results()

    def get_scan_results(self):
        # Fetches the scan results
        xml_output = self.nm.get_nmap_last_output().decode('utf-8')
        dict_output = xmltodict.parse(xml_output)
        return dict_output
