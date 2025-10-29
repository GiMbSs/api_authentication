"""
Flask API for User Authentication and Management.

This module provides a REST API for user authentication with role-based access control.
"""

import bcrypt
from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)

from models.database import db
from models.user import User


# App Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'QAwsED1@__@(2345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'

# Login Manager Setup
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database tables and a default user for testing
with app.app_context():
    db.create_all()
    password = bcrypt.hashpw(b'admin', bcrypt.gensalt())
    user = User(username='admin', password=password, role='master')
    if not User.query.filter_by(username='admin').first():
        db.session.add(user)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return User.query.get(int(user_id))


# Authentication Routes
@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and create session."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if current_user.is_authenticated:
        return jsonify({"message": "User already logged in"}), 409
    
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(str.encode(password), user.password):
            login_user(user)
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Login credentials fails."}), 401


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Log out current user."""
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


# User Management Routes
@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get specific user by ID."""
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200
    return jsonify({"message": "User not found."}), 404


@app.route('/users/all', methods=['GET'])
@login_required
def get_users():
    """Get all users (admin/master only)."""
    if current_user.role == 'user':
        return jsonify({"message": "Admin access required."}), 403
    
    users = User.query.all()
    list_users = []
    for user in users:
        list_users.append({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })
    return jsonify(list_users), 200


@app.route('/create_user', methods=['POST'])
@login_required
def create_user():
    """Create a new user (admin/master only)."""
    if current_user.role == 'user':
        return jsonify({"message": "Admin access required."}), 403
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password = (bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) 
                if password else None)
    role = data.get('role') if current_user.role == 'master' else 'user'
    
    if username and password:
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists."}), 400
        
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    
    return jsonify({"message": "Invalid data provided."}), 400


@app.route('/update_user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """Update user information."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password = (bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) 
                if password else None)
    role = data.get('role')
    
    if current_user.role == 'user' and current_user.id != user_id:
        return jsonify({
            "message": "You can only update your own profile."
        }), 403
    
    if (username and current_user.username != username 
        and current_user.id == user_id):
        return jsonify({
            "message": "You cannot change your username while you are logged in."
        }), 422
    
    user = User.query.get(user_id)
    if user:
        if username:
            user.username = username
        if password:
            user.password = password
        if role and current_user.role == 'master':
            user.role = role
        else:
            if role:
                return jsonify({
                    "message": "Only master admins can change roles."
                }), 403
        
        db.session.commit()
        return jsonify({
            "message": f"User 'id {user.id}' updated successfully"
        }), 200
    
    return jsonify({"message": "User not found."}), 404


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete a user (admin/master only)."""
    if current_user.role == 'user':
        return jsonify({"message": "Admin access required."}), 403
    
    if current_user.id == user_id:
        return jsonify({
            "message": "You cannot delete your own account while logged in."
        }), 422
    
    user = User.query.get(user_id)
    if (current_user.role != 'master' and user 
        and (user.role == 'admin' or user.role == 'master')):
        return jsonify({
            "message": "Only master admins can delete other admins."
        }), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 204
    
    return jsonify({"message": "User not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)



