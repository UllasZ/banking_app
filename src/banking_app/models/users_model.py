from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    is_active: bool
    is_logged_in: bool

