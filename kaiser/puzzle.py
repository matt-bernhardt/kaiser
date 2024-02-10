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
      self.error(logger, say, "creating channel", e)

  def error(self, logger, say, context, message):
    logger.error(f"Error {context}: {format(message)}")
    say(f":no_entry: *Error {context}:* {format(message)}")

  def list(self, say, client, logger):
    result = []
    try:
      result = client.conversations_list()
    except Exception as e:
      self.error(logger, say, "listing channels", e)
    return result

  def lookup(self, client, logger, say, puzzle_name):
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
      self.error(logger, say, "renaming channel", e)
