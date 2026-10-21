document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = [...document.querySelectorAll("[data-dashboard-tab]")];
    const tabPanels = [...document.querySelectorAll(".dashboard-tab-panel")];

    function activateDashboardTab(panelId, moveFocus = false) {
        tabButtons.forEach((button) => {
            const active = button.dataset.dashboardTab === panelId;
            button.classList.toggle("is-active", active);
            button.setAttribute("aria-selected", String(active));
            button.tabIndex = active ? 0 : -1;
            if (active && moveFocus) button.focus();
        });
        tabPanels.forEach((panel) => {
            panel.hidden = panel.id !== panelId;
        });
    }

    tabButtons.forEach((button, index) => {
        button.addEventListener("click", () => activateDashboardTab(button.dataset.dashboardTab));
        button.addEventListener("keydown", (event) => {
            if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
            event.preventDefault();
            const direction = event.key === "ArrowRight" ? 1 : -1;
            const nextIndex = (index + direction + tabButtons.length) % tabButtons.length;
            activateDashboardTab(tabButtons[nextIndex].dataset.dashboardTab, true);
        });
    });

    document.querySelectorAll("[data-open-tab]").forEach((button) => {
        button.addEventListener("click", () => {
            const targetPanel = button.dataset.openTab;
            activateDashboardTab(targetPanel);
            document.getElementById(
                tabButtons.find((tab) => tab.dataset.dashboardTab === targetPanel)?.id
            )?.focus();
        });
    });

    const slotData = [...document.querySelectorAll("[data-slot-option]")];
    const calendar = document.getElementById("availability-calendar");
    const monthLabel = document.getElementById("calendar-month");
    const previousMonthButton = document.getElementById("calendar-previous");
    const nextMonthButton = document.getElementById("calendar-next");
    const selectedDateLabel = document.getElementById("selected-date-label");
    const calendarFeedback = document.getElementById("calendar-feedback");
    const availableTimesList = document.getElementById("available-times-list");
    const timePanelDescription = document.getElementById("time-panel-description");
    const timeEmptyState = document.getElementById("time-empty-state");
    const detailsStepButton = document.getElementById("details-step-button");
    const selectionPanel = document.getElementById("booking-selection");
    const detailsPanel = document.getElementById("booking-details");
    const stepIndicators = [...document.querySelectorAll("[data-step-indicator]")];
    const slotInput = document.getElementById("selected-slot-id");
    const summaryDate = document.getElementById("booking-summary-date");
    const summaryTime = document.getElementById("booking-summary-time");
    const bookingForm = document.getElementById("booking-form");
    const bookingFeedback = document.getElementById("booking-feedback");
    const noSlotsMessage = document.getElementById("no-slots-message");

    const slotsByDate = new Map();
    slotData.forEach((slotElement) => {
        const date = slotElement.dataset.slotDate;
        const slotId = slotElement.dataset.slotId;
        const time = slotElement.dataset.slotTime;
        if (!date || !slotId || !time) return;
        if (!slotsByDate.has(date)) slotsByDate.set(date, []);
        slotsByDate.get(date).push({ id: slotId, time });
    });

    const availableDates = [...slotsByDate.keys()].sort();
    const monthKeys = [...new Set(availableDates.map((date) => date.slice(0, 7)))];
    let displayedMonth = monthKeys[0] || getMonthKey(new Date());
    let selectedDate = null;
    let selectedSlot = null;
    let currentStep = 1;

    function getMonthKey(date) {
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
    }

    function parseLocalDate(isoDate) {
        const [year, month, day] = isoDate.split("-").map(Number);
        return new Date(year, month - 1, day, 12);
    }

    function formatDate(isoDate, options = { weekday: "long", year: "numeric", month: "long", day: "numeric" }) {
        return parseLocalDate(isoDate).toLocaleDateString(undefined, options);
    }

    function showCalendarFeedback(message) {
        if (!calendarFeedback) return;
        calendarFeedback.textContent = message;
        calendarFeedback.hidden = !message;
    }

    function updateWizardStep(step) {
        currentStep = step;
        stepIndicators.forEach((indicator) => {
            const indicatorStep = Number(indicator.dataset.stepIndicator);
            indicator.classList.toggle("is-current", indicatorStep === step);
            indicator.classList.toggle("is-complete", indicatorStep < step);
            if (indicatorStep === step) {
                indicator.setAttribute("aria-current", "step");
            } else {
                indicator.removeAttribute("aria-current");
            }
        });

        if (selectionPanel) selectionPanel.hidden = step === 3;
        if (detailsPanel) detailsPanel.hidden = step !== 3;
        if (step === 3) {
            document.getElementById("booking-purpose")?.focus();
        } else if (step === 2) {
            availableTimesList?.querySelector(".time-slot-button")?.focus();
        }
    }

    function renderAvailableTimes() {
        if (!availableTimesList || !timeEmptyState || !timePanelDescription) return;
        availableTimesList.replaceChildren();

        if (!selectedDate) {
            timePanelDescription.textContent = "Select a date first to see available times.";
            timeEmptyState.hidden = false;
            timeEmptyState.querySelector("p").textContent =
                "Your available appointment times will appear here after you choose a date.";
            return;
        }

        const slots = slotsByDate.get(selectedDate) || [];
        timePanelDescription.textContent = formatDate(selectedDate);
        timeEmptyState.hidden = slots.length > 0;
        if (slots.length === 0) {
            timeEmptyState.querySelector("p").textContent = "No appointment times are available on this date.";
            return;
        }

        slots.forEach((slot) => {
            const button = document.createElement("button");
            button.className = "time-slot-button";
            button.type = "button";
            button.textContent = slot.time;
            button.setAttribute("aria-pressed", String(selectedSlot?.id === slot.id));
            if (selectedSlot?.id === slot.id) button.classList.add("is-selected");
            button.addEventListener("click", () => {
                selectedSlot = slot;
                if (slotInput) slotInput.value = slot.id;
                if (summaryDate) summaryDate.textContent = formatDate(selectedDate);
                if (summaryTime) summaryTime.textContent = slot.time;
                if (detailsStepButton) detailsStepButton.disabled = false;
                availableTimesList.querySelectorAll(".time-slot-button").forEach((timeButton) => {
                    const selected = timeButton === button;
                    timeButton.classList.toggle("is-selected", selected);
                    timeButton.setAttribute("aria-pressed", String(selected));
                });
                if (currentStep === 1) updateWizardStep(2);
            });
            availableTimesList.append(button);
        });
    }

    function selectDate(date) {
        if (!slotsByDate.has(date)) return;
        selectedDate = date;
        selectedSlot = null;
        if (slotInput) slotInput.value = "";
        if (detailsStepButton) detailsStepButton.disabled = true;
        if (selectedDateLabel) selectedDateLabel.textContent = `Selected date: ${formatDate(date)}.`;
        if (summaryDate) summaryDate.textContent = formatDate(date);
        if (summaryTime) summaryTime.textContent = "Not selected";
        showCalendarFeedback("");
        renderCalendar();
        renderAvailableTimes();
        updateWizardStep(2);
    }

    function renderCalendar() {
        if (!calendar || !monthLabel) return;
        const [year, month] = displayedMonth.split("-").map(Number);
        const currentMonth = new Date(year, month - 1, 1, 12);
        monthLabel.textContent = currentMonth.toLocaleDateString(undefined, {
            month: "long",
            year: "numeric"
        });

        if (previousMonthButton) {
            previousMonthButton.disabled = !monthKeys.some((key) => key < displayedMonth);
        }
        if (nextMonthButton) {
            nextMonthButton.disabled = !monthKeys.some((key) => key > displayedMonth);
        }

        calendar.replaceChildren();
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].forEach((weekday) => {
            const label = document.createElement("span");
            label.className = "calendar-weekday";
            label.setAttribute("aria-hidden", "true");
            label.textContent = weekday;
            calendar.append(label);
        });

        const firstWeekday = new Date(year, month - 1, 1, 12).getDay();
        const daysInMonth = new Date(year, month, 0, 12).getDate();
        for (let blank = 0; blank < firstWeekday; blank += 1) {
            const spacer = document.createElement("span");
            spacer.className = "calendar-empty";
            spacer.setAttribute("aria-hidden", "true");
            calendar.append(spacer);
        }

        const today = new Date();
        const todayKey = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
        for (let day = 1; day <= daysInMonth; day += 1) {
            const isoDate = `${displayedMonth}-${String(day).padStart(2, "0")}`;
            const button = document.createElement("button");
            button.className = "calendar-day";
            button.type = "button";
            button.textContent = String(day);
            button.disabled = !slotsByDate.has(isoDate);
            button.setAttribute("aria-pressed", String(isoDate === selectedDate));
            button.setAttribute(
                "aria-label",
                slotsByDate.has(isoDate)
                    ? `${formatDate(isoDate)}, available`
                    : formatDate(isoDate)
            );
            if (slotsByDate.has(isoDate)) {
                button.classList.add("calendar-day--available");
                button.addEventListener("click", () => selectDate(isoDate));
            }
            if (isoDate === todayKey) button.classList.add("calendar-day--today");
            if (isoDate === selectedDate) button.classList.add("calendar-day--selected");
            calendar.append(button);
        }
    }

    previousMonthButton?.addEventListener("click", () => {
        const [year, month] = displayedMonth.split("-").map(Number);
        displayedMonth = getMonthKey(new Date(year, month - 2, 1, 12));
        renderCalendar();
    });

    nextMonthButton?.addEventListener("click", () => {
        const [year, month] = displayedMonth.split("-").map(Number);
        displayedMonth = getMonthKey(new Date(year, month, 1, 12));
        renderCalendar();
    });

    detailsStepButton?.addEventListener("click", () => {
        if (!selectedDate || !selectedSlot) {
            showCalendarFeedback("Choose a date and time before continuing.");
            return;
        }
        updateWizardStep(3);
    });

    document.getElementById("back-to-times")?.addEventListener("click", () => {
        updateWizardStep(2);
    });

    if (noSlotsMessage && slotData.length > 0) noSlotsMessage.hidden = true;
    renderCalendar();
    renderAvailableTimes();

    const appointmentModal = document.getElementById("appointment-modal");
    const modalDialog = appointmentModal?.querySelector('[role="dialog"]');
    const cancelAppointmentButton = document.getElementById("cancel-appointment-button");
    const modalFeedback = document.getElementById("modal-feedback");
    let modalTrigger = null;
    let currentAppointmentId = null;

    function openAppointmentDetails(card) {
        if (!appointmentModal || !modalDialog) return;
        modalTrigger = card;
        currentAppointmentId = card.dataset.apptId || null;

        const fields = {
            "modal-date": card.dataset.apptDate,
            "modal-time": card.dataset.apptTime,
            "modal-purpose": card.dataset.apptPurpose,
            "modal-contact": card.dataset.apptContact,
            "modal-id": `#${card.dataset.apptId || ""}`,
            "modal-created": card.dataset.apptCreated
        };
        Object.entries(fields).forEach(([id, value]) => {
            const field = document.getElementById(id);
            if (field) field.textContent = value || "Not provided";
        });

        const status = card.dataset.apptStatus || "Unknown";
        const statusBadge = document.getElementById("modal-status-badge");
        const modalStatus = document.getElementById("modal-status");
        const statusIcons = {
            Pending: "schedule",
            Confirmed: "check_circle",
            Completed: "task_alt",
            Cancelled: "cancel"
        };
        if (statusBadge) {
            statusBadge.className = `status-badge status-${status.toLowerCase()}`;
            statusBadge.replaceChildren();
            const icon = document.createElement("span");
            icon.className = "material-symbols-outlined";
            icon.setAttribute("aria-hidden", "true");
            icon.textContent = statusIcons[status] || "event";
            statusBadge.append(icon, document.createTextNode(status));
        }
        if (modalStatus) modalStatus.textContent = status;
        if (cancelAppointmentButton) {
            cancelAppointmentButton.hidden = !["Pending", "Confirmed"].includes(status);
        }
        if (modalFeedback) {
            modalFeedback.hidden = true;
            modalFeedback.textContent = "";
        }

        appointmentModal.hidden = false;
        appointmentModal.classList.remove("hidden");
        appointmentModal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
        appointmentModal.querySelector("[data-close-appointment-modal]")?.focus();
    }

    function closeAppointmentDetails() {
        if (!appointmentModal) return;
        appointmentModal.hidden = true;
        appointmentModal.classList.add("hidden");
        appointmentModal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
        currentAppointmentId = null;
        modalTrigger?.focus();
    }

    document.querySelectorAll("[data-appointment-details]").forEach((card) => {
        card.addEventListener("click", () => openAppointmentDetails(card));
    });

    appointmentModal?.querySelectorAll("[data-close-appointment-modal]").forEach((button) => {
        button.addEventListener("click", closeAppointmentDetails);
    });

    appointmentModal?.addEventListener("click", (event) => {
        if (event.target === appointmentModal) closeAppointmentDetails();
    });

    cancelAppointmentButton?.addEventListener("click", async () => {
        if (!currentAppointmentId || !window.ClinicEase) return;
        if (!window.confirm("Are you sure you want to cancel this appointment?")) return;

        cancelAppointmentButton.disabled = true;
        if (modalFeedback) {
            modalFeedback.hidden = true;
            modalFeedback.textContent = "";
        }

        try {
            const result = await window.ClinicEase.request(
                `/api/patient/appointments/${encodeURIComponent(currentAppointmentId)}/cancel`,
                { method: "POST" }
            );
            window.ClinicEase.showToast(result.message || "Appointment cancelled.", "success");
            closeAppointmentDetails();
            window.setTimeout(() => window.location.reload(), 1200);
        } catch (error) {
            if (modalFeedback) {
                modalFeedback.textContent = error.message;
                modalFeedback.hidden = false;
            }
            window.ClinicEase.showToast(error.message, "error");
        } finally {
            cancelAppointmentButton.disabled = false;
        }
    });

    bookingForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!bookingForm || !window.ClinicEase) return;
        if (!selectedSlot || !slotInput?.value) {
            updateWizardStep(2);
            showCalendarFeedback("Choose an available date and time before submitting.");
            return;
        }
        if (!bookingForm.reportValidity()) return;

        const submitButton = document.getElementById("submit-booking");
        if (submitButton) submitButton.disabled = true;
        if (bookingFeedback) {
            bookingFeedback.hidden = true;
            bookingFeedback.textContent = "";
        }

        try {
            const result = await window.ClinicEase.request(bookingForm.action, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    slot_id: Number(slotInput.value),
                    purpose: document.getElementById("booking-purpose")?.value || "",
                    contact_number: document.getElementById("booking-contact")?.value || ""
                })
            });
            const message = [result.message, result.warning].filter(Boolean).join(" ");
            window.ClinicEase.showToast(
                message || "Your appointment request was submitted.",
                result.warning ? "error" : "success"
            );
            window.setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            if (bookingFeedback) {
                bookingFeedback.textContent = error.message;
                bookingFeedback.hidden = false;
            }
            window.ClinicEase.showToast(error.message, "error");
            if (error.status === 409) {
                window.setTimeout(() => window.location.reload(), 1500);
            } else if (submitButton) {
                submitButton.disabled = false;
            }
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && appointmentModal && !appointmentModal.hidden) {
            closeAppointmentDetails();
        }

        if (event.key !== "Tab" || !appointmentModal || appointmentModal.hidden || !modalDialog) return;
        const focusable = [...modalDialog.querySelectorAll(
            'button:not(:disabled), a[href], input:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])'
        )].filter((element) => !element.hidden);
        if (!focusable.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    });
});
