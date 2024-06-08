from pydantic import BaseModel

# ========== Request Models ===========


class SetUsernameRequestModel(BaseModel):
    displayName: str


# ========== Response Models (200 HTTP Code) ===========


class GetProfileResponseDataModel(BaseModel):
    username: str
    email: str
    photo_url: str

class GetProfileResponseModel(BaseModel):
    status: str = "ok"
    data: GetProfileResponseDataModel

class SetUsernameResponseModel(BaseModel):
    status: str = "ok"
    message: str = "Username updated successfully"