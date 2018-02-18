# -*- coding: utf-8 -*-
"""ciscosparkapi/__init__.py Fixtures & Tests"""


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


import os

import pytest

import ciscosparkapi


# pytest Fixtures

@pytest.fixture(scope="session")
def access_token():
    return os.environ.get(ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE)


@pytest.fixture
def unset_access_token(access_token):
    del os.environ[ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE]
    yield None
    os.environ[ciscosparkapi.ACCESS_TOKEN_ENVIRONMENT_VARIABLE] = access_token


@pytest.fixture(scope="session")
def api():
    return ciscosparkapi.CiscoSparkAPI()


# CiscoSparkAPI Tests

class TestCiscoSparkAPI:
    """Test the CiscoSparkAPI package-level code."""

    # Test creating CiscoSparkAPI objects

    @pytest.mark.usefixtures("unset_access_token")
    def test_creating_a_new_ciscosparkapi_object_without_an_access_token(self):
        with pytest.raises(ciscosparkapi.ciscosparkapiException):
            ciscosparkapi.CiscoSparkAPI()

    @pytest.mark.usefixtures("unset_access_token")
    def test_creating_a_new_ciscosparkapi_object_via_access_token_argument(self, access_token):
        connection_object = ciscosparkapi.CiscoSparkAPI(access_token=access_token)
        assert isinstance(connection_object,ciscosparkapi.CiscoSparkAPI)

    def test_creating_a_new_ciscosparkapi_object_via_environment_varable(self):
        connection_object = ciscosparkapi.CiscoSparkAPI()
        assert isinstance(connection_object,ciscosparkapi.CiscoSparkAPI)

    def test_default_base_url(self):
        connection_object = ciscosparkapi.CiscoSparkAPI()
        assert connection_object.base_url == ciscosparkapi.DEFAULT_BASE_URL

    def test_custom_base_url(self):
        custom_url = "https://spark.cmlccie.com/v1/"
        connection_object = ciscosparkapi.CiscoSparkAPI(base_url=custom_url)
        assert connection_object.base_url == custom_url

    def test_default_timeout(self):
        connection_object = ciscosparkapi.CiscoSparkAPI()
        assert connection_object.timeout == \
               ciscosparkapi.DEFAULT_SINGLE_REQUEST_TIMEOUT

    def test_custom_timeout(self):
        custom_timeout = 10
        connection_object = ciscosparkapi.CiscoSparkAPI(timeout=custom_timeout)
        assert connection_object.timeout == custom_timeout

    def test_default_single_request_timeout(self):
        connection_object = ciscosparkapi.CiscoSparkAPI()
        assert connection_object.single_request_timeout == \
               ciscosparkapi.DEFAULT_SINGLE_REQUEST_TIMEOUT

    def test_custom_single_request_timeout(self):
        custom_timeout = 10
        connection_object = ciscosparkapi.CiscoSparkAPI(
                single_request_timeout=custom_timeout
        )
        assert connection_object.single_request_timeout == custom_timeout

    def test_default_wait_on_rate_limit(self):
        connection_object = ciscosparkapi.CiscoSparkAPI()
        assert connection_object.wait_on_rate_limit == \
               ciscosparkapi.DEFAULT_WAIT_ON_RATE_LIMIT

    def test_non_default_wait_on_rate_limit(self):
        connection_object = ciscosparkapi.CiscoSparkAPI(
                wait_on_rate_limit=not ciscosparkapi.DEFAULT_WAIT_ON_RATE_LIMIT
        )
        assert connection_object.wait_on_rate_limit != \
               ciscosparkapi.DEFAULT_WAIT_ON_RATE_LIMIT

    # Test creation of component API objects

    def test_people_api_object_creation(self, api):
        assert isinstance(api.people, ciscosparkapi._PeopleAPI)

    def test_rooms_api_object_creation(self, api):
        assert isinstance(api.rooms, ciscosparkapi._RoomsAPI)

    def test_memberships_api_object_creation(self, api):
        assert isinstance(api.memberships, ciscosparkapi._MembershipsAPI)

    def test_messages_api_object_creation(self, api):
        assert isinstance(api.messages, ciscosparkapi._MessagesAPI)

    def test_teams_api_object_creation(self, api):
        assert isinstance(api.teams, ciscosparkapi._TeamsAPI)

    def test_team_memberships_api_object_creation(self, api):
        assert isinstance(api.team_memberships, ciscosparkapi._TeamMembershipsAPI)

    def test_webhooks_api_object_creation(self, api):
        assert isinstance(api.webhooks, ciscosparkapi._WebhooksAPI)

    def test_access_tokens_api_object_creation(self, api):
        assert isinstance(api.access_tokens, ciscosparkapi._AccessTokensAPI)
