(() => {
    const modal = document.getElementById("booking-modal");
    const purposeInput = document.getElementById("modal-purpose");
    const phoneInput = document.getElementById("modal-contact-number");
    let bookingTrigger = null;

    function openBookingModal(button) {
        bookingTrigger = button;
        document.getElementById("modal-slot-id").value = button.dataset.slotId;
        document.getElementById("modal-slot-info").textContent =
            `${button.dataset.slotDate} at ${button.dataset.slotTime}`;
        purposeInput.value = "";
        phoneInput.value = phoneInput.dataset.defaultValue || "";
        const feedback = document.getElementById("booking-feedback");
        feedback.hidden = true;
        feedback.textContent = "";
        modal.classList.remove("hidden");
        modal.setAttribute("aria-hidden", "false");
        purposeInput.focus();
    }

    function closeBookingModal() {
        modal.classList.add("hidden");
        modal.setAttribute("aria-hidden", "true");
        bookingTrigger?.focus();
    }

    document.querySelectorAll("[data-slot-id]").forEach((button) => {
        button.addEventListener("click", () => openBookingModal(button));
    });

    modal.querySelector("[data-close-booking]").addEventListener("click", closeBookingModal);
    modal.addEventListener("click", (event) => {
        if (event.target === modal) closeBookingModal();
    });

    document.addEventListener("keydown", (event) => {
        if (modal.classList.contains("hidden")) return;

        if (event.key === "Escape") {
            closeBookingModal();
        } else if (event.key === "Tab") {
            const focusable = modal.querySelectorAll(
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

    document.getElementById("booking-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!window.confirm("Save this appointment?")) return;

        const form = event.currentTarget;
        const submitButton = form.querySelector('[type="submit"]');
        const feedback = document.getElementById("booking-feedback");
        feedback.hidden = true;
        feedback.textContent = "";
        submitButton.disabled = true;

        try {
            const result = await window.ClinicEase.request(form.action, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    slot_id: Number(document.getElementById("modal-slot-id").value),
                    purpose: purposeInput.value,
                    contact_number: phoneInput.value
                })
            });
            closeBookingModal();
            const message = [result.message, result.warning].filter(Boolean).join(" ");
            window.ClinicEase.showToast(
                message || "Your appointment request was submitted.",
                result.warning ? "error" : "success"
            );
            window.setTimeout(() => window.location.reload(), 2500);
        } catch (error) {
            feedback.textContent = error.message;
            feedback.hidden = false;
            window.ClinicEase.showToast(error.message, "error");
            if (error.status === 409) {
                closeBookingModal();
                window.setTimeout(() => window.location.reload(), 1800);
            }
        } finally {
            submitButton.disabled = false;
        }
    });
})();
