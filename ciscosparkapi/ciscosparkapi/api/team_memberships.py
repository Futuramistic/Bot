# -*- coding: utf-8 -*-
"""Cisco Spark Memberships API wrapper.

Classes:
    TeamMembership: Models a Spark 'team membership' JSON object as a native
        Python object.
    TeamMembershipsAPI: Wraps the Cisco Spark Memberships API and exposes
        the APIs as native Python methods that return native Python objects.

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from past.builtins import basestring


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


from ..generator_containers import generator_container
from ..restsession import RestSession
from ..sparkdata import SparkData
from ..utils import (
    check_type,
    dict_from_items_with_values,
)


class TeamMembership(SparkData):
    """Model a Spark 'team membership' JSON object as a native Python object.
    """

    def __init__(self, json):
        """Initialize a TeamMembership object from a dictionary or JSON string.

        Args:
            json(dict, basestring): Input dictionary or JSON object.

        Raises:
            TypeError: If the input object is not a dictionary or string.

        """
        super(TeamMembership, self).__init__(json)

    @property
    def id(self):
        """The team membership's unique ID."""
        return self._json_data.get('id')

    @property
    def teamId(self):
        """The ID of the team."""
        return self._json_data.get('teamId')

    @property
    def personId(self):
        """The ID of the person."""
        return self._json_data.get('personId')

    @property
    def personEmail(self):
        """The email address of the person."""
        return self._json_data.get('personEmail')

    @property
    def personDisplayName(self):
        """The display name of the person."""
        return self._json_data.get('personDisplayName')

    @property
    def personOrgId(self):
        """The ID of the organization that the person is associated with."""
        return self._json_data.get('personOrgId')

    @property
    def isModerator(self):
        """Person is a moderator for the team."""
        return self._json_data.get('isModerator')

    @property
    def created(self):
        """The date and time the team membership was created."""
        return self._json_data.get('created')


class TeamMembershipsAPI(object):
    """Cisco Spark Team-Memberships API wrapper.

    Wraps the Cisco Spark Memberships API and exposes the API as native Python
    methods that return native Python objects.

    """

    def __init__(self, session):
        """Init a new TeamMembershipsAPI object with the provided RestSession.

        Args:
            session(RestSession): The RESTful session object to be used for
                API calls to the Cisco Spark service.

        Raises:
            TypeError: If the parameter types are incorrect.

        """
        check_type(session, RestSession)

        super(TeamMembershipsAPI, self).__init__()

        self._session = session

    @generator_container
    def list(self, teamId, max=None, **request_parameters):
        """List team memberships for a team, by ID.

        This method supports Cisco Spark's implementation of RFC5988 Web
        Linking to provide pagination support.  It returns a generator
        container that incrementally yields all team memberships returned by
        the query.  The generator will automatically request additional 'pages'
        of responses from Spark as needed until all responses have been
        returned. The container makes the generator safe for reuse.  A new API
        call will be made, using the same parameters that were specified when
        the generator was created, every time a new iterator is requested from
        the container.

        Args:
            teamId(basestring): List team memberships for a team, by ID.
            max(int): Limit the maximum number of items returned from the Spark
                service per request.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            GeneratorContainer: A GeneratorContainer which, when iterated,
                yields the team memberships returned by the Cisco Spark query.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(teamId, basestring, may_be_none=False)
        check_type(max, int)

        params = dict_from_items_with_values(
            request_parameters,
            teamId=teamId,
            max=max,
        )

        # API request - get items
        items = self._session.get_items('team/memberships', params=params)

        # Yield Person objects created from the returned items JSON objects
        for item in items:
            yield TeamMembership(item)

    def create(self, teamId, personId=None, personEmail=None,
               isModerator=False, **request_parameters):
        """Add someone to a team by Person ID or email address.

        Add someone to a team by Person ID or email address; optionally making
        them a moderator.

        Args:
            teamId(basestring): The team ID.
            personId(basestring): The person ID.
            personEmail(basestring): The email address of the person.
            isModerator(bool): Set to True to make the person a team moderator.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            TeamMembership: A TeamMembership object with the details of the
                created team membership.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(teamId, basestring, may_be_none=False)
        check_type(personId, basestring)
        check_type(personEmail, basestring)
        check_type(isModerator, bool)

        post_data = dict_from_items_with_values(
            request_parameters,
            teamId=teamId,
            personId=personId,
            personEmail=personEmail,
            isModerator=isModerator,
        )

        # API request
        json_data = self._session.post('team/memberships', json=post_data)

        # Return a TeamMembership object created from the response JSON data
        return TeamMembership(json_data)

    def get(self, membershipId):
        """Get details for a team membership, by ID.

        Args:
            membershipId(basestring): The team membership ID.

        Returns:
            TeamMembership: A TeamMembership object with the details of the
                requested team membership.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(membershipId, basestring, may_be_none=False)

        # API request
        json_data = self._session.get('team/memberships/' + membershipId)

        # Return a TeamMembership object created from the response JSON data
        return TeamMembership(json_data)

    def update(self, membershipId, isModerator=None, **request_parameters):
        """Update a team membership, by ID.

        Args:
            membershipId(basestring): The team membership ID.
            isModerator(bool): Set to True to make the person a team moderator.
            **request_parameters: Additional request parameters (provides
                support for parameters that may be added in the future).

        Returns:
            TeamMembership: A TeamMembership object with the updated Spark team
                membership details.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(membershipId, basestring, may_be_none=False)
        check_type(isModerator, bool)

        put_data = dict_from_items_with_values(
            request_parameters,
            isModerator=isModerator,
        )

        # API request
        json_data = self._session.put('team/memberships/' + membershipId,
                                      json=put_data)

        # Return a TeamMembership object created from the response JSON data
        return TeamMembership(json_data)

    def delete(self, membershipId):
        """Delete a team membership, by ID.

        Args:
            membershipId(basestring): The team membership ID.

        Raises:
            TypeError: If the parameter types are incorrect.
            SparkApiError: If the Cisco Spark cloud returns an error.

        """
        check_type(membershipId, basestring, may_be_none=False)

        # API request
        self._session.delete('team/memberships/' + membershipId)
