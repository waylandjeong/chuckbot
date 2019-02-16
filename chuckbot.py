#! /usr/bin/python

import time
import json
import logging
import requests
import slack_utility


def safe_requests(f, *args, **kwargs):
    """ A helper function to wrap requests calls with try/except block
    """
    try:

        r = f(*args, **kwargs)

        if r.status_code != 200:
            logging.error("Error: Unexpected response {}".format(r))
            return {}
        else:
            return r.json()

    except requests.exceptions.RequestException as e:
        logging.error("Error: {}".format(e))
        return {}


def handle_command(slack_api, command, channel):
	"""
	Recieves commands directed for the bot, if they are valid perform action 
	else resends clarification
	"""
	EXAMPLE_COMMAND = 'wisdom'
	if command.lower().startswith(EXAMPLE_COMMAND): 
                r = safe_requests(requests.get, "http://api.icndb.com/jokes/random")
                if r['type'] == 'success':
                    message = r['value']['joke']
                logging.info(message)
		slack_api.rtm_send_message(channel, message)
	elif command.lower().startswith('hi') or command.lower().startswith('hey') or command.lower().startswith('hello') or command.lower().startswith('who are you'):
		slack_api.rtm_send_message(channel, 'Hey, I\'m your Chuck Norris bot, ask me to give you some wisdom')
	else:
		print 'Invalid Command: Not Understood'
		slack_api.rtm_send_message(channel, 'Invalid Command: Not Understood')

	
def main():
	"""
	Initiate the bot and call appropriate handler functions
	"""
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	slack_api = slack_utility.connect()
	if slack_api.rtm_connect():
		print 'CHUCKBOT connected and running'
		while True:
			command, channel = slack_utility.parse_slack_response(slack_api.rtm_read())
			if command and channel:
				handle_command(slack_api, command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print 'Connection failed. Invalid Slack token or bot ID?' 


if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO)
	main()
