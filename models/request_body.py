from typing import List
from pydantic import BaseModel

# for get request body
class UrlRequestBody(BaseModel):
    url: str

class ListUrlRequestBody(BaseModel):
    urls: List[str]