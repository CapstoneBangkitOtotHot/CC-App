from pydantic import BaseModel

# ========== Request Models ===========


class LoginRequestModel(BaseModel):
    email: str
    password: str


class RefreshTokenRequestModel(BaseModel):
    token: str


class SendPasswordResetEmailRequestModel(BaseModel):
    email: str


# ========== Response Models (200 HTTP Code) ===========


class OkResponseModel(BaseModel):
    status: str = "ok"


class LoginResponseDataModel(BaseModel):
    session_token: str
    refresh_token: str


class LoginResponseModel(BaseModel):
    status: str = "ok"
    data: LoginResponseDataModel


class ResetPasswordResponseModel(BaseModel):
    status: str = "ok"
    message: str = "Password reset email sent"


class SendPasswordResetEmailResponseModel(BaseModel):
    status: str = "ok"
    message: str = "Password reset email sent"


class DeleteAccountResponseModel(BaseModel):
    status: str = "ok"
    message: str = "User account deleted successfully"