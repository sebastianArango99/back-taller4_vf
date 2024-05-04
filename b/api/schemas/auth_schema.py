from pydantic import BaseModel
from api.schemas.user_schema import User

class Auth(BaseModel):
    access_token: str
    token_type: str
    user: User