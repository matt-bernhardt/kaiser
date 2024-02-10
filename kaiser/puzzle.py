# -*- coding: utf-8 -*-
"""Module wrapping a puzzle class"""
from __future__ import absolute_import

class Puzzle():
    """This is a wrapper for a Puzzle, which will in turn manipulate Slack and Sheets."""

    def __init__(self):
        """Initialization - doesn't do much right now"""
        self.data = {}

    def create(self, client, logger, say, puzzle_name):
        """Public method that coordinates creation steps"""
        channel_name = self.set_channel_name(puzzle_name)
        try:
            result = client.conversations_create(
                name=channel_name
            )
            logger.info(result)
            say(f"The channel #{channel_name} has been created!")
        except Exception as e:
            self.error(logger, say, "creating channel", e)

    def error(self, logger, say, context, message):
        """Shared error reporting from all the exceptions"""
        logger.error(f"Error {context}: {format(message)}")
        say(f":no_entry: *Error {context}:* {format(message)}")

    def list(self, say, client, logger):
        """Private: Look up and return the list of channels"""
        result = []
        try:
            response = client.conversations_list()
            result = response["channels"]
        except Exception as e:
            self.error(logger, say, "listing channels", e)
        return result

    def lookup(self, client, logger, say, puzzle_name):
        """Private: Roll our own channel lookup since Slack doesn't have one"""
        channel_id = ""
        channels = self.list(say, client, logger)
        try:
            for channel in channels:
                if channel["name"] == self.set_channel_name(puzzle_name):
                    channel_id = channel["id"]
        except Exception as e:
            self.error(logger, say, "looking up channel", e)
        return channel_id

    def set_channel_name(self, puzzle_name):
        """Private: Clean and process a provided puzzle name to be Slack-friendly"""
        return "puzzle-" + puzzle_name.lower().replace(" ","_")

    def solve(self, client, logger, say, puzzle_name):
        """Public method that coordinates the steps to mark a puzzle as solved"""
        # Look up channel info based on name
        channel_id = self.lookup(client, logger, say, puzzle_name)
        if channel_id == "":
            say("Could not find channel, nothing to do")
            return
        try:
            result = client.conversations_rename(
                channel=channel_id,
                name=self.set_channel_name(puzzle_name).replace("puzzle-","solved-")
            )
            say(f"Channel for puzzle \"{puzzle_name}\" has been renamed.")
            say(f"{result}")
        except Exception as e:
            self.error(logger, say, "renaming channel", e)
