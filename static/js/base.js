// ClinicEase Client Scripts

// Patient Booking Modal Functions
function openBookingModal(slotId, date, time) {
    const slotIdInput = document.getElementById("modal-slot-id");
    const slotInfoText = document.getElementById("modal-slot-info");
    const purposeInput = document.getElementById("modal-purpose");
    const modal = document.getElementById("booking-modal");

    if (slotIdInput) slotIdInput.value = slotId;
    if (slotInfoText) slotInfoText.innerText = date + " at " + time + " (Slot #" + slotId + ")";
    if (purposeInput) purposeInput.value = "General Consultation";
    if (modal) modal.classList.remove("hidden");
}

function closeBookingModal() {
    const modal = document.getElementById("booking-modal");
    if (modal) modal.classList.add("hidden");
}

async function handleBookSlot(event) {
    event.preventDefault();
    const slotId = document.getElementById("modal-slot-id").value;
    const purpose = document.getElementById("modal-purpose").value;

    try {
        const res = await fetch("/api/slots/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ slot_id: parseInt(slotId), purpose: purpose })
        });
        const data = await res.json();

        if (res.ok && data.status === "success") {
            closeBookingModal();
            window.location.reload();
        } else {
            alert(data.message || "Failed to book slot.");
        }
    } catch (err) {
        alert("An unexpected error occurred while booking.");
    }
}

// Staff Appointment Actions
async function handleAppointmentAction(apptId, action) {
    if (!confirm("Are you sure you want to " + action + " appointment #" + apptId + "?")) {
        return;
    }

    try {
        const res = await fetch("/api/staff/appointments/" + apptId + "/action", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: action })
        });
        const data = await res.json();

        if (res.ok && data.status === "success") {
            window.location.reload();
        } else {
            alert(data.message || "Action failed.");
        }
    } catch (err) {
        alert("An unexpected error occurred.");
    }
}

// Staff Report Generator
async function generateReport() {
    try {
        const res = await fetch("/api/staff/report");
        const data = await res.json();

        if (res.ok && data.status === "success") {
            const reportCard = document.getElementById("report-card");
            const reportContent = document.getElementById("report-content");
            if (reportContent) reportContent.innerText = data.report.join("\n");
            if (reportCard) {
                reportCard.classList.remove("hidden");
                reportCard.scrollIntoView({ behavior: "smooth" });
            }
        } else {
            alert(data.message || "Failed to generate report.");
        }
    } catch (err) {
        alert("Error generating appointment report.");
    }
}
