# config.py
# File Path: api/config.py
# os module provides functions for interacting with the operating system like reading environment variables
from os import getenv


class Config(object):
    """
    Config Class to manage configuration settings used in the wtf-bot application.

    This class reads configured environment variables and exposes them through
    properties. Currently uses SLACK_TOKENS and DATA_URL environment variables.
    """

    @property
    def SLACK_TOKENS(self):
        """
        A property that retrieves and parses the SLACK_TOKENS environment variable.

        SLACK_TOKENS should be stored in the environment as a string, with individual tokens
        separated by commas.

        Returns:
            List of slack tokens to validate the requests from slack in '/slack' endpoint.

        Raises:
            ValueError:
            If the 'SLACK_TOKENS' environment variable is not set, a ValueError is raised.
        """
        slack_tokens_string = getenv('SLACK_TOKENS')  # Fetch 'SLACK_TOKENS' from the environment
        if not slack_tokens_string:
            raise ValueError("No SLACK_TOKENS environment variable set")
        # Split the string containing tokens by ',' and transform to list after stripping extra spaces
        return [token.strip() for token in slack_tokens_string.split(',')]

    @property
    def DATA_URL(self):
        """
        A property that retrieves the DATA_URL environment variable.

        The DATA_URL is the URL pointing to the CSV file containing the VA acronyms in GitHub.

        Returns:
            A single string representing the URL to raw CSV file of acronyms.

        Raises:
            ValueError:
            If the 'DATA_URL' environment variable is not set, a ValueError is raised.
        """
        data_url = getenv('DATA_URL')  # Fetch 'DATA_URL' from the environment
        if not data_url:
            raise ValueError("No DATA_URL environment variable set")
        return data_url