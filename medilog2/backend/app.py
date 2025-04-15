from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Medication
from medications import meds_bp



app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Change this in production!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app, supports_credentials=True)

@app.before_first_request
def create_tables():
    db.create_all()

# ---------- User Authentication ----------

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        username=data['username']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'})

# ---------- Medication CRUD ----------

@app.route('/api/medications', methods=['GET'])
def get_medications():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    query = Medication.query.filter_by(user_id=user_id)

    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)

    sort = request.args.get('sort')
    if sort == 'name':
        query = query.order_by(Medication.name)
    elif sort == 'date':
        query = query.order_by(Medication.start_date)

    meds = query.all()
    data = [
        {
            'id': m.id,
            'name': m.name,
            'dosage': m.dosage,
            'frequency': m.frequency,
            'start_date': m.start_date,
            'notes': m.notes,
            'status': m.status
        } for m in meds
    ]

    active_count = Medication.query.filter_by(user_id=user_id, status='Active').count()

    return jsonify({'medications': data, 'active_count': active_count})

@app.route('/api/medications/<int:id>', methods=['GET'])
def get_medication(id):
    user_id = session.get('user_id')
    med = Medication.query.get_or_404(id)
    if med.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'id': med.id,
        'name': med.name,
        'dosage': med.dosage,
        'frequency': med.frequency,
        'start_date': med.start_date,
        'notes': med.notes,
        'status': med.status
    })

@app.route('/api/medications', methods=['POST'])
def add_medication():
    user_id = session.get('user_id')
    data = request.json
    med = Medication(
        name=data['name'],
        dosage=data['dosage'],
        frequency=data['frequency'],
        start_date=data['start_date'],
        notes=data['notes'],
        status=data['status'],
        user_id=user_id
    )
    db.session.add(med)
    db.session.commit()
    return jsonify({'message': 'Medication added'})

@app.route('/api/medications/<int:id>', methods=['PUT'])
def update_medication(id):
    user_id = session.get('user_id')
    med = Medication.query.get_or_404(id)
    if med.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    med.name = data['name']
    med.dosage = data['dosage']
    med.frequency = data['frequency']
    med.start_date = data['start_date']
    med.notes = data['notes']
    med.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Medication updated'})

@app.route('/api/medications/<int:id>', methods=['DELETE'])
def delete_medication(id):
    user_id = session.get('user_id')
    med = Medication.query.get_or_404(id)
    if med.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(med)
    db.session.commit()
    return jsonify({'message': 'Medication deleted'})

# ---------- Run the App ----------
if __name__ == '__main__':
    app.run(debug=True)
    app.register_blueprint(meds_bp)
