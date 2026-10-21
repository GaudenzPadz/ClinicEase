(() => {
    const reportCard = document.getElementById("report-card");
    const reportContent = document.getElementById("report-content");
    const reportButton = document.getElementById("report-button");

    reportButton?.addEventListener("click", async () => {
        reportButton.disabled = true;
        try {
            const result = await window.ClinicEase.request(reportButton.dataset.endpoint);
            reportContent.textContent = (result.report || []).join("\n");
            reportCard.classList.remove("hidden");
            reportCard.setAttribute("aria-hidden", "false");
            reportCard.scrollIntoView({
                behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"
            });
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
        } finally {
            reportButton.disabled = false;
        }
    });

    document.getElementById("close-report")?.addEventListener("click", () => {
        reportCard.classList.add("hidden");
        reportCard.setAttribute("aria-hidden", "true");
        reportButton.focus();
    });

    document.querySelectorAll("[data-appointment-action]").forEach((button) => {
        button.addEventListener("click", async () => {
            const action = button.dataset.appointmentAction;
            const appointmentId = button.dataset.appointmentId;
            const label = action === "confirm" ? "approve" : action === "cancel" ? "reject" : "mark as completed";
            if (!window.confirm(`Are you sure you want to ${label} appointment #${appointmentId}?`)) return;

            button.disabled = true;
            try {
                const result = await window.ClinicEase.request(button.dataset.endpoint, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action })
                });
                const message = [result.message, result.warning].filter(Boolean).join(" ");
                window.ClinicEase.showToast(
                    message || "Appointment updated.",
                    result.warning ? "error" : "success"
                );
                window.setTimeout(() => window.location.reload(), 1800);
            } catch (error) {
                window.ClinicEase.showToast(error.message, "error");
                button.disabled = false;
            }
        });
    });

    const generateSlotsForm = document.getElementById("generate-slots-form");
    generateSlotsForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = generateSlotsForm.querySelector('[type="submit"]');
        submitButton.disabled = true;
        try {
            const [year, month] = new FormData(generateSlotsForm).get("month").split("-").map(Number);
            const result = await window.ClinicEase.request(generateSlotsForm.action, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ year, month })
            });
            window.ClinicEase.showToast(result.message || "Monthly slots generated.");
            window.setTimeout(() => window.location.reload(), 1800);
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
            submitButton.disabled = false;
        }
    });

    const blockedDateForm = document.getElementById("blocked-date-form");
    blockedDateForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = blockedDateForm.querySelector('[type="submit"]');
        submitButton.disabled = true;
        try {
            const result = await window.ClinicEase.request(blockedDateForm.action, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(Object.fromEntries(new FormData(blockedDateForm)))
            });
            window.ClinicEase.showToast(result.message || "Clinic closure saved.");
            window.setTimeout(() => window.location.reload(), 1800);
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
            submitButton.disabled = false;
        }
    });

    document.querySelectorAll("[data-slot-action]").forEach((button) => {
        button.addEventListener("click", async () => {
            const action = button.dataset.slotAction;
            const slotId = button.dataset.slotId;
            if (action === "delete" && !window.confirm(`Remove available time #${slotId}?`)) return;

            button.disabled = true;
            try {
                const result = await window.ClinicEase.request(button.dataset.endpoint, {
                    method: action === "delete" ? "DELETE" : "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action })
                });
                window.ClinicEase.showToast(result.message || "Appointment time updated.");
                window.setTimeout(() => window.location.reload(), 1800);
            } catch (error) {
                window.ClinicEase.showToast(error.message, "error");
                button.disabled = false;
            }
        });
    });

    const editSlotModal = document.getElementById("edit-slot-modal");
    const editSlotForm = document.getElementById("edit-slot-form");
    let editSlotTrigger;

    document.querySelectorAll("[data-edit-slot]").forEach((button) => {
        button.addEventListener("click", () => {
            editSlotTrigger = button;
            editSlotForm.action = button.dataset.endpoint;
            document.getElementById("edit-slot-date").value = button.dataset.slotDate;
            document.getElementById("edit-slot-time").value = button.dataset.slotTime;
            editSlotModal.classList.remove("hidden");
            editSlotModal.setAttribute("aria-hidden", "false");
            document.getElementById("edit-slot-date").focus();
        });
    });

    function closeEditSlotModal() {
        editSlotModal.classList.add("hidden");
        editSlotModal.setAttribute("aria-hidden", "true");
        editSlotTrigger?.focus();
    }

    editSlotModal.querySelector("[data-close-edit-slot]").addEventListener("click", closeEditSlotModal);
    editSlotModal.addEventListener("click", (event) => {
        if (event.target === editSlotModal) closeEditSlotModal();
    });

    editSlotForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = editSlotForm.querySelector('[type="submit"]');
        submitButton.disabled = true;
        try {
            const result = await window.ClinicEase.request(editSlotForm.action, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ...Object.fromEntries(new FormData(editSlotForm)),
                    action: "update"
                })
            });
            closeEditSlotModal();
            window.ClinicEase.showToast(result.message || "Appointment time updated.");
            window.setTimeout(() => window.location.reload(), 1800);
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
        } finally {
            submitButton.disabled = false;
        }
    });

    document.addEventListener("keydown", (event) => {
        if (editSlotModal.classList.contains("hidden")) return;

        if (event.key === "Escape") {
            closeEditSlotModal();
        } else if (event.key === "Tab") {
            const focusable = editSlotModal.querySelectorAll(
                'button:not(:disabled), input:not(:disabled), textarea:not(:disabled), select:not(:disabled), a[href], [tabindex]:not([tabindex="-1"])'
            );
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        }
    });
})();
