from dataclasses import dataclass


@dataclass
class GetUploadUrlRequest:
    fileKey: str
