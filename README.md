# Kaiser

This is intended to be a chatbot where I will experiment with Slackbots, Bolt,
and chatops style automation.

My goals are to help prepare for next year's Mystery Hunt by building a bot
to handle some simple automation needs for our team.

## About the name

Kaiser was one of the robots built by J.F. Sebastian in Blade Runner.

## Required environment variables

* SLACK_BOT_TOKEN
* SLACK_SIGNING_SECRET

## Local development

The documentation I'm following mentions using a virtual env named venv.

Personally, I'm also using ASDF to manage my local Python versions, but this may
not be necessary for you.

### ngrok

We use ngrok to connect from the local development environment (your computer)
to the greater internet.

```bash
$ ngrok http 3000
```

### local python application

With ngrok underway, you can start the virtual environment and run the app.

```bash
$ source ./venv/bin/activate
(.vent)$ python3 app.py
```

Certain code changes may need you to restart the application.
