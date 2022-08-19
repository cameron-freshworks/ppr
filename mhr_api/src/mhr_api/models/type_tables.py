# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module holds model definitions for the MHR type tables."""

from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

from mhr_api.utils.base import BaseEnum

from .db import db


class CountryType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the country_type table."""

    __tablename__ = 'country_types'

    country_type = db.Column('country_type', db.String(2), primary_key=True)
    country_desc = db.Column('country_desc', db.String(75), nullable=False)

    # parent keys

    # Relationships - Address
    address = db.relationship('Address', back_populates='country_type')


class ProvinceType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the province_type table."""

    __tablename__ = 'province_types'

    province_type = db.Column('province_type', db.String(2), primary_key=True)
    country_type = db.Column('country_type', db.String(2),
                             db.ForeignKey('country_types.country_type'), nullable=False)
    province_desc = db.Column('province_desc', db.String(75), nullable=False)

    # parent keys

    # Relationships - Address
    address = db.relationship('Address', back_populates='province_type')


class PartyType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the party_type table."""

    __tablename__ = 'party_types'

    party_type = db.Column('party_type', db.String(2), primary_key=True)
    party_type_desc = db.Column('party_type_desc', db.String(30), nullable=False)

    # parent keys

    # Relationships - Party
    party = db.relationship('Party', back_populates='party_types')


class RegistrationTypeClass(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the registration_type_class table."""

    __tablename__ = 'registration_type_classes'

    registration_type_cl = db.Column('registration_type_cl', db.String(10), primary_key=True)
    registration_desc = db.Column('registration_desc', db.String(100), nullable=False)

    # parent keys

    # Relationships


class RegistrationType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the registration_type table."""

    __tablename__ = 'registration_types'

    registration_type = db.Column('registration_type', db.String(2), primary_key=True)
    registration_type_cl = db.Column('registration_type_cl', db.String(10),
                                     db.ForeignKey('registration_type_classes.registration_type_cl'), nullable=False)
    registration_desc = db.Column('registration_desc', db.String(100), nullable=False)
    registration_act = db.Column('registration_act', db.String(60), nullable=False)

    # parent keys

    # Relationships - Registration
    registration = db.relationship('Registration', back_populates='reg_type')


class EventTrackingType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the event_tracking_types table."""

    __tablename__ = 'event_tracking_types'

    event_tracking_type = db.Column('event_tracking_type', db.String(20), primary_key=True)
    event_tracking_desc = db.Column('event_tracking_desc', db.String(100), nullable=False)

    # parent keys

    # Relationships - EventTracking
    event_tracking = db.relationship('EventTracking', back_populates='tracking_type')


class SearchType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the search_type table."""

    __tablename__ = 'search_types'

    search_type = db.Column('search_type', db.String(2), primary_key=True)
    search_type_desc = db.Column('search_type_desc', db.String(60), nullable=False)

    # parent keys

    # Relationships - SearchRequest
    search_request = db.relationship('SearchRequest', back_populates='search_request_type')


class StateType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the state_type table."""

    __tablename__ = 'state_types'

    state_type = db.Column('state_type', db.String(3), primary_key=True)
    state_type_desc = db.Column('state_type_desc', db.String(30), nullable=False)

    # parent keys

    # Relationships - FinancingStatement
    financing_statement = db.relationship('FinancingStatement', back_populates='fin_state_type')


