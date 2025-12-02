# user-service/app/core/security.py

from pwdlib import PasswordHash

# 1. CẤU HÌNH
password_hash = PasswordHash.recommended()

# 2. CÁC HÀM TIỆN ÍCH (Chỉ Hash và Verify)
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)