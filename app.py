import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
  token = os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
)

# Listener for opening home tab
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
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
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
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
def simple_response(say):
  say("Hi there!")

if __name__ == "__main__":
  # app.start(port=int(os.environ.get("PORT", 3000)))
  handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
  handler.start()
