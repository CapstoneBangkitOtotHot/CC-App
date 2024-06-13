from pydantic import BaseModel

# ========== Request Models ===========


class LoginRequestModel(BaseModel):
    email: str
    password: str


class RefreshTokenRequestModel(BaseModel):
    token: str


class SendPasswordResetEmailRequestModel(BaseModel):
    email: str


class ChangePasswordRequestModel(BaseModel):
    old_password: str
    new_password: str


# ========== Response Models (200 HTTP Code) ===========


class OkResponseModel(BaseModel):
    status: str = "ok"


class LoginResponseDataModel(BaseModel):
    session_token: str
    refresh_token: str


class LoginResponseModel(BaseModel):
    status: str = "ok"
    data: LoginResponseDataModel


class ChangePasswordResponseModel(BaseModel):
    status: str = "ok"
    message: str = "Password has been changed"


class SendPasswordResetEmailResponseModel(BaseModel):
    status: str = "ok"
    message: str = "Password reset email sent"


class DeleteAccountResponseModel(BaseModel):
    status: str = "ok"
    message: str = "User account deleted successfully"


class GetStatusEmailVerificationResponseModel(BaseModel):
    status: str = "ok"
    email_verified: bool
