(() => {
    const tabs = [
        { button: document.getElementById("sign-in-tab"), panel: document.getElementById("sign-in-panel") },
        { button: document.getElementById("create-account-tab"), panel: document.getElementById("create-account-panel") }
    ];
    const authPage = document.querySelector(".auth-page");
    const signInForm = document.getElementById("sign-in-form");
    const createAccountForm = document.getElementById("create-account-form");
    const slotInput = document.getElementById("initial-slot-id");
    const calendar = document.getElementById("availability-calendar");
    const availableTimes = document.getElementById("available-times-list");
    const calendarFeedback = document.getElementById("calendar-feedback");
    const calendarInstructions = document.getElementById("calendar-instructions");
    const monthLabel = document.getElementById("calendar-month");
    const previousMonthButton = document.getElementById("calendar-previous");
    const nextMonthButton = document.getElementById("calendar-next");

    slotInput.name = "slot_id";

    const slotsByDate = new Map();
    document.querySelectorAll("[data-slot-option]").forEach((option) => {
        const date = option.dataset.slotDate;
        if (!slotsByDate.has(date)) slotsByDate.set(date, []);
        slotsByDate.get(date).push({
            id: option.dataset.slotId,
            time: option.dataset.slotTime
        });
    });

    const availableDates = [...slotsByDate.keys()].sort();
    const monthKeys = [...new Set(availableDates.map((date) => date.slice(0, 7)))];
    let displayedMonth = monthKeys[0] || monthKeyFromDate(new Date());
    let selectedDate = null;
    let selectedSlotId = slotInput.value;

    function parseLocalDate(isoDate) {
        const [year, month, day] = isoDate.split("-").map(Number);
        return new Date(year, month - 1, day, 12);
    }

    function monthDate(monthKey) {
        const [year, month] = monthKey.split("-").map(Number);
        return new Date(year, month - 1, 1, 12);
    }

    function monthKeyFromDate(date) {
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
    }

    function setCalendarFeedback(message) {
        calendarFeedback.textContent = message;
        calendarFeedback.hidden = !message;
        if (message) {
            calendar.setAttribute("aria-invalid", "true");
        } else {
            calendar.removeAttribute("aria-invalid");
        }
    }

    function renderAvailableTimes() {
        availableTimes.replaceChildren();
        if (!selectedDate) {
            calendarInstructions.textContent = slotsByDate.size
                ? "Choose a date on the calendar to see available times."
                : "No appointment times are currently available.";
            return;
        }

        const times = slotsByDate.get(selectedDate) || [];
        calendarInstructions.textContent =
            `${times.length} available ${times.length === 1 ? "time" : "times"} on ` +
            parseLocalDate(selectedDate).toLocaleDateString(undefined, {
                weekday: "long",
                month: "long",
                day: "numeric"
            }) +
            ".";

        times.forEach((slot) => {
            const button = document.createElement("button");
            button.className = "available-time-button";
            button.type = "button";
            button.textContent = slot.time;
            button.dataset.slotId = slot.id;
            button.setAttribute("aria-pressed", String(slot.id === selectedSlotId));
            button.addEventListener("click", () => {
                selectedSlotId = slot.id;
                slotInput.value = slot.id;
                calendarInstructions.textContent =
                    `Selected appointment: ${parseLocalDate(selectedDate).toLocaleDateString(undefined, {
                        weekday: "long",
                        month: "long",
                        day: "numeric"
                    })} at ${slot.time}.`;
                availableTimes.querySelectorAll(".available-time-button").forEach((timeButton) => {
                    timeButton.setAttribute(
                        "aria-pressed",
                        String(timeButton.dataset.slotId === selectedSlotId)
                    );
                });
                setCalendarFeedback("");
            });
            availableTimes.append(button);
        });
    }

    function selectDate(isoDate) {
        if (isoDate === selectedDate) return;
        selectedDate = isoDate;
        selectedSlotId = "";
        slotInput.value = "";
        setCalendarFeedback("");
        renderCalendar();
        renderAvailableTimes();
    }

    function renderCalendar() {
        const currentMonth = monthDate(displayedMonth);
        const year = currentMonth.getFullYear();
        const month = currentMonth.getMonth();
        monthLabel.textContent = currentMonth.toLocaleDateString(undefined, {
            month: "long",
            year: "numeric"
        });

        previousMonthButton.disabled = !monthKeys.some((key) => key < displayedMonth);
        nextMonthButton.disabled = !monthKeys.some((key) => key > displayedMonth);

        calendar.replaceChildren();
        ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].forEach((weekday) => {
            const label = document.createElement("span");
            label.className = "calendar-weekday";
            label.setAttribute("aria-hidden", "true");
            label.textContent = weekday;
            calendar.append(label);
        });

        const firstWeekday = new Date(year, month, 1, 12).getDay();
        const daysInMonth = new Date(year, month + 1, 0, 12).getDate();
        for (let blank = 0; blank < firstWeekday; blank += 1) {
            const spacer = document.createElement("span");
            spacer.className = "calendar-empty";
            spacer.setAttribute("aria-hidden", "true");
            calendar.append(spacer);
        }

        for (let day = 1; day <= daysInMonth; day += 1) {
            const isoDate = [
                year,
                String(month + 1).padStart(2, "0"),
                String(day).padStart(2, "0")
            ].join("-");
            const dateSlots = slotsByDate.get(isoDate);
            const button = document.createElement("button");
            button.className = "calendar-day";
            button.type = "button";
            button.textContent = String(day);
            button.disabled = !dateSlots;
            button.setAttribute("aria-pressed", String(isoDate === selectedDate));
            button.setAttribute(
                "aria-label",
                dateSlots
                    ? `${parseLocalDate(isoDate).toLocaleDateString(undefined, {
                          weekday: "long",
                          month: "long",
                          day: "numeric"
                      })}, ${dateSlots.length} available ${dateSlots.length === 1 ? "time" : "times"}`
                    : parseLocalDate(isoDate).toLocaleDateString(undefined, {
                          weekday: "long",
                          month: "long",
                          day: "numeric"
                      })
            );
            if (dateSlots) {
                button.classList.add("calendar-day--available");
                button.addEventListener("click", () => selectDate(isoDate));
            }
            calendar.append(button);
        }

        if (!slotsByDate.size) {
            calendarInstructions.textContent = "No appointment times are currently available.";
        }
    }

    previousMonthButton.addEventListener("click", () => {
        const date = monthDate(displayedMonth);
        date.setMonth(date.getMonth() - 1);
        displayedMonth = monthKeyFromDate(date);
        renderCalendar();
    });

    nextMonthButton.addEventListener("click", () => {
        const date = monthDate(displayedMonth);
        date.setMonth(date.getMonth() + 1);
        displayedMonth = monthKeyFromDate(date);
        renderCalendar();
    });

    if (selectedSlotId) {
        const restoredDate = availableDates.find((date) =>
            slotsByDate.get(date).some((slot) => slot.id === selectedSlotId)
        );
        if (restoredDate) {
            selectedDate = restoredDate;
            displayedMonth = restoredDate.slice(0, 7);
        } else {
            selectedSlotId = "";
            slotInput.value = "";
        }
    }
    renderCalendar();
    renderAvailableTimes();

    function activateTab(index, moveFocus = false) {
        tabs.forEach((tab, tabIndex) => {
            const active = tabIndex === index;
            tab.button.setAttribute("aria-selected", String(active));
            tab.button.tabIndex = active ? 0 : -1;
            tab.panel.hidden = !active;
        });
        authPage.classList.toggle("auth-page-create", index === 1);
        authPage.classList.toggle("auth-page-login", index === 0);
        if (moveFocus) tabs[index].button.focus();
    }

    function setFeedback(id, message, success = false) {
        const feedback = document.getElementById(id);
        feedback.textContent = message;
        feedback.classList.toggle("alert-success", success);
        feedback.classList.toggle("alert-error", !success);
        feedback.setAttribute("role", success ? "status" : "alert");
        feedback.hidden = false;
    }

    function clearFeedback(id) {
        const feedback = document.getElementById(id);
        feedback.textContent = "";
        feedback.classList.remove("alert-success");
        feedback.classList.add("alert-error");
        feedback.setAttribute("role", "alert");
        feedback.hidden = true;
    }

    tabs.forEach((tab, index) => {
        tab.button.addEventListener("click", () => activateTab(index));
        tab.button.addEventListener("keydown", (event) => {
            if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
            event.preventDefault();
            const next = (index + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
            activateTab(next, true);
        });
    });

    signInForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearFeedback("sign-in-feedback");
        const submitButton = signInForm.querySelector('[type="submit"]');
        submitButton.disabled = true;

        try {
            await window.ClinicEase.request(signInForm.dataset.apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(Object.fromEntries(new FormData(signInForm)))
            });
            window.location.assign(signInForm.dataset.dashboardUrl);
        } catch (error) {
            setFeedback("sign-in-feedback", error.message, false);
        } finally {
            submitButton.disabled = false;
        }
    });

    createAccountForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!slotInput.value) {
            setCalendarFeedback("Choose an available date and time before continuing.");
            calendar.focus();
            return;
        }
        if (!window.confirm(createAccountForm.dataset.confirmMessage)) return;

        clearFeedback("create-account-feedback");
        const submitButton = createAccountForm.querySelector('[type="submit"]');
        submitButton.disabled = true;

        try {
            const result = await window.ClinicEase.request(createAccountForm.dataset.apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(Object.fromEntries(new FormData(createAccountForm)))
            });
            window.location.assign(
                result.redirect_url || createAccountForm.dataset.dashboardUrl
            );
        } catch (error) {
            setFeedback("create-account-feedback", error.message, false);
        } finally {
            submitButton.disabled = false;
        }
    });
})();
