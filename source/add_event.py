from __future__ import print_function

import datetime
from distutils.util import convert_path
from operator import index
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

cals = ['cal_id1', 'cal_id2', 'primary']  # Enter your calendar ids here
# 0 - cal_name1
# 1 - cal_name2
cal_selector = 2    # Default Calendar = Primary



def main():

    # don't manipulate this section

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


# manipulate this section
    try:            
        service = build('calendar', 'v3', credentials=creds)
        #review periods: 1, 7, 30 days after
        timedeltas = [datetime.timedelta(days=1), datetime.timedelta(
            days=7), datetime.timedelta(days=30)]

        def convert_to_RDATE(date):
            return date.strftime("%Y") + date.strftime("%m") + date.strftime("%d") + 'T' + date.strftime("%X") + 'Z'

        def convert_to_cal_format(date):
            return date.strftime("%Y") + "-" + date.strftime("%m") + "-" + date.strftime("%d")

        now = datetime.datetime.now()

        cal_selector = int(input(bcolors.OKGREEN + "Choose Calendar:\n    0 - cal_name1\n    1 - cal_name2\n    2 - Primary\n" + bcolors.ENDC))
        summary = input(bcolors.OKGREEN + "Enter the title:\n" + bcolors.ENDC)
        description = input(bcolors.OKGREEN + "Enter the description:\n" + bcolors.ENDC)

        for i in timedeltas:
            event = {
                'summary': summary + " R" + str(timedeltas.index(i)+1),
                'description': description,
                'start': {
                    'date': convert_to_cal_format(datetime.datetime.now() + i),
                },
                'end': {
                    'date': convert_to_cal_format(datetime.datetime.now() + i),
                },
                'transparency': 'transparent',      # doesn't block time = Available
                #'reminders': {
                #    'useDefault': False,
                #    'overrides': [
                #        #{'method': 'email', 'minutes': 24 * 60},
                #        {'method': 'popup', 'minutes': 90},
                #    ],
                #},
            }

            event = service.events().insert(calendarId=cals[cal_selector], body=event).execute()
            print('Event created: %s' % (event.get('id')))


    except HttpError as error:
        print('An error occurred: %s' % error)



# Prints the start and name of the next 10 events
"""# Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event)

    except HttpError as error:
        print('An error occurred: %s' % error)"""


# if you want to create recurring events add this to the body:
"""" 'recurrence': [
                    'RDATE;VALUE=DATE:' + convert_to_RDATE(now + t1) + ',' + convert_to_RDATE(
                        now + t2) + ',' + convert_to_RDATE(now + t3)
                ],"""

if __name__ == '__main__':
    main()
