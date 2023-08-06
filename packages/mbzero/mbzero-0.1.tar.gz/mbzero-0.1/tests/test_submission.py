# -*- coding: utf-8 -*-
#
# This file is part of the mbzero library
#
# Copyright (C) 2023 Louis Rannou
#
# This file is distributed under a BSD-2-Clause type license. See the LICENSE
# file for more information.

import unittest
from unittest.mock import patch


from mbzero import (mbzauth as mba,
                    mbzrequest as mbr)


MUSICBRAINZ_API = mbr.MUSICBRAINZ_API
OTHER_API = "https://example.com"


@patch('requests_oauthlib.OAuth2Session.post')
class SubmissionTest(unittest.TestCase):
    def setUp(self):
        self.user_agent = "test_user_agent"
        self.headers = {"User-Agent": self.user_agent,
                        "Authorization": "Bearer token"}
        self.payload = {"fmt": "json"}
        self.data = "data"
        self.data_type = "xml"
        self.cred = mba.MbzCredentials()
        self.cred.oauth2_new("token", "refresh",
                             "client_id", "client_secret")

    def testSend(self, mock_post):
        mbr.MbzRequest(self.user_agent
                       ).post("/request", data="data", data_type="xml",
                              credentials=self.cred,
                              payload=self.payload, headers=self.headers)
        headers = self.headers
        headers["Content-Type"] = "application/xml; charset=utf-8"
        mock_post.assert_called_once_with(
            MUSICBRAINZ_API + "/request",
            data=self.data,
            params=self.payload, headers=self.headers)

    def testSubmissionSend(self, mock_post):
        mbr.MbzSubmission(self.user_agent, "request",
                          data="data", data_type="xml").send(
                              credentials=self.cred)
        headers = self.headers
        headers["Content-Type"] = "application/xml; charset=utf-8"
        payload = self.payload
        payload["client"] = self.user_agent
        mock_post.assert_called_once_with(
            MUSICBRAINZ_API + "/request",
            data=self.data,
            params=self.payload, headers=self.headers)
