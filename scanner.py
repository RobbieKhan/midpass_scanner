import requests
from datetime import datetime, timedelta
import time

RESULTS_DIRECTORY_NAME = 'results/'
REQUEST_PERIOD_SEC = 0.5                                                                        # requests are done every 1 second
MAX_CHECK_DEPTH_DAYS = 10                                                                       # the period of time during which the application information is searched.
MAX_ACCESS_BLOCKED_ATTEMPTS_MIN = 1                                                             # we don't want to stuck for more than 1 minute
MAX_ACCESS_BLOCKED_ATTEMPTS_NUM = MAX_ACCESS_BLOCKED_ATTEMPTS_MIN * 60 / REQUEST_PERIOD_SEC     # maximal attempts number based on request period and maximal wait time


application_type = '2000'
application_consulate = '93104'
application_date = '20230313'
application_number = 11571

request_url = 'https://info.midpass.ru/api/request/'
request_required_headers = {'User-Agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

counter_no_info = 0
counter_access_blocked_attempts = 0

wrong_dates_counter = 0

filename = f'results_{datetime.now().strftime("%Y%m%d")}.txt'
file = open(RESULTS_DIRECTORY_NAME + filename, 'w')

while application_number > 11000:
    time.sleep(REQUEST_PERIOD_SEC)
    application_full_url = request_url + application_type + application_consulate + application_date + str(application_number).zfill(8)
    r = requests.get(application_full_url, headers=request_required_headers)
    # Parse result
    if 200 == r.status_code:
        # It maybe a valid result or just an empty request if such application is missing
        try:
            json_response = r.json()
            result = f"{json_response['receptionDate']}, {application_number}, {json_response['internalStatus']['percent']}, {json_response['internalStatus']['name']}"
            print(result)
            file.write(result + '\n')
            # Go to further application
            application_number -= 1
            counter_no_info = 0
            counter_access_blocked_attempts = 0
        except requests.exceptions.JSONDecodeError:
            # It is an empty request, reduce the date
            counter_no_info += 1
            date = datetime.strptime(application_date, '%Y%m%d')
            date -= timedelta(days=1)
            application_date = date.strftime('%Y%m%d')
            if counter_no_info == MAX_CHECK_DEPTH_DAYS:
                # No info during more than 'MAX_CHECK_DEPTH_DAYS' days:
                # 1) get back to day + 'MAX_CHECK_DEPTH_DAYS';
                # 2) decrease application number.
                print(f'            {application_number}, no information found')
                date = datetime.strptime(application_date, '%Y%m%d')
                date += timedelta(days=MAX_CHECK_DEPTH_DAYS)
                application_date = date.strftime('%Y%m%d')
                application_number -= 1
                counter_no_info = 0
    elif 403 == r.status_code:
        # Access is blocked, try again after small pause
        counter_access_blocked_attempts += 1
        if counter_access_blocked_attempts == MAX_ACCESS_BLOCKED_ATTEMPTS_NUM:
            # Couldn't obtain informaion during 'MAX_ACCESS_BLOCKED_ATTEMPTS_MIN' minutes, ignore that application
            print(f'            {application_number}, access blocked')
            application_number -= 1
            counter_access_blocked_attempts = 0

file.close()
