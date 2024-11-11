from datetime import datetime
from pydantic import UUID4, BaseModel


class Token(BaseModel):
    exp:datetime
    iat:datetime
    sub:UUID4