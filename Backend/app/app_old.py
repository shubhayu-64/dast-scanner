from datetime import datetime
import json
from flask import Flask, jsonify, request, make_response
import time
from flask_cors import CORS, cross_origin
from zapv2 import ZAPv2
from database import create_report, get_history, get_reports_of_user
from models import Alert, Report
from helper import CustomEncoder, dict_to_json_file, verify_local_database, verify_zap_exists, verify_zap_running, localUsername
from pprint import pprint
from bson.json_util import dumps

# Define a global variable to store the ZAP API key
API_KEY = 'mk5f08maq9eh575sem'


# Define ZAP API client
zap = ZAPv2(apikey=API_KEY, proxies={
    'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})


# Define a Flask app and a Docker client
app = Flask(__name__)
CORS(app)

# HTTP status code constants
HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED = 201
HTTP_SUCCESS_DELETED = 204
HTTP_SERVER_ERROR = 500
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400


def send(data, status_code):
    """
        Create a Flask response based on the data and status_code received.
    """
    return make_response(dumps(data), status_code)


@app.route('/spider', methods=['POST'])
@cross_origin()
def get_data():
    url = request.json['url']
    isActiveScan = False
    isActiveScan = request.json.get('ascan', False)

    print(f"Scanning for: {url}")
    print('Spidering target {}'.format(url))
    # The scan returns a scan id to support concurrent scanning
    scanID = zap.spider.scan(url)
    while int(zap.spider.status(scanID)) < 100:
        # Poll the status until it completes
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)
    print('Spider has completed!')

    # Passive scan
    print('Passive Scanning target {}'.format(url))
    while int(zap.pscan.records_to_scan) > 0:
        # Loop until the passive scan has finished
        print('Records to passive scan : ' + zap.pscan.records_to_scan)
        time.sleep(2)

    print('Passive Scan completed')

    # Active scan
    if isActiveScan:
        print("Active Scan for Target: {}".format(url))
        scan_id = zap.ascan.scan(url)

        while int(zap.ascan.status(scan_id)) < 100:
            print("Active scan completed: {} % ".format(
                zap.ascan.status(scan_id)))
            time.sleep(5)

        print("Active Scan Completed")

    # Save all scan results to a file
    dict_to_json_file({"Scan Results": {
                      "alerts": zap.alert.alerts(baseurl=url)}}, "scan_results.json")

    # Save the report to the database
    alertsData = zap.alert.alerts(baseurl=url),
    alerts = [Alert(userId=localUsername, **alert) for alert in alertsData[0]]
    report = Report(
        userId=localUsername,
        scanId=str(len(get_reports_of_user(localUsername)) + 1),
        target=url,
        alerts=alerts,
        status="Completed",
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )

    try:
        create_report(report)
    except Exception as e:
        print(e)

    return jsonify({"Scan Results": {
        "alerts": zap.alert.alerts(baseurl=url)}})


@app.route('/pscan', methods=['POST'])
def passive_scan():
    while int(zap.pscan.records_to_scan) > 0:
        # Loop until the passive scan has finished
        print('Records to passive scan : ' + zap.pscan.records_to_scan)
        time.sleep(2)

    print('Passive Scan completed')

    # Print Passive scan results/alerts
    dict_to_json_file({"Passive Scan": {"hosts": zap.core.hosts,
                      "alerts": zap.core.alerts()}}, "passive_scan_results.json")
    return jsonify({"status": True})


@app.route('/history', methods=['POST'])
@cross_origin()
def history():
    userId = request.json['userId']
    history = get_history(userId)
    return json.dumps([dict(obj) for obj in history], cls=CustomEncoder)


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return {"status": "Hello World"}

# Error Handler 404


@app.errorhandler(404)
def not_found(error):
    return send({'error': 'Not found'}, HTTP_NOT_FOUND)

# Error Handler 500


@app.errorhandler(500)
def internal_server_error(error):
    return send({'error': 'Internal Server Error'}, HTTP_SERVER_ERROR)

# Exception


@app.errorhandler(Exception)
def unhandled_exception(error):
    try:
        return send({'error': str(error)}, HTTP_SERVER_ERROR)
    except:
        return send({'error': "Unknown error"}, HTTP_SERVER_ERROR)


if __name__ == '__main__':
    # To run ZAP in daemon mode, use the following command in terminal:
    # zap/zap.sh -daemon -config api.key=mk5f08maq9eh575sem
    # zaproxy -daemon -config api.key=mk5f08maq9eh575sem
    # Or run ZAP in your local machine on port 8080
    # verify_zap_exists()
    verify_zap_running()
    verify_local_database()
    app.run(debug=True, port=5000)
    print("Stopping ZAP...")
