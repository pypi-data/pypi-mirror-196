# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gc_google_services_api',
 'gc_google_services_api.auth',
 'gc_google_services_api.auth.__tests__',
 'gc_google_services_api.bigquery',
 'gc_google_services_api.bigquery.__tests__',
 'gc_google_services_api.calendar_api',
 'gc_google_services_api.calendar_api.__tests__',
 'gc_google_services_api.gmail',
 'gc_google_services_api.gmail.__tests__',
 'gc_google_services_api.gsheet',
 'gc_google_services_api.gsheet.__tests__',
 'gc_google_services_api.permissions']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=6.0.0,<7.0.0',
 'google-api-python-client>=2.80.0,<3.0.0',
 'google-cloud-bigquery>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'gc-google-services-api',
    'version': '1.2.2',
    'description': '',
    'long_description': '[![Publish to PyPI.org](https://github.com/GoodCod3/gc-google-services-api/actions/workflows/pr.yml/badge.svg)](https://github.com/GoodCod3/gc-google-services-api/actions/workflows/pr.yml)\n\nGoogle services API\n=============================\nThis repository is a suite that exposes Google services to easily integrate with our project (Big query, Google sheet, Gmail, etc...).\n\nEach api needs a different form of authentication, either because it requires the interaction of a person who approves the api to extract sensitive information or because we want to connect automatically without user intervention.\n\n\n\nWhat APIs and methods does it support?\n=======================\nThis project will grow as new services and methods are integrated.\n\nHere is a list of current support\n\n## Big Query\n----------------------------------\n\n### execute_query (Method):\nAllows you to run a query on a Big Query table.\n\nIn order for the api to connect to the table, it is necessary to configure the environment variable `$GOOGLE_APPLICATION_CREDENTIALS` indicating the path of the file with the credentials (service account json file)\n\n```bash\nexport GOOGLE_APPLICATION_CREDENTIALS=/home/service_account_file.json\n```\n\n### Usage example\n\n```python\nfrom gc_google_services_api.bigquery import execute_query\n\n\nquery = "SELECT * FROM users;"\nusers = execute_query(query)\n\nfor user in users:\n    print(user)\n```\n\n## Google sheet\n----------------------------------\n\n## 1.- **read_gsheet** (Method of a class):\nAllows to read and return the content of a Google sheet link.\nIt is necessary to indicate the range of columns that we want to return\n\nIn order for the api to connect with Google, it is necessary to send the JSON content of your service account.\nthe format of the service account should be something like this:\n\n```\n{\n  "type": "service_account",\n  "project_id": "XXXXXX",\n  "private_key_id": "XXXXXX",\n  "private_key": "XXXXXX",\n  "client_email": "XXXXXX",\n  "client_id": "XXXXXX",\n  "auth_uri": "https://accounts.google.com/o/oauth2/auth",\n  "token_uri": "https://oauth2.googleapis.com/token",\n  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",\n  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/XXXXXX"\n}\n\n```\n\n### Usage example\n\n```python\nfrom gc_google_services_api.gsheet import GSheet\n\n\nname = \'Sheet 1\'\nspreadsheet_id = \'11111111\'\nspreadsheet_range = \'A2:B12\'\n\ngsheet_api = GSheet(\'subject_email@test.com\')\nresult = gsheet_api.read_gsheet(sheet_name, spreadsheet_id, spreadsheet_range)\n\nfor row in result[\'values\']:\n    print(row)\n```\n\n## 2.-  **get_sheetnames** (Method of a class):\nGet the list of sheetnames given a spreadsheet id.\n\n\n### Usage example\n\n```python\nfrom gc_google_services_api.gsheet import GSheet\n\n\nspreadsheet_id = \'11111111\'\n\ngsheet_api = GSheet(\'subject_email@test.com\')\nresult = gsheet_api.get_sheetnames(spreadsheet_id)\n\nfor row in result[\'sheets\']:\n    print(row)\n```\n\n## Gmail\n----------------------------------\nSend emails with Gmail API.\n\nThis module needs to have configured an environment variable called `AUTHENTICATION_EMAIL` that will be the email used as sender.\n\n### Usage example\n\n```python\nimport os\nfrom gc_google_services_api.gmail import Gmail\n\n\ngmail_api = Gmail(\'subject-email@test.com\')\ngmail_api.send_email(\n    \'email message\',\n    \'email title\',\n    [\'to_email1@gmail.com\'],\n)\n```\n\n## Calendar\n----------------------------------\nGet calendars info and events.\n\nThis module needs to have configured an environment variable called `AUTHENTICATION_EMAIL` that will be the email used to authenticate with Google services.\n\n### Usage example\n\n```python\nimport os\nfrom datetime import datetime, timedelta\nfrom gc_google_services_api.calenda_api import Calendar\n\n\nstart_date = datetime.today()\nend_date = datetime.today() + timedelta(days=1)\ncreator = \'test@test.com\'\n\ncalendar_api = Calendar(start_date, end_date, creator)\n\n# Getting calendar resources\nresources = calendar_api.get_all_resources()\nprint(resources)\n\n# Getting calendars\ncalendar_api.request_calendars()\nprint(calendar_api.calendars)\n\n# Getting events from a calendar\ncalendar_id = \'1\'\ncalendar_api.request_calendar_events(calendar_id)\nprint(calendar_api.calendar_events)\n\n# Delete calendar event\ncalendar_id = \'1\'\nevent_id = \'2\'\ncalendar_api.remove_event(calendar_id, event_id)\n```',
    'author': 'Jonathan Rodríguez Alejos',
    'author_email': 'jrodriguez.5716@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
