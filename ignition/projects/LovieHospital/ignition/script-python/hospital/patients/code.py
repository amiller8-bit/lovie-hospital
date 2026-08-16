import uuid

DB_CONNECTION = "LovieHospital"


def get_patient_roster():
	"""Returns a dataset of all known patients (stuffed animals)."""
	query = "SELECT patient_id, name, species, photo_url, default_quirks FROM patients ORDER BY name"
	return system.db.runQuery(query, DB_CONNECTION)


def check_in(patient_id, chief_complaint):
	"""
	Checks in a patient, generating a new QR token for this visit.
	Returns the visit_id and qr_token so a caller can render/print the wristband.
	"""
	qr_token = uuid.uuid4().hex

	insert_query = """
		INSERT INTO visits (patient_id, qr_token, chief_complaint, status)
		VALUES (?, ?, ?, 'checked_in')
	"""
	system.db.runPrepUpdate(insert_query, [patient_id, qr_token, chief_complaint], DB_CONNECTION)

	lookup_query = "SELECT visit_id FROM visits WHERE qr_token = ?"
	result = system.db.runPrepQuery(lookup_query, [qr_token], DB_CONNECTION)
	visit_id = result.getValueAt(0, "visit_id")

	return {"visit_id": visit_id, "qr_token": qr_token}


def get_visit_by_qr(qr_token):
	"""
	Looks up the active visit for a scanned QR token. This is what the
	Perspective mobile QR scanner component should call after a scan.
	Returns None if no matching visit is found.
	"""
	query = """
		SELECT v.visit_id, v.status, v.chief_complaint, v.checked_in_at,
		       p.patient_id, p.name, p.species, p.photo_url
		FROM visits v
		JOIN patients p ON p.patient_id = v.patient_id
		WHERE v.qr_token = ?
	"""
	result = system.db.runPrepQuery(query, [qr_token], DB_CONNECTION)
	if result.getRowCount() == 0:
		return None

	return {
		"visit_id": result.getValueAt(0, "visit_id"),
		"status": result.getValueAt(0, "status"),
		"chief_complaint": result.getValueAt(0, "chief_complaint"),
		"checked_in_at": result.getValueAt(0, "checked_in_at"),
		"patient_id": result.getValueAt(0, "patient_id"),
		"name": result.getValueAt(0, "name"),
		"species": result.getValueAt(0, "species"),
		"photo_url": result.getValueAt(0, "photo_url"),
	}


def log_vitals(visit_id, temperature_f, heart_rate_bpm, mood, notes=""):
	"""Records one vitals reading for a visit. Call this from the mood buttons / vitals screen."""
	query = """
		INSERT INTO vitals (visit_id, temperature_f, heart_rate_bpm, mood, notes)
		VALUES (?, ?, ?, ?, ?)
	"""
	system.db.runPrepUpdate(query, [visit_id, temperature_f, heart_rate_bpm, mood, notes], DB_CONNECTION)

	# Bumping status to in_treatment on first vitals reading, if not already there
	update_status = """
		UPDATE visits SET status = 'in_treatment'
		WHERE visit_id = ? AND status = 'checked_in'
	"""
	system.db.runPrepUpdate(update_status, [visit_id], DB_CONNECTION)


def administer_medication(visit_id, medication_name, dose, method="tilt-administered"):
	"""Records a medication event. Call this from the Phase 3 tilt-sensor screen."""
	query = """
		INSERT INTO medications_administered (visit_id, medication_name, dose, method)
		VALUES (?, ?, ?, ?)
	"""
	system.db.runPrepUpdate(query, [visit_id, medication_name, dose, method], DB_CONNECTION)


def discharge(visit_id, instructions):
	"""Discharges a patient, stamping the discharge time and instructions."""
	query = """
		UPDATE visits
		SET status = 'discharged', discharged_at = now(), discharge_instructions = ?
		WHERE visit_id = ?
	"""
	system.db.runPrepUpdate(query, [instructions, visit_id], DB_CONNECTION)


def get_active_visits():
	"""Returns all visits currently checked in or in treatment — this is your 'patient board'."""
	query = """
		SELECT v.visit_id, v.status, v.chief_complaint, v.checked_in_at,
		       p.name, p.species, p.photo_url
		FROM visits v
		JOIN patients p ON p.patient_id = v.patient_id
		WHERE v.status IN ('checked_in', 'in_treatment')
		ORDER BY v.checked_in_at ASC
	"""
	return system.db.runQuery(query, DB_CONNECTION)