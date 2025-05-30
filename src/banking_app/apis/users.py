from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.banking_app.services.users_service import create_user, get_user, get_all_users, update_user

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["POST"])
def register_user():
    user_data = request.json
    try:
        created_user = create_user(user_data)
        return jsonify({
            "message": "User created successfully",
            "user": created_user
        }), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = get_all_users()
        if not users:
            return jsonify({"message": "No users found"}), HTTPStatus.NOT_FOUND
        return jsonify({"users": users}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), HTTPStatus.NOT_FOUND
        return jsonify({"user": user}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_details(user_id):
    update_data = request.json
    try:
        updated_user = update_user(user_id, update_data)
        if not updated_user:
            return jsonify({"error": "User not found or no changes made"}), HTTPStatus.NOT_FOUND
        return jsonify({
            "message": "User updated successfully",
            "user": updated_user
        }), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
