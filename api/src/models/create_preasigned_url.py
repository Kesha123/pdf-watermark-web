from dataclasses import dataclass


@dataclass
class CreatePreasignedUrl:
    url: str
    s3_object_key: str
