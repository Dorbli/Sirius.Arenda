from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from database.database import get_db
import uuid

secret_key = "HelloWorld"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_acc_token(user_id: str):
    payload = {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=1)}
    return jwt.encode(payload, secret_key, "HS256")

def verify_acc_token(token: str):
    try:
        return jwt.decode(token, secret_key, "HS256")
    except jwt.InvalidTokenError:
        return 'invalid'
    except jwt.ExpiredSignatureError:
        return 'expired'
    
def get_user(username: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            return dict(row)
        return '404'

def get_user_by_id(user_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?",
                            (user_id,)).fetchone()
        if row:
            return dict(row)
        else:
            return '404'

def get_all_users():
    with get_db() as conn:
        rows = conn.execute("SELECT id, username FROM users").fetchall()
        return [dict(r) for r in rows]

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user == '404':
        return '404'
    if not verify_password(password, user["hashed_pass"]):
        return '401'
    return user

def create_user(username: str, password: str, role: str = 'base'):
    with get_db() as conn:
        if get_user(username) == '404':
            id = str(uuid.uuid4())
            conn.execute("INSERT INTO users (id, username, hashed_pass, role) VALUES (?, ?, ?, ?)",
                         (id, username, get_password_hash(password), role))
            conn.commit()
            return get_user(username)
        return '409'
        
