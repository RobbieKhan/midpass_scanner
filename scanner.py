import json
import requests
from datetime import datetime, timedelta
from typing import Optional
import time

RESULTS_DIRECTORY_NAME = 'results/'
REQUEST_PERIOD_SEC = 0.1  # requests are done every 1 second
MAX_CHECK_DEPTH_DAYS = 10  # the period of time during which the application information is searched.
MAX_ACCESS_BLOCKED_ATTEMPTS_MIN = 1  # we don't want to stuck for more than 1 minute
MAX_ACCESS_BLOCKED_ATTEMPTS_NUM = MAX_ACCESS_BLOCKED_ATTEMPTS_MIN * 60 / REQUEST_PERIOD_SEC  # maximal attempts number based on request period and maximal wait time

request_url = 'https://info.midpass.ru/api/request/'
request_required_headers = {
    'User-Agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

wrong_dates_counter = 0


class Scanner:
    APPLICATION_TYPE = '2000'

    def __init__(self):
        self.consulate_code: Optional[str] = None
        self.application_date: Optional[str] = None
        self.application_number: Optional[int] = None

        self.depth_days: Optional[int] = None
        self.depth_applications: Optional[int] = None

        self.counter_access_blocked_attempts: int = 0
        self.counter_no_info: int = 0

    def set_consulate_code(self, code: int):
        self.consulate_code = str(code)

    def set_application_number(self, number: int):
        self.application_number = number

    def set_application_date(self, date: str):
        self.application_date = date

    def set_scanning_depth(self, days: Optional[int] = None, applications: Optional[int] = None):
        self.depth_days = days
        self.depth_applications = applications

    def start_scanning(self):
        # Create file with results
        filename = f'results_{datetime.now().strftime("%Y%m%d")}.txt'
        file = open(RESULTS_DIRECTORY_NAME + filename, 'w')
        # Start scanning
        days_scanned = 0
        for application_cnt in iter(int, 1):
            time.sleep(REQUEST_PERIOD_SEC)
            application_full_url = request_url + Scanner.APPLICATION_TYPE + self.consulate_code + self.application_date + str(
                self.application_number).zfill(8)
            r = requests.get(application_full_url, headers=request_required_headers)
            # Parse result
            if 200 == r.status_code:
                # It maybe a valid result or just an empty request if such application is missing
                try:
                    json_response = r.json()
                    result = f"{json_response['receptionDate']}, {self.application_number}, {json_response['internalStatus']['percent']}, {json_response['internalStatus']['name']}"
                    print(result)
                    file.write(result + '\n')
                    # Go to further application
                    self.application_number -= 1
                    self.counter_no_info = 0
                    self.counter_access_blocked_attempts = 0
                except json.JSONDecodeError:
                    # It is an empty request, reduce the date
                    self.counter_no_info += 1
                    date = datetime.strptime(self.application_date, '%Y%m%d')
                    date -= timedelta(days=1)
                    days_scanned += 1
                    self.application_date = date.strftime('%Y%m%d')
                    if self.counter_no_info == MAX_CHECK_DEPTH_DAYS:
                        # No info during more than 'MAX_CHECK_DEPTH_DAYS' days:
                        # 1) get back to day + 'MAX_CHECK_DEPTH_DAYS';
                        # 2) decrease application number.
                        print(f'            {self.application_number}, no information found')
                        date = datetime.strptime(self.application_date, '%Y%m%d')
                        date += timedelta(days=MAX_CHECK_DEPTH_DAYS)
                        days_scanned -= MAX_CHECK_DEPTH_DAYS
                        self.application_date = date.strftime('%Y%m%d')
                        self.application_number -= 1
                        self.counter_no_info = 0
            elif 403 == r.status_code:
                # Access is blocked, try again after small pause
                self.counter_access_blocked_attempts += 1
                if self.counter_access_blocked_attempts == MAX_ACCESS_BLOCKED_ATTEMPTS_NUM:
                    # Couldn't obtain informaion during 'MAX_ACCESS_BLOCKED_ATTEMPTS_MIN' minutes, ignore that application
                    print(f'            {self.application_number}, access blocked')
                    self.application_number -= 1
                    self.counter_access_blocked_attempts = 0

            if (self.depth_applications is not None and application_cnt > self.depth_applications) or \
                    (self.depth_days is not None and timedelta(self.depth_days) < timedelta(days_scanned)):
                break

        file.close()
