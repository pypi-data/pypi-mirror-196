from uuid import UUID
from dataclasses import dataclass
from propzen.common.service_layer.externalbus import ExternalEvent


@dataclass
class ProfilePictureUploaded(ExternalEvent):
    account_id: UUID
    filename: str


@dataclass
class PropertyPictureUploaded(ExternalEvent):
    account_id: UUID
    property_id: UUID
    filename: str


@dataclass
class AssetAttachmentUploaded(ExternalEvent):
    account_id: UUID
    asset_id: UUID
    file_id: UUID
    filename: str
    originalname: str


@dataclass
class AssetImageUploaded(ExternalEvent):
    account_id: UUID
    asset_id: UUID
    file_id: UUID
    filename: str
    originalname: str


@dataclass
class UtilityBillAttachmentUploaded(ExternalEvent):
    account_id: UUID
    utility_id: UUID
    bill_id: UUID
    file_id: UUID
    filename: str
    originalname: str


@dataclass
class UtilityInvoiceAttachmentUploaded(ExternalEvent):
    account_id: UUID
    utility_id: UUID
    invoice_id: UUID
    file_id: UUID
    filename: str
    originalname: str