class SerialType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the serial_type table."""

    __tablename__ = 'serial_types'

    serial_type = db.Column('serial_type', db.String(2), primary_key=True)
    serial_type_desc = db.Column('serial_type_desc', db.String(30), nullable=False)

    # parent keys

    # Relationships - VehicleCollateral
    vehicle_collateral = db.relationship('VehicleCollateral', back_populates='serial_type')


# MHR specific type table enums below
class MhrNoteStatusTypes(BaseEnum):
    """Render an Enum of the MHR note status types."""

    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    CORRECTED = 'CORRECTED'


class MhrOwnerStatusTypes(BaseEnum):
    """Render an Enum of the MHR owner/owner group status types."""

    ACTIVE = 'ACTIVE'
    EXEMPT = 'EXEMPT'
    PREVIOUS = 'PREVIOUS'


class MhrPartyTypes(BaseEnum):
    """Render an Enum of the MHR party types."""

    OWNER_BUS = 'OWNER_BUS'
    OWNER_IND = 'OWNER_IND'
    SUBMITTING = 'SUBMITTING'


class MhrRegistrationStatusTypes(BaseEnum):
    """Render an Enum of the MHR registration status types."""

    ACTIVE = 'ACTIVE'
    DRAFT = 'DRAFT'
    EXEMPT = 'EXEMPT'
    HISTORICAL = 'HISTORICAL'


class MhrRegistrationTypes(BaseEnum):
    """Render an Enum of the MHR registration types."""

    MHREG = 'MHREG'


class MhrStatusTypes(BaseEnum):
    """Render an Enum of the MHR general status types."""

    ACTIVE = 'ACTIVE'
    DRAFT = 'DRAFT'
    HISTORICAL = 'HISTORICAL'


class MhrTenancyTypes(BaseEnum):
    """Render an Enum of the MHR tenancy types."""

    COMMON = 'COMMON'
    JOINT = 'JOINT'
    SOLE = 'SOLE'


# MHR specific type tables below
class MhrNoteStatusType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_note_status_types table."""

    __tablename__ = 'mhr_note_status_types'

    status_type = db.Column('status_type', PG_ENUM(MhrNoteStatusTypes), primary_key=True)
    status_type_desc = db.Column('status_type_desc', db.String(100), nullable=False)
    legacy_status_type = db.Column('legacy_status_type', db.String(1), nullable=False)

    # Relationships -

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrNoteStatusType).all()


class MhrOwnerStatusType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_owner_status_types table."""

    __tablename__ = 'mhr_owner_status_types'

    status_type = db.Column('status_type', PG_ENUM(MhrOwnerStatusTypes), primary_key=True)
    status_type_desc = db.Column('status_type_desc', db.String(100), nullable=False)
    legacy_status_type = db.Column('legacy_status_type', db.String(1), nullable=False)

    # Relationships -

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrOwnerStatusType).all()


class MhrPartyType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_party_types table."""

    __tablename__ = 'mhr_party_types'

    party_type = db.Column('party_type', PG_ENUM(MhrPartyTypes), primary_key=True)
    party_type_desc = db.Column('party_type_desc', db.String(100), nullable=False)
    legacy_party_type = db.Column('legacy_party_type', db.String(1), nullable=True)

    # Relationships -

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrPartyType).all()


class MhrRegistrationStatusType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_registration_status_types table."""

    __tablename__ = 'mhr_registration_status_types'

    status_type = db.Column('status_type', PG_ENUM(MhrRegistrationStatusTypes), primary_key=True)
    status_type_desc = db.Column('status_type_desc', db.String(100), nullable=False)
    legacy_status_type = db.Column('legacy_status_type', db.String(1), nullable=False)

    # Relationships -

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrRegistrationStatusType).all()


class MhrRegistrationType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_registration_types table."""

    __tablename__ = 'mhr_registration_types'

    registration_type = db.Column('registration_type', PG_ENUM(MhrRegistrationTypes), primary_key=True)
    registration_type_desc = db.Column('registration_type_desc', db.String(100), nullable=False)
    legacy_registration_type = db.Column('legacy_registration_type', db.String(4), nullable=False)

    # Relationships - MHR Registration
    registration = db.relationship('MhrRegistration', back_populates='reg_type')

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrRegistrationType).all()


class MhrStatusType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_status_types table."""

    __tablename__ = 'mhr_status_types'

    status_type = db.Column('status_type', PG_ENUM(MhrStatusTypes), primary_key=True)
    status_type_desc = db.Column('status_type_desc', db.String(100), nullable=False)
    legacy_status_type = db.Column('legacy_status_type', db.String(1), nullable=False)

    # Relationships -

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrStatusType).all()


class MhrTenancyType(db.Model):  # pylint: disable=too-few-public-methods
    """This class defines the model for the mhr_tenancy_types table."""

    __tablename__ = 'mhr_tenancy_types'

    tenancy_type = db.Column('tenancy_type', PG_ENUM(MhrTenancyTypes), primary_key=True)
    tenancy_type_desc = db.Column('tenancy_type_desc', db.String(100), nullable=False)
    legacy_tenancy_type = db.Column('legacy_tenancy_type', db.String(2), nullable=False)

    # Relationships -

    @classmethod
    def find_all(cls):
        """Return all the type records."""
        return db.session.query(MhrTenancyType).all()
