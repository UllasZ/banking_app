from http import HTTPStatus

from flask import Blueprint, request, jsonify
from src.banking_app.services.auth_service import login_user, logout_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("auth/login", methods=["POST"])
def login():

    user_data = request.json
    try:
        logged_in_user = login_user(user_data)

        return jsonify({
            "message": "User logged in successfully",
            "user": logged_in_user
        }), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@auth_bp.route("auth/logout", methods=["POST"])
def logout():

    user_data = request.json
    try:
        logged_out_user = logout_user(user_data)

        if not logged_out_user:
            return jsonify({"error": "User not found or no changes made"}), HTTPStatus.NOT_FOUND
        return jsonify({
            "message": "User logged out successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
