# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Sheet():
  """
  This is a wrapper for a google sheet.
  """

  def __init__(self):
    # This needs to handle authentication
    self.data = {}

  # This creates a new sheet
  def create(self):
    self.data["worksheet_id"] = "some_new_value"

  # This connects to an existing sheet, for example the dashboard
  def load(self, sheet_id):
    self.data["worksheet_id"] = sheet_id
