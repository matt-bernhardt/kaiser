"""This is the core of the Slackbot."""
import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from kaiser.sheet import Sheet
from kaiser.puzzle import Puzzle

logging.basicConfig(level=logging.DEBUG)

app = App(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
)

# Listener for opening home tab
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    """This populates the bot's home tab."""
    try:
        client.views_publish(
            user_id = event["user"],
            view={
                "type": "home",
                "callback_id": "home_view",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home tab_* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a \
                                     listener for it using the `actions()` method and passing its unique \
                                     `action_id`. See an example in the `examples` folder within your Bolt \
                                     app."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Click me!"
                                }
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

# Listener for mentions
@app.event("app_mention")
def simple_response(say, logger):
    """This is the equivalent of a ping / pong response, or a simple heartbeat."""
    logger.info("Inside simple_response")
    say("Hi there!")

@app.command("/create-puzzle")
def create_puzzle(ack, client, logger, say, command):
    """This is a CLI command to create a cluster of infrastructure for a single puzzle."""
    ack()
    say(f"This would create the puzzle \"{command['text']}\".")
    # Create the Puzzle object, through which the Slack channel and Google sheet
    # will be created.
    draft = Puzzle()
    draft.create(client, logger, say, command['text'])
    # Everything after this is subject to deletion...
    # Create the working sheet
    working = Sheet()
    working.create()
    say(f"Working sheet defined as {working.data['worksheet_id']}")
    # Update the dashboard with a link to the working sheet
    dashboard = Sheet()
    dashboard.load(os.environ.get("SHEETS_DASHBOARD_ID"))
    say(f"Updating dashboard at {dashboard.data['worksheet_id']}")

    # Create the Slack channel
    # Pin a link to the sheet to the channel
    # Announce the new channel
    say("New puzzle created")

@app.command("/solve-puzzle")
def solve_puzzle(ack, client, logger, say, command):
    """This is a CLI command to update a puzzle's infrastructure after it is solved."""
    ack()
    say(f"This will solve the puzzle \"{command['text']}\".")
    target = Puzzle()
    target.solve(client, logger, say, command['text'])

# Listener for the demonstration modal
@app.shortcut("demonstrate_modal")
def demonstrate_modal(ack, shortcut, client):
    """This is a demonstration of a modal dialog."""
    ack()
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Demonstration modal box"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "This is a demonstration of a modal box invoked by a shortcut. If \
                                 this were a working form, there would be input boxes and a submit \
                                 button.\n\nThis is only a demonstration."
                    }
                }
            ]
        }
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
