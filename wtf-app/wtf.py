# wtf.py
# File Path: wtf-app/wtf.py
import csv
import http
import requests
from flask import Flask, make_response, request
from config import Config

# Initialize Flask application
APP = Flask(__name__)
# Load tokens and URL from environment via Config class
APP.config.from_object(Config())

# Define route for /slack endpoint
@APP.route('/slack', methods=['GET', 'POST'])
def slack():
    """
    Function that handles the '/slack' endpoint.
    Upon invocation, validates the request, fetches the acronym explanations from the CSV file,
    and prepares the response to be sent back to Slack.
    """

    # Convert request form data into dict
    req = dict(request.form)

    # Check if all required keys are present in the request
    if not all(k in req.keys() for k in ['text', 'token']):
        # If not, return a HTTP 400 Bad Request status code and error message
        return make_response('Improper request.', http.HTTPStatus.BAD_REQUEST)

    # Check if provided token is in the list of valid SLACK_TOKENS
    if req['token'] not in APP.config['SLACK_TOKENS']:
        # If not, return a HTTP 401 Unauthorized status code and error message
        return make_response('Not authorized', 401)

    # Fetch raw data from the DATA_URL
    raw = requests.get(APP.config['DATA_URL'])

    # Decode the fetched raw data
    decoded = raw.content.decode('utf-8')

    # Parse the decoded CSV data into a list of rows
    reader = csv.reader(decoded.split('\n'), delimiter=',')

    # Filter out any empty rows
    data = [r for r in reader if len(r) > 1]

    # Initialize empty dictionary for terms and their explanations
    term_dict = {}

    # Iterate through all rows in the data and populate the term_dict
    for d in data:
        # If row does not consist of 4 elements (Acronym, Definition, Context, Notes), skip
        if len(d) != 4:
            continue

        # Prepare data for each acronym
        acroynm = d[0].lower()  # Acronym
        definition = d[1].strip()  # Definition
        context = notes = ''  # Initialize empty strings for Context and Notes

        # If context provided, update context
        if len(d[2]) > 0:
            context = "\n\t- " + d[2].strip()

        # If notes provided, update notes
        if len(d[3]) > 0:
            notes = "\n\t- " + d[3].strip()

        # Prepare the complete acronym explanation
        full_data = "{}{}{}".format(definition, context, notes)

        # Check if acronym is already in the term_dict
        existing = term_dict.get(acroynm, None)

        # Add the complete explanation to the acronym's existing explanations, if any
        if not existing:
            term_dict[acroynm] = [full_data]
        else:
            term_dict[acroynm] = existing + [full_data]

    # Handling the response
    try:
        # Get and prepare the response for the requested acronym
        acroynm_defined = term_dict[req['text'].lower()]

        if len(acroynm_defined) > 1:
            response = ' - ' + '; \n - '.join(acroynm_defined)
        else:
            response = ' - ' + acroynm_defined[0]

        response = req['text'] + '\n' + response

    # If the requested acronym does not exist, prepare an error message
    except KeyError:
        response = """
        Entry for '{}' not found! Acronyms may be added at
        https://github.com/department-of-veterans-affairs/acronyms
        """.format(req['text'])

    # Return the response
    return make_response(response)
