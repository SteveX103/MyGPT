import hashlib
import hmac


class CryptContext:
	def __init__(self, *args, **kwargs):
		pass

	def hash(self, password: str) -> str:
		return hashlib.sha256(password.encode("utf-8")).hexdigest()

	def verify(self, password: str, hashed_password: str) -> bool:
		return hmac.compare_digest(self.hash(password), hashed_password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")