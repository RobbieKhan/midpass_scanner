import json
import time
import requests
import threading
from ui.diagram import Diagram
from ui.constants import *
from datetime import datetime, timedelta
from typing import Optional

REQUEST_PERIOD_SEC = 0.1  # requests are done every 1 second
MAX_CHECK_DEPTH_DAYS = 10  # the period of time during which the application information is searched.
MAX_ACCESS_BLOCKED_ATTEMPTS_MIN = 1  # we don't want to stuck for more than 1 minute
MAX_ACCESS_BLOCKED_ATTEMPTS_NUM = MAX_ACCESS_BLOCKED_ATTEMPTS_MIN * 60 / REQUEST_PERIOD_SEC  # maximal attempts number based on request period and maximal wait time


class Scanner:
    APPLICATION_TYPE = '2000'

    def __init__(self, diagram: Optional[Diagram] = None):
        self.consulate_code: Optional[str] = None
        self.application_date: Optional[str] = None
        self.application_number: Optional[int] = None

        self.depth_days: Optional[int] = None
        self.depth_applications: Optional[int] = None

        self.counter_access_blocked_attempts: int = 0
        self.counter_no_info: int = 0

        self.diagram: Optional[Diagram] = diagram

        self.is_scan_in_progress: bool = False

    def set_consulate_code(self, code: int):
        self.consulate_code = str(code)

    def set_application_number(self, number: int):
        self.application_number = number

    def set_application_date(self, date: str):
        self.application_date = date

    def set_scanning_depth(self, days: Optional[int] = None, applications: Optional[int] = None):
        self.depth_days = days
        self.depth_applications = applications

    def set_diagram_instance(self, diagram: Diagram):
        self.diagram = diagram

    def start_scanning(self):
        self.is_scan_in_progress = True
        threading.Thread(target=self.__scan, daemon=True).start()

    def __scan(self):
        # Create file with results
        filename = f'results_{datetime.now().strftime("%Y%m%d")}.txt'
        file = open(RESULTS_DIRECTORY_NAME + filename, 'w')
        if self.diagram is not None:
            self.diagram.set_filename(filename)
        # Start scanning
        days_scanned = 0
        applications_scanned = 0
        previous_date = None
        while True:
            time.sleep(REQUEST_PERIOD_SEC)
            application_full_url = REQUEST_URL + Scanner.APPLICATION_TYPE + self.consulate_code + \
                                   self.application_date + str(self.application_number).zfill(8)
            r = requests.get(application_full_url, headers=REQUEST_REQUIRED_HEADERS)
            # Parse result
            if 200 == r.status_code:
                # It maybe a valid result or just an empty request if such application is missing
                try:
                    json_response = r.json()
                    result = f"{json_response['receptionDate']}, {self.application_number}, " \
                             f"{json_response['internalStatus']['percent']}, {json_response['internalStatus']['name']}"
                    print(result)
                    file.write(result + '\n')
                    # Notify diagram builder
                    if self.diagram is not None:
                        if previous_date != json_response['receptionDate'] and previous_date is not None:
                            # Date has changed. Build all collected data for the previous day
                            self.diagram.build_appended()
                        previous_date = json_response['receptionDate']
                        self.diagram.append_data(date=previous_date, percent=json_response['internalStatus']['percent'])
                    # Go to further application
                    self.application_number -= 1
                    applications_scanned += 1
                    self.counter_no_info = 0
                    self.counter_access_blocked_attempts = 0
                except json.JSONDecodeError:
                    # It is an empty request, reduce the date
                    date = datetime.strptime(self.application_date, '%Y%m%d')
                    days_to_subtract = 3 if date.weekday() == 0 else 1
                    date -= timedelta(days=days_to_subtract)
                    days_scanned += days_to_subtract
                    self.counter_no_info += days_to_subtract
                    self.application_date = date.strftime('%Y%m%d')
                    if self.counter_no_info >= MAX_CHECK_DEPTH_DAYS:
                        # No info during more than 'MAX_CHECK_DEPTH_DAYS' days:
                        # 1) get back to day + 'MAX_CHECK_DEPTH_DAYS';
                        # 2) decrease application number.
                        print(f'            {self.application_number}, no information found')
                        date = datetime.strptime(self.application_date, '%Y%m%d')
                        date += timedelta(days=MAX_CHECK_DEPTH_DAYS)
                        days_scanned -= MAX_CHECK_DEPTH_DAYS
                        self.application_date = date.strftime('%Y%m%d')
                        self.application_number -= 1
                        applications_scanned += 1
                        self.counter_no_info = 0
            elif 403 == r.status_code:
                # Access is blocked, try again after small pause
                self.counter_access_blocked_attempts += 1
                if self.counter_access_blocked_attempts == MAX_ACCESS_BLOCKED_ATTEMPTS_NUM:
                    # Couldn't obtain information during 'MAX_ACCESS_BLOCKED_ATTEMPTS_MIN' minutes,
                    # ignore that application
                    print(f'            {self.application_number}, access blocked')
                    self.application_number -= 1
                    applications_scanned += 1
                    self.counter_access_blocked_attempts = 0

            if (self.depth_applications is not None and applications_scanned > self.depth_applications) or \
                    (self.depth_days is not None and self.depth_days < days_scanned) or \
                    not self.is_scan_in_progress:  # that indicator boolean is also used a stop flag
                self.is_scan_in_progress = False
                if self.diagram is not None:
                    self.diagram.build_appended()
                print('Script is finished!')
                break

        file.close()
