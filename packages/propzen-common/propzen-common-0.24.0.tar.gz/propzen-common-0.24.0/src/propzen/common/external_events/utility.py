from uuid import UUID
from dataclasses import dataclass
from propzen.common.service_layer.externalbus import ExternalEvent

@dataclass
class UtilityAttachmentRemoved(ExternalEvent):
    account_id: UUID
    utility_id: UUID
    file_id: UUID
