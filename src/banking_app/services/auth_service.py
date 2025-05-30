from src.banking_app.database.mysql_connector import Mysqldb
from src.banking_app.logger.logger import log
from src.banking_app.models.users_model import User

def login_user(user_data: dict) -> dict:
    try:
        username = user_data.get("username")
        password = user_data.get("password")
        log.info(f"Attempting login for user: {username}")

        mysqldb = Mysqldb()
        query = "SELECT id, username, first_name, last_name FROM users WHERE username=%s AND password=%s"
        result = mysqldb.read_mysqldb(query, (username, password))

        if result:
            user = User(**result[0])
            query_update = "UPDATE users SET is_logged_in = 1 WHERE id = %s"
            mysqldb.update_mysqldb(query_update, (user.id,))
            return user.__dict__
        else:
            return {"error": "Invalid username or password."}
    except Exception as e:
        log.error(f"Login error: {str(e)}")
        return {"error": "Internal server error."}

def logout_user(user_data: dict) -> dict:
    try:
        user_id = user_data.get("id")
        log.info(f"Logging out user ID: {user_id}")

        mysqldb = Mysqldb()
        query = "UPDATE users SET is_logged_in = 0 WHERE id = %s"
        mysqldb.update_mysqldb(query, (user_id,))
        return {"message": f"User {user_id} successfully logged out."}
    except Exception as e:
        log.error(f"Logout error: {str(e)}")
        return {"error": "Internal server error."}
