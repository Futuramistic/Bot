# -*- coding: utf-8 -*-
"""pytest Memberships functions, fixtures and tests."""


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


import itertools

import pytest

import ciscosparkapi


# Helper Functions

def add_person_to_room_by_email(api, room, person, isModerator=False):
    return api.memberships.create(room.id,
                                  personEmail=person.emails[0],
                                  isModerator=isModerator)


def add_person_to_room_by_id(api, room, person, isModerator=False):
    return api.memberships.create(room.id,
                                  personId=person.id,
                                  isModerator=isModerator)


def add_people_to_room_by_email(api, room, people):
    return [add_person_to_room_by_email(api, room, person)
            for person in people]


def add_people_to_room_by_id(api, room, people):
    return [add_person_to_room_by_id(api, room, person)
            for person in people]


def get_room_membership_list(api, room, **kwargs):
    return list(api.memberships.list(roomId=room.id, **kwargs))


def get_my_membership(api, room, me):
    memberships = get_room_membership_list(api, room, personId=me.id)
    assert len(memberships) == 1
    membership = memberships[0]
    return membership


def get_membership_by_id(api, id):
    return api.memberships.get(id)


def make_moderator(api, membership):
    return api.memberships.update(membership.id, isModerator=True)


def delete_membership(api, membership):
    api.memberships.delete(membership.id)


def empty_room(api, me, room):
    """Remove all memberships from a room (except me)."""
    memberships = api.memberships.list(room.id)
    for membership in memberships:
        if membership.personId != me.id:
            delete_membership(api, membership)


def is_valid_membership(membership):
    return isinstance(membership, ciscosparkapi.Membership) \
           and membership.id is not None


def are_valid_memberships(iterable):
    are_valid = (is_valid_membership(item) for item in iterable)
    return all(are_valid)


def membership_exists(api, membership):
    try:
        get_membership_by_id(api, membership.id)
    except ciscosparkapi.SparkApiError:
        return False
    else:
        return True


# pytest Fixtures

@pytest.fixture(scope="session")
def authenticated_user_memberships(api, group_room, team_room, direct_rooms):
    return list(api.memberships.list())


@pytest.fixture(scope="session")
def me_group_room_moderator(api, group_room, me):
    membership_id = get_my_membership(api, group_room, me)
    return make_moderator(api, membership_id)


@pytest.fixture(scope="session")
def group_room_member_added_by_email(api, me_group_room_moderator,
                                     group_room, test_people):
    person = test_people["member_added_by_email"]
    membership = add_person_to_room_by_email(api, group_room, person)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def group_room_member_added_by_id(api, me_group_room_moderator,
                                  group_room, test_people):
    person = test_people["member_added_by_id"]
    membership = add_person_to_room_by_id(api, group_room, person)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def group_room_moderator_added_by_email(api, me_group_room_moderator,
                                        group_room, test_people):
    person = test_people["moderator_added_by_email"]
    membership = add_person_to_room_by_email(api, group_room, person,
                                             isModerator=True)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def group_room_moderator_added_by_id(api, me_group_room_moderator,
                                     group_room, test_people):
    person = test_people["moderator_added_by_id"]
    membership = add_person_to_room_by_id(api, group_room, person,
                                          isModerator=True)

    yield membership

    delete_membership(api, membership)


@pytest.fixture(scope="session")
def additional_group_room_memberships(group_room_member_added_by_email,
                                      group_room_member_added_by_id,
                                      group_room_moderator_added_by_email,
                                      group_room_moderator_added_by_id):
    return [group_room_member_added_by_email,
            group_room_member_added_by_id,
            group_room_moderator_added_by_email,
            group_room_moderator_added_by_id]


@pytest.fixture(scope="session")
def group_room_with_members(group_room, additional_group_room_memberships):
    return group_room


# Tests

class TestMembershipsAPI(object):
    """Test MembershipsAPI methods."""

    def test_get_membership_details(self, api, me_group_room_moderator):
        membership_id = me_group_room_moderator.id
        membership = get_membership_by_id(api, membership_id)
        assert is_valid_membership(membership)

    def test_list_user_memberships(self, authenticated_user_memberships):
        assert len(authenticated_user_memberships) >= 3
        assert are_valid_memberships(authenticated_user_memberships)

    def test_list_user_memberships_with_paging(self, api, add_rooms,
                                               authenticated_user_memberships):
        page_size = 1
        pages = 3
        num_memberships = pages * page_size
        if len(authenticated_user_memberships) < num_memberships:
            add_rooms(num_memberships - len(authenticated_user_memberships))
        memberships = api.memberships.list(max=page_size)
        memberships_list = list(itertools.islice(memberships, num_memberships))
        assert len(memberships_list) == num_memberships
        assert are_valid_memberships(memberships_list)

    def test_create_membership_by_email(self,
                                        group_room_member_added_by_email):
        assert is_valid_membership(group_room_member_added_by_email)

    def test_create_membership_by_person_id(self,
                                            group_room_member_added_by_id):
        assert is_valid_membership(group_room_member_added_by_id)

    def test_create_moderator_by_email(self,
                                       group_room_moderator_added_by_email):
        assert is_valid_membership(group_room_moderator_added_by_email)

    def test_create_moderator_by_person_id(self,
                                           group_room_moderator_added_by_id):
        assert is_valid_membership(group_room_moderator_added_by_id)

    def test_update_membership_make_moderator(self,
                                              me_group_room_moderator):
        assert is_valid_membership(me_group_room_moderator)
        assert me_group_room_moderator.isModerator

    def test_delete_membership(self, api, group_room, test_people):
        person = test_people["not_a_member"]
        membership = add_person_to_room_by_id(api, group_room, person)
        assert is_valid_membership(membership)
        delete_membership(api, membership)
        assert not membership_exists(api, membership)

    def test_list_room_memberships(self, api, group_room_with_members):
        memberships = get_room_membership_list(api, group_room_with_members)
        assert len(memberships) > 1
        assert are_valid_memberships(memberships)

    def test_filter_room_memberships_by_personEmail(self, api, test_people,
                                                    group_room_with_members):
        email = test_people["member_added_by_email"].emails[0]
        memberships = get_room_membership_list(api, group_room_with_members,
                                               personEmail=email)
        assert len(memberships) == 1
        membership = memberships[0]
        assert is_valid_membership(membership)
        assert membership.roomId == group_room_with_members.id

    def test_filter_room_memberships_by_personId(self, api, test_people,
                                                 group_room_with_members):
        id = test_people["member_added_by_id"].id
        memberships = get_room_membership_list(api, group_room_with_members,
                                               personId=id)
        assert len(memberships) == 1
        membership = memberships[0]
        assert is_valid_membership(membership)
        assert membership.roomId == group_room_with_members.id
