# -*- coding: utf-8 -*-
"""Module wrapping a google sheet"""
from __future__ import absolute_import

class Sheet():
    """This will be a wrapper for a google sheet."""

    def __init__(self):
        """Initialization - doesn't do much right now"""
        self.data = {}

    def create(self):
        """This creates a new sheet"""
        self.data["worksheet_id"] = "some_new_value"

    def load(self, sheet_id):
        """This connects to an existing sheet, for example the dashboard"""
        self.data["worksheet_id"] = sheet_id
