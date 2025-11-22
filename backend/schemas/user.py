from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from uuid import UUID


PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\"':{}|<>]).{8,}$"
# Base schema cho user
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)

# Response
class UserResponse(UserBase):
    id: int | UUID
    is_active: bool = True
    role: str = "user" 
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }  # mapping sang ORM object thành JSON response


# Schema dùng khi tạo user mới (register/signup)
class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=25,
        description="Mật khẩu từ 8 kí tự trở lên và phải có ít nhất 1 chữ hoa, 1 chữ thường, 1 số và 1 ký tự đặc biệt."
    )
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                'Mật khẩu phải có ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.'
            )
        return value

# Schema dùng khi cập nhật user (chỉ cập nhật một số trường)
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="Mật khẩu từ 8 kí tự trở lên.")
    is_active: Optional[bool] = None
    role: Optional[str] = None

    # Nếu có cập nhật password thì validate lại
    @field_validator('password', mode='before') 
    @classmethod
    def validate_password_update(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        # Kiểm tra v không phải chuỗi rỗng trước khi match (nếu cần)
        if v and not re.match(PASSWORD_REGEX, v):
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự, gồm chữ hoa, thường, số và ký tự đặc biệt')
        return v


# Schema dùng để trả về thông tin user khi login (có token)
class UserLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

