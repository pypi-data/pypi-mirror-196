import re
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from pydantic import validator

from fides.lib.cryptography.cryptographic_util import decode_password
from fides.lib.oauth.schemas.oauth import AccessToken
from fides.lib.schemas.base_class import BaseSchema


class PrivacyRequestReviewer(BaseSchema):
    """Data we can expose via the PrivacyRequest.reviewer relation"""

    id: str
    username: str


class UserCreate(BaseSchema):
    """Data required to create a FidesUser."""

    organization_fides_key: str
    username: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]

    @validator("organization_fides_key")
    @classmethod
    def validate_organization(cls, organization_fides_key: str) -> str:
        """Ensure organization does not have spaces."""
        if " " in organization_fides_key:
            raise ValueError("Organization cannot have spaces.")
        return organization_fides_key

    @validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        """Ensure password does not have spaces."""
        if " " in username:
            raise ValueError("Usernames cannot have spaces.")
        return username

    @validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Add some password requirements"""
        decoded_password = decode_password(password)

        if len(decoded_password) < 8:
            raise ValueError("Password must have at least eight characters.")
        if re.search("[0-9]", decoded_password) is None:
            raise ValueError("Password must have at least one number.")
        if re.search("[A-Z]", decoded_password) is None:
            raise ValueError("Password must have at least one capital letter.")
        if re.search("[a-z]", decoded_password) is None:
            raise ValueError("Password must have at least one lowercase letter.")
        if re.search(r"[\W]", decoded_password) is None:
            raise ValueError("Password must have at least one symbol.")

        return decoded_password


class UserCreateResponse(BaseSchema):
    """Response after creating a FidesUser"""

    id: str


class UserLogin(BaseSchema):
    """Similar to UserCreate except we do not need the extra validation on
    username and password.
    """
    
    username: str
    password: str

    @validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Convert b64 encoded password to normal string"""
        return decode_password(password)

class UserLoginOrg(BaseSchema):
    """Similar to UserCreate except we do not need the extra validation on
    username and password.
    """

    organization_fides_key: str
    username: str
    password: str

    @validator("organization_fides_key")
    @classmethod
    def validate_organization(cls, organization_fides_key: str) -> str:
        """Ensure organization does not have spaces."""
        if " " in organization_fides_key:
            raise ValueError("Organization cannot have spaces.")
        return organization_fides_key

    @validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Convert b64 encoded password to normal string"""
        return decode_password(password)

class UserOrgResponse(BaseSchema):
    """Response after requesting a User"""

    id: str
    username: str
    created_at: datetime
    first_name: Optional[str]
    last_name: Optional[str]
    organization_fides_key: str
    last_login_at: Optional[datetime] = None

class UserResponse(BaseSchema):
    """Response after requesting a User"""

    id: str
    username: str
    created_at: datetime
    first_name: Optional[str]
    last_name: Optional[str]
    organization_fides_key: str
    password_reset_at: Optional[datetime]
    password_expire: Optional[bool] = False
    last_login_at: Optional[datetime] = None

    @validator('password_expire', pre=True, always=True)
    def set_password_expire(cls, v, values):
        password_reset_at = values.get('password_reset_at')
        if password_reset_at is None:
            return None
        password_expire_date = password_reset_at + timedelta(days=30)
        return password_expire_date < datetime.now(timezone.utc)

class OrgResponse(BaseSchema):
    """Response after requesting a Organization"""

    id: str
    fides_key: str
    organization_fides_key: str
    name: Optional[str]
    description: Optional[str]    


class UserLoginResponse(BaseSchema):
    """Similar to UserResponse except with an access token"""
    org_data: OrgResponse
    user_data: UserResponse
    token_data: AccessToken


class UserPasswordReset(BaseSchema):
    """Contains both old and new passwords when resetting a password"""

    old_password: str
    new_password: str


class UserForcePasswordReset(BaseSchema):
    """Only a new password, for the case where the user does not remember their password"""

    new_password: str


class UserUpdate(BaseSchema):
    """Data required to update a FidesopsUser"""

    first_name: Optional[str]
    last_name: Optional[str]

class UserNewResponse(BaseSchema):
    items: List[UserResponse]
    total: int
    page: int
    size: int