from bs4 import BeautifulSoup
from pprint import pprint
import json
import os
import urllib.request
import tarfile
from database import create_user
from models import User
from datetime import datetime

# Local Username for the database
localUsername = "local"


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def dict_to_json_file(my_dict, filename):
    """Write a dictionary to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(my_dict, file)


def verify_zap_running():
    """_summary_: Verify if ZAP is running.
    """

    try:
        response = urllib.request.urlopen('http://localhost:8080')
        # print(response.status)
        print("ZAP is running.")
        return True
    except urllib.error.URLError:
        print("ZAP is not running. Please start ZAP and try again.")
        return False


def verify_local_database():
    print("Verifying local database...")
    user = User(userId=localUsername)
    try:
        create_user(user)
        print("Local database created successfully.")
    except Exception as e:
        print("Local database already exists.")


def verify_zap_exists():
    """_summary_: Download ZAP.
    """
    filename = "ZAP_2.12.0_Linux.tar.gz"
    extractDir = "ZAP_2.12.0"
    zapDirname = "zap"

    if os.path.exists(os.path.join(".", zapDirname)):
        print("ZAP package already exists in current directory.")
    else:
        print("ZAP package not found in current directory. Downloading...")
        url = "https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz"
        urllib.request.urlretrieve(url, filename)
        print("Download complete.")

        print("Extracting ZAP package...")
        tar = tarfile.open(filename, "r:gz")
        tar.extractall()
        tar.close()
        print("Extraction complete.")

        print("Renaming directory...")
        os.rename(os.path.join(".", extractDir),
                  os.path.join(".", zapDirname))
        print("Renaming complete.")

        print("Deleting tar.gz file...")
        os.remove(filename)
        print("Deletion complete.")

        print("ZAP package downloaded and extracted successfully.")


def parse_zap_report(filename):
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # find all vulnerabilities in the report
    vulnSummary = soup.find_all('table', {'class': ['summary']})
    vulnAlerts = soup.find_all('table', {'class': ['alerts']})
    vulnResults = soup.find_all('table', {'class': ['results']})

    # create a dictionary to store the vulnerabilities and their details
    result = []
    for data in vulnResults:
        headers = [th.text.strip() for th in data.find_all('th')]
        body = [td.text.strip() for td in data.find_all('td')]
        pprint(headers)
        type = headers[0]
        title = headers[1]
        # details = {body[i]: body[i+1] for i in range(0, len(body), 2)}

        # pprint(len(body))
        print(body)
        # result.append(data)
        break

    return result


def extract_zap_vulnerabilities(html_file_path):
    with open(html_file_path) as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Find the table containing vulnerability information
        table = soup.find('table', {'id': 'sitesTable'})

        # Extract the table headers
        headers = [th.text.strip() for th in table.find_all('th')]

        # Extract the vulnerability information
        vulnerabilities = []
        for tr in table.find_all('tr')[1:]:
            row = [td.text.strip() for td in tr.find_all('td')]
            vulnerability = dict(zip(headers, row))
            vulnerabilities.append(vulnerability)

        return vulnerabilities


def parse_basic_result(filename: str):
    if not os.path.exists(filename):
        print("File not found")
        raise Exception("File not found")

    with open(filename, 'r') as f:
        data = json.load(f)

    results = data["Scan Results"]["alerts"]
    pprint(results[0])
