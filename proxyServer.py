
import json
import sys


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from flask import Flask
from flask import request


def get_data(url, params={'base':'USD'}):
    ''' Retrives the data from the url'''
    # Being very careful when checking for failure when accessing the external site
    try:
        response = requests.get(url=url, params=params)
        if response.status_code != requests.codes['ok']:
            print("The url {0} did not return the expected value back.".format(response.url))
            print("Response: {0} {1}".format(response.status_code, response.reason))
            sys.exit(0)
        try:
            return json.dumps(response.json(), indent=4, sort_keys=True)
        except ValueError as exception:
            print(exception)
            sys.exit(0)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Connection timed out")
        sys.exit(0)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Too many redirects")
        sys.exit(0)
    except requests.exceptions.RequestException as exception:
        print("There was an issue with requesting the data:")
        print(exception)
        sys.exit(0)


application = Flask(__name__)
# Suppress insecure HTTPS warnings, if an untrusted certificate is used by the target endpoint
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@application.route("/")
def main():
    '''Returns the current data'''
    currency = request.args.get('base')
    return get_data('http://api.fixer.io/latest', {'base':currency})

if __name__ == "__main__":
    application.run()
