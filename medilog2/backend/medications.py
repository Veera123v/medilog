from flask import Blueprint, request, jsonify, session
from models import db, Medication

meds_bp = Blueprint('medications', __name__)

# ---------- Get All Medications (with filtering/sorting) ----------
@meds_bp.route('/api/medications', methods=['GET'])
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

    medications = query.all()
    data = [
        {
            'id': m.id,
            'name': m.name,
            'dosage': m.dosage,
            'frequency': m.frequency,
            'start_date': m.start_date,
            'notes': m.notes,
            'status': m.status
        } for m in medications
    ]

    active_count = Medication.query.filter_by(user_id=user_id, status='Active').count()

    return jsonify({'medications': data, 'active_count': active_count})


# ---------- Get One Medication ----------
@meds_bp.route('/api/medications/<int:id>', methods=['GET'])
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


# ---------- Create Medication ----------
@meds_bp.route('/api/medications', methods=['POST'])
def add_medication():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

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


# ---------- Update Medication ----------
@meds_bp.route('/api/medications/<int:id>', methods=['PUT'])
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


# ---------- Delete Medication ----------
@meds_bp.route('/api/medications/<int:id>', methods=['DELETE'])
def delete_medication(id):
    user_id = session.get('user_id')
    med = Medication.query.get_or_404(id)
    if med.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(med)
    db.session.commit()
    return jsonify({'message': 'Medication deleted'})

