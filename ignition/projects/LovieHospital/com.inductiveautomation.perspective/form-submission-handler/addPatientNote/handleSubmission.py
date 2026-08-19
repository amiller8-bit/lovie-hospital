def handleSubmission(session, name, data, files, formContext, sessionContext, retry):
	logger = system.util.getLogger("addPatientNote")
	logger.info("Received note submission: " + str(data))
	
	note_text = data.get("noteText", "").strip()
	
	if not note_text:
		response = {
			"success": False,
			"title": "Missing Note",
			"message": "Please write something before submitting.",
			"fieldErrors": {"noteText": {"title": "Required", "message": "Note can't be empty."}}
		}
	else:
		hospital.patients.add_note(1, note_text)  # hardcoded visit_id=1 for now, our test visit
		response = {"success": True, "title": "Note Saved", "message": "Added to the chart."}
	
	response