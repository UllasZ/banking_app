from src.banking_app.database.mysql_connector import Mysqldb
from src.banking_app.logger.logger import log
from src.banking_app.models.users_model import User


def create_user(user_data: dict) -> dict:
    try:
        mysqldb = Mysqldb()
        query = """
            INSERT INTO users (username, password, first_name, last_name, is_active, is_logged_in)
            VALUES (%s, %s, %s, %s, 1, 0)
        """
        values = (
            user_data.get("username"),
            user_data.get("password"),
            user_data.get("first_name"),
            user_data.get("last_name"),
        )
        mysqldb.insert_mysqldb(query, values)
        log.info("User created successfully")
        return {"message": "User created successfully"}
    except Exception as e:
        log.error(f"Error creating user: {str(e)}")
        return {"error": "User creation failed."}


def get_user(user_id: int) -> dict:
    try:
        mysqldb = Mysqldb()
        query = "SELECT id, username, first_name, last_name, is_active, is_logged_in FROM users WHERE id = %s"
        result = mysqldb.read_mysqldb(query, (user_id,))
        if result:
            return User(**result[0]).__dict__
        else:
            return {"error": "User not found."}
    except Exception as e:
        log.error(f"Error fetching user: {str(e)}")
        return {"error": "Failed to fetch user."}


def get_all_users() -> list[dict]:
    try:
        mysqldb = Mysqldb()
        query = "SELECT id, username, first_name, last_name, is_active, is_logged_in FROM users WHERE is_active = 1"
        results = mysqldb.read_mysqldb(query)
        users = [User(**row).__dict__ for row in results]
        log.info(f"Fetched {len(users)} active users")
        return users
    except Exception as e:
        log.error(f"Error fetching users: {str(e)}")
        return []


def update_user(user_id: int, update_data: dict) -> dict:
    try:
        # Only allow updating certain fields
        allowed_fields = ["first_name", "last_name", "password"]
        fields = []
        values = []

        for field in allowed_fields:
            if field in update_data:
                fields.append(f"{field} = %s")
                values.append(update_data[field])

        if not fields:
            log.warning("No valid fields provided for update")
            return {"error": "No valid fields provided for update"}

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"

        mysqldb = Mysqldb()
        mysqldb.update_mysqldb(query, tuple(values))

        log.info(f"User {user_id} updated successfully")
        # Return updated user info
        return get_user(user_id)
    except Exception as e:
        log.error(f"Error updating user: {str(e)}")
        return {"error": "Failed to update user"}
