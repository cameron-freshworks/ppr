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
"""This module holds data for MHR documents."""

from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

from mhr_api.exceptions import DatabaseException
from mhr_api.models import utils as model_utils
from mhr_api.utils.logging import logger

from .db import db
from .type_tables import MhrDocumentTypes


class MhrDocument(db.Model):  # pylint: disable=too-many-instance-attributes
    """This class manages all of the MHR document information."""

    __tablename__ = "mhr_documents"

    id = db.mapped_column("id", db.Integer, db.Sequence("mhr_document_id_seq"), primary_key=True)
    document_id = db.mapped_column("document_id", db.String(10), nullable=False, index=True)
    document_registration_number = db.mapped_column(
        "document_registration_number", db.String(8), nullable=False, index=True
    )
    attention_reference = db.mapped_column("attention_reference", db.String(50), nullable=True)
    owner_cross_reference = db.mapped_column("owner_x_reference", db.String(5), nullable=True)
    declared_value = db.mapped_column("declared_value", db.Integer, nullable=True)
    own_land = db.mapped_column("own_land", db.String(1), nullable=True)
    consideration_value = db.mapped_column("consideration_value", db.String(80), nullable=True)
    consent = db.mapped_column("consent", db.String(60), nullable=True)
    transfer_date = db.mapped_column("transfer_date", db.DateTime, nullable=True)
    affirm_by = db.mapped_column("affirm_by", db.String(60), nullable=True)

    # parent keys
    registration_id = db.mapped_column(
        "registration_id", db.Integer, db.ForeignKey("mhr_registrations.id"), nullable=False, index=True
    )
    change_registration_id = db.mapped_column("change_registration_id", db.Integer, nullable=False, index=True)
    document_type = db.mapped_column(
        "document_type",
        PG_ENUM(MhrDocumentTypes, name="mhr_document_type"),
        db.ForeignKey("mhr_document_types.document_type"),
        nullable=False,
    )

    # Relationships - MhrRegistration
    registration = db.relationship(
        "MhrRegistration",
        foreign_keys=[registration_id],
        back_populates="documents",
        cascade="all, delete",
        uselist=False,
    )

    @property
    def json(self) -> dict:
        """Return the document as a json object."""
        document = {
            "documentId": self.document_id,
            "documentRegistrationNumber": model_utils.format_doc_reg_number(self.document_registration_number),
            "documentType": self.document_type,
            "ownLand": False,
        }
        if self.attention_reference:
            document["attentionReference"] = self.attention_reference
        if self.consideration_value:
            document["consideration"] = self.consideration_value
        if self.consent:
            document["consent"] = self.consent
        if self.owner_cross_reference:
            document["ownerCrossReference"] = self.owner_cross_reference
        if self.own_land == "Y":
            document["ownLand"] = True
        if self.transfer_date:
            document["transferDate"] = model_utils.format_ts(self.transfer_date)
        if self.declared_value is not None:
            document["declaredValue"] = self.declared_value
        if self.affirm_by:
            document["affirmByName"] = self.affirm_by
        return document

    @classmethod
    def find_by_id(cls, pkey: int = None):
        """Return a document object by primary key."""
        document = None
        if pkey:
            try:
                document = db.session.query(MhrDocument).filter(MhrDocument.id == pkey).one_or_none()
            except Exception as db_exception:  # noqa: B902; return nicer error
                logger.error("MhrDocument.find_by_id exception: " + str(db_exception))
                raise DatabaseException(db_exception) from db_exception
        return document

    @classmethod
    def find_by_registration_id(cls, reg_id: int = None):
        """Return a list of document objects by registration id."""
        documents = None
        if reg_id:
            try:
                documents = (
                    db.session.query(MhrDocument)
                    .filter(MhrDocument.registration_id == reg_id)
                    .order_by(MhrDocument.id)
                    .all()
                )
            except Exception as db_exception:  # noqa: B902; return nicer error
                logger.error("MhrDocument.find_by_registration_id exception: " + str(db_exception))
                raise DatabaseException(db_exception) from db_exception
        return documents

    @classmethod
    def find_by_change_registration_id(cls, reg_id: int = None):
        """Return a list of document objects by change registration id."""
        documents = None
        if reg_id:
            try:
                documents = (
                    db.session.query(MhrDocument)
                    .filter(MhrDocument.change_registration_id == reg_id)
                    .order_by(MhrDocument.id)
                    .all()
                )
            except Exception as db_exception:  # noqa: B902; return nicer error
                logger.error("MhrDocument.find_by_change_registration_id exception: " + str(db_exception))
                raise DatabaseException(db_exception) from db_exception
        return documents

    @classmethod
    def find_by_document_id(cls, document_id: str):
        """Return the document matching the document id."""
        document = None
        if document_id:
            try:
                document = db.session.query(MhrDocument).filter(MhrDocument.document_id == document_id).one_or_none()
            except Exception as db_exception:  # noqa: B902; return nicer error
                logger.error("MhrDocument.find_by_document_id exception: " + str(db_exception))
                raise DatabaseException(db_exception) from db_exception
        return document

    @classmethod
    def find_by_doc_reg_num(cls, doc_reg_num: str):
        """Return the document matching the document registration number."""
        document = None
        if doc_reg_num:
            try:
                document = (
                    db.session.query(MhrDocument)
                    .filter(MhrDocument.document_registration_number == doc_reg_num)
                    .one_or_none()
                )
            except Exception as db_exception:  # noqa: B902; return nicer error
                logger.error("MhrDocument.find_by_doc_reg_num exception: " + str(db_exception))
                raise DatabaseException(db_exception) from db_exception
        return document

    @staticmethod
    def create_from_json(registration, reg_json, doc_type: str, change_registration_id: int = None):
        """Create a new document object from a new MH registration."""
        doc = MhrDocument(
            id=registration.doc_pkey,
            registration_id=registration.id,
            document_id=registration.doc_id,
            document_type=doc_type,
            document_registration_number=registration.doc_reg_number,
            own_land="N",
        )
        if not change_registration_id:
            doc.change_registration_id = registration.id
        else:
            doc.change_registration_id = change_registration_id
        if reg_json.get("attentionReference"):
            doc.attention_reference = reg_json["attentionReference"]
        if reg_json.get("declaredValue"):
            doc.declared_value = reg_json["declaredValue"]
        if reg_json.get("consideration"):
            doc.consideration_value = reg_json["consideration"]
        if reg_json.get("consent"):
            doc.consent = reg_json["consent"]
        if "ownLand" in reg_json and reg_json["ownLand"] is True:
            doc.own_land = "Y"
        if reg_json.get("ownerCrossReference"):
            doc.owner_cross_reference = reg_json["ownerCrossReference"]
        if reg_json.get("affirmByName"):
            doc.affirm_by = str(reg_json["affirmByName"]).upper()
        if registration.is_transfer() and reg_json.get("transferDate"):
            #  Set to end of day in the local time zone.
            doc.transfer_date = model_utils.expiry_datetime(reg_json["transferDate"])
        return doc
