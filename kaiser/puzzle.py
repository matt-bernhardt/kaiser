# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os, logging

class Puzzle():
  """
  This is a wrapper for a puzzle.
  """

  def __init__(self):
    self.data = {}

  def create(self, client, logger, say, puzzle_name):
    channel_name = self.set_channel_name(puzzle_name)
    try:
      result = client.conversations_create(
        name=channel_name
      )
      logger.info(result)
      say(f"The channel #{channel_name} has been created!")
    except Exception as e:
      logger.error("Error creating channel: {}".format(e))
      say(f"I tried to create the channel #{channel_name}. Unfortunately, I failed.")

  def list(self, say, client, logger):
    try:
      result = client.conversations_list()
      return result["channels"]
    except Exception as e:
      logger.error("Error listing channels: {}".format(e))
      say(f"I tried to list all channels. Unfortunately, I failed.")
      return []

  def lookup(self, client, logger, say, puzzle_name):
    channel_id = ""
    channels = self.list(say, client, logger)
    try:
      for channel in channels:
        if channel["name"] == self.set_channel_name(puzzle_name):
          channel_id = channel["id"]
    except Exception as e:
      logger.error("Error looking up channel: {}".format(e))
      say(f"I tried to look up information about the channel. Unfortunately, I failed.")
    return channel_id

  def set_channel_name(self, puzzle_name):
    return "puzzle-" + puzzle_name.lower().replace(" ","_")

  def solve(self, client, logger, say, puzzle_name):
    # Look up channel info based on name
    channel_id = self.lookup(client, logger, say, puzzle_name)
    if channel_id == "":
      say(f"Could not find channel, nothing to do")
      return
    try:
      result = client.conversations_rename(
        channel=channel_id,
        name=self.set_channel_name(puzzle_name).replace("puzzle-","solved-") 
      )
      say(f"Channel for puzzle \"{puzzle_name}\" has been renamed.")
    except Exception as e:
      logger.error("Error renaming channel: {}".format(e))
      say(f"I tried to rename the channel. Unfortunately, I failed.")
