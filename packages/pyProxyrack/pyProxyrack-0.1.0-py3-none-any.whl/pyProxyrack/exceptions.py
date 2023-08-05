class ProxyrackAPIError(Exception):
	"""Base Proxyrack API Exception."""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class NotLoggedInError(ProxyrackAPIError):
	"""Raised when you're not logged in and try to access protected endpoints."""
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

