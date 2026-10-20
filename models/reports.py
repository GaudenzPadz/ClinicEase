# Generator Pattern: Memory-efficient streaming of appointment reports
def generate_appointment_report(appointments_list):
    for appt in appointments_list:
        appt_id = appt.get("appointment_id", "N/A")
        patient_name = appt.get("patient_name", "Unknown Patient")
        status = appt.get("status", "Unknown Status")
        purpose = appt.get("purpose", "General")
        date = appt.get("slot_date", "N/A")
        time = appt.get("time", "N/A")

        yield (
            f"[Appt #{appt_id}] Patient: {patient_name} | "
            f"Schedule: {date} at {time} | "
            f"Purpose: {purpose} | Status: {status}"
        )
