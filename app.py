from flask import Flask, jsonify, request
from models.user import User
from models.database import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'pLOkIjU@@7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if current_user.is_authenticated:
        return jsonify({"message": "User already logged in"}), 200

    if username and password:
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Login credentials fails."}), 403

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
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
    users = User.query.all()
    list_users = []
    if users:
        for user in users:
            list_users.append({
                "id": user.id,
                "username": user.username
            })
        return jsonify(list_users), 200
    return jsonify({"message": "No users found."}), 404



@app.route('/create_user', methods=['POST'])
@login_required
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists."}), 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"message": "Invalid data provided."}), 400

@app.route('/update_user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.get(user_id)
    if user:
        if username:
            user.username = username
        if password:
            user.password = password
        db.session.commit()
        return jsonify({"message": f"User 'id {user.id}' updated successfully"}), 200
    return jsonify({"message": "User not found."}), 404

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User 'id {user.id}' deleted successfully"}), 200
    return jsonify({"message": "User not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)



