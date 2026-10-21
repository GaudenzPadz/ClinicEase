document.addEventListener("DOMContentLoaded", () => {
    const navItems = [...document.querySelectorAll(".nav-item[data-section]")];
    const contentSections = [...document.querySelectorAll(".content-section")];
    let dashboardStatsLoaded = false;
    let statusChart;
    let weeklyChart;

    function switchSection(sectionId) {
        navItems.forEach((item) => {
            const active = item.dataset.section === sectionId;
            item.classList.toggle("active", active);
            item.setAttribute("aria-current", active ? "page" : "false");
        });
        contentSections.forEach((section) => {
            section.classList.toggle("active", section.id === `${sectionId}-section`);
        });
        if (sectionId === "dashboard" && !dashboardStatsLoaded) {
            loadDashboardStats();
        }
    }

    navItems.forEach((item) => {
        item.addEventListener("click", () => switchSection(item.dataset.section));
    });

    document.querySelectorAll("[data-nav]").forEach((button) => {
        button.addEventListener("click", () => switchSection(button.dataset.nav));
    });

    function setStatValue(id, value) {
        const element = document.getElementById(id);
        if (element) element.textContent = String(value);
    }

    function renderPendingTrend(trend) {
        const container = document.getElementById("pending-trend");
        if (!container) return;

        const direction = ["up", "down", "flat"].includes(trend?.direction)
            ? trend.direction
            : "flat";
        const iconNames = {
            up: "trending_up",
            down: "trending_down",
            flat: "trending_flat"
        };
        const descriptions = {
            up: "More new requests than last week",
            down: "Fewer new requests than last week",
            flat: "Same new requests as last week"
        };
        container.replaceChildren();
        container.className = `stat-trend stat-trend--${direction}`;

        const icon = document.createElement("span");
        icon.className = "material-symbols-outlined";
        icon.setAttribute("aria-hidden", "true");
        icon.textContent = iconNames[direction];
        container.append(icon, document.createTextNode(descriptions[direction]));
    }

    function renderCharts(stats) {
        const statusCanvas = document.getElementById("appointment-status-chart");
        const weeklyCanvas = document.getElementById("weekly-bookings-chart");
        if (!statusCanvas || !weeklyCanvas) return;
        if (typeof window.Chart !== "function") {
            window.ClinicEase?.showToast(
                "Dashboard data loaded, but the charts could not be displayed.",
                "error"
            );
            return;
        }

        const statusLabels = ["Pending", "Confirmed", "Completed", "Cancelled"];
        const statusColors = ["#D9A441", "#4F78B8", "#4B855D", "#C25C56"];
        const statusCounts = stats.status_counts || {};
        const weekLabels = Array.isArray(stats.weekly_bookings)
            ? stats.weekly_bookings.map((day) => day.day)
            : [];
        const weekCounts = Array.isArray(stats.weekly_bookings)
            ? stats.weekly_bookings.map((day) => day.count)
            : [];

        statusChart?.destroy();
        weeklyChart?.destroy();
        statusChart = new window.Chart(statusCanvas, {
            type: "doughnut",
            data: {
                labels: statusLabels,
                datasets: [{
                    data: statusLabels.map((status) => statusCounts[status] || 0),
                    backgroundColor: statusColors,
                    borderColor: "#FFFFFF",
                    borderWidth: 3,
                    hoverOffset: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "58%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { color: "#34443A", padding: 16, usePointStyle: true }
                    }
                }
            }
        });

        weeklyChart = new window.Chart(weeklyCanvas, {
            type: "bar",
            data: {
                labels: weekLabels,
                datasets: [{
                    label: "Appointments",
                    data: weekCounts,
                    backgroundColor: "#6B8D72",
                    borderColor: "#486B52",
                    borderWidth: 1,
                    borderRadius: 6,
                    maxBarThickness: 44
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: "#46534A" }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0, color: "#46534A" },
                        grid: { color: "#E7EBE5" }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: true }
                }
            }
        });
    }

    async function loadDashboardStats() {
        const dashboard = document.getElementById("dashboard-section");
        if (!dashboard || !window.ClinicEase) return;

        try {
            const stats = await window.ClinicEase.request(dashboard.dataset.statsUrl);
            const pendingCount = stats.status_counts?.Pending ?? 0;
            setStatValue("stat-pending-count", pendingCount);
            setStatValue("stat-confirmed-count", stats.confirmed_this_week ?? 0);
            setStatValue("stat-completed-count", stats.completed_this_month ?? 0);
            setStatValue("stat-available-slots", stats.available_slots_next_7_days ?? 0);
            renderPendingTrend(stats.pending_trend);
            renderCharts(stats);
            dashboardStatsLoaded = true;
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
        }
    }

    const reportButton = document.getElementById("generate-report-btn");
    const reportContent = document.getElementById("report-content");
    reportButton?.addEventListener("click", async () => {
        if (!reportContent || !window.ClinicEase) return;
        reportButton.disabled = true;
        try {
            const result = await window.ClinicEase.request(reportButton.dataset.endpoint);
            reportContent.textContent = (result.report || []).join("\n");
            reportContent.classList.remove("hidden");
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
        } finally {
            reportButton.disabled = false;
        }
    });

    document.querySelectorAll("[data-appointment-action]").forEach((button) => {
        button.addEventListener("click", async () => {
            const action = button.dataset.appointmentAction;
            const appointmentId = button.dataset.appointmentId;
            const label = action === "confirm"
                ? "approve"
                : action === "cancel"
                    ? "reject"
                    : "mark as completed";
            if (!window.confirm(`Are you sure you want to ${label} appointment #${appointmentId}?`)) {
                return;
            }

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
                window.setTimeout(() => window.location.reload(), 1500);
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
        const monthValue = new FormData(generateSlotsForm).get("month");
        if (!submitButton || typeof monthValue !== "string" || !monthValue) return;

        submitButton.disabled = true;
        try {
            const [year, month] = monthValue.split("-").map(Number);
            const result = await window.ClinicEase.request(generateSlotsForm.action, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ year, month })
            });
            window.ClinicEase.showToast(result.message || "Monthly slots generated.", "success");
            window.setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
            submitButton.disabled = false;
        }
    });

    const blockedDateForm = document.getElementById("blocked-date-form");
    blockedDateForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = blockedDateForm.querySelector('[type="submit"]');
        if (!submitButton) return;

        submitButton.disabled = true;
        try {
            const result = await window.ClinicEase.request(blockedDateForm.action, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(Object.fromEntries(new FormData(blockedDateForm)))
            });
            window.ClinicEase.showToast(result.message || "Clinic closure saved.", "success");
            window.setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
            submitButton.disabled = false;
        }
    });

    document.querySelectorAll("[data-slot-action]").forEach((button) => {
        button.addEventListener("click", async () => {
            const action = button.dataset.slotAction;
            const slotId = button.dataset.slotId;
            if (action === "delete" && !window.confirm(`Remove appointment time #${slotId}?`)) return;

            button.disabled = true;
            try {
                const result = await window.ClinicEase.request(button.dataset.endpoint, {
                    method: action === "delete" ? "DELETE" : "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action })
                });
                window.ClinicEase.showToast(result.message || "Appointment time updated.", "success");
                window.setTimeout(() => window.location.reload(), 1500);
            } catch (error) {
                window.ClinicEase.showToast(error.message, "error");
                button.disabled = false;
            }
        });
    });

    const editSlotModal = document.getElementById("edit-slot-modal");
    const editSlotForm = document.getElementById("edit-slot-form");
    let editSlotTrigger = null;

    function closeEditSlotModal() {
        if (!editSlotModal) return;
        editSlotModal.classList.add("hidden");
        editSlotModal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
        editSlotTrigger?.focus();
    }

    document.querySelectorAll("[data-edit-slot]").forEach((button) => {
        button.addEventListener("click", () => {
            if (!editSlotModal || !editSlotForm) return;
            editSlotTrigger = button;
            editSlotForm.action = button.dataset.endpoint;
            const dateInput = document.getElementById("edit-slot-date");
            const timeInput = document.getElementById("edit-slot-time");
            if (dateInput) dateInput.value = button.dataset.slotDate || "";
            if (timeInput) timeInput.value = button.dataset.slotTime || "";
            editSlotModal.classList.remove("hidden");
            editSlotModal.setAttribute("aria-hidden", "false");
            document.body.classList.add("modal-open");
            dateInput?.focus();
        });
    });

    editSlotModal?.querySelector("[data-close-edit-slot]")?.addEventListener(
        "click",
        closeEditSlotModal
    );
    editSlotModal?.addEventListener("click", (event) => {
        if (event.target === editSlotModal) closeEditSlotModal();
    });

    editSlotForm?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = editSlotForm.querySelector('[type="submit"]');
        if (!submitButton || !window.ClinicEase) return;

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
            window.ClinicEase.showToast(result.message || "Appointment time updated.", "success");
            window.setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            window.ClinicEase.showToast(error.message, "error");
        } finally {
            submitButton.disabled = false;
        }
    });

    function updateSlotCalendar() {
        const days = [...document.querySelectorAll("[data-calendar-day]")];
        const fromDate = document.getElementById("slot-from-date")?.value || "";
        const toDate = document.getElementById("slot-to-date")?.value || "";
        const showMoreButton = document.getElementById("show-more-slots");
        const emptyMessage = document.getElementById("slot-filter-empty");
        const resultCount = document.getElementById("slot-results-count");
        const clearButton = document.getElementById("clear-slot-filters");
        const hasCustomFilter = Boolean(fromDate || toDate);
        const isExpanded = showMoreButton?.dataset.expanded === "true";
        const invalidRange = Boolean(fromDate && toDate && fromDate > toDate);
        let visibleCount = 0;

        days.forEach((day) => {
            const slotDate = day.dataset.slotDate || "";
            let visible = !invalidRange;
            if (fromDate && slotDate < fromDate) visible = false;
            if (toDate && slotDate > toDate) visible = false;
            if (!hasCustomFilter && !isExpanded && Number(day.dataset.dayIndex) >= 7) {
                visible = false;
            }
            if (visible) {
                visibleCount += day.querySelectorAll(".calendar-slot").length;
            }
            day.hidden = !visible;
        });

        if (emptyMessage) {
            emptyMessage.hidden = visibleCount > 0;
            emptyMessage.textContent = invalidRange
                ? "The start date must be on or before the end date."
                : days.length === 0
                    ? "No appointment times are currently available."
                    : "No appointment times match these dates.";
        }
        if (resultCount) {
            resultCount.textContent = hasCustomFilter
                ? `Showing ${visibleCount} matching appointment time${visibleCount === 1 ? "" : "s"}.`
                : `Showing ${visibleCount} appointment time${visibleCount === 1 ? "" : "s"}${isExpanded ? " from today through 14 days ahead." : " in the next 7 days."}`;
        }
        if (showMoreButton) {
            showMoreButton.hidden = hasCustomFilter || days.length <= 7;
            showMoreButton.textContent = isExpanded ? "Show fewer dates" : "Show more dates";
        }
        if (clearButton) clearButton.disabled = !hasCustomFilter;
    }

    const fromDateInput = document.getElementById("slot-from-date");
    const toDateInput = document.getElementById("slot-to-date");
    fromDateInput?.addEventListener("change", updateSlotCalendar);
    toDateInput?.addEventListener("change", updateSlotCalendar);
    document.getElementById("clear-slot-filters")?.addEventListener("click", () => {
        if (fromDateInput) fromDateInput.value = "";
        if (toDateInput) toDateInput.value = "";
        updateSlotCalendar();
    });
    document.getElementById("show-more-slots")?.addEventListener("click", (event) => {
        const button = event.currentTarget;
        button.dataset.expanded = button.dataset.expanded !== "true" ? "true" : "false";
        updateSlotCalendar();
    });
    updateSlotCalendar();

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && editSlotModal && !editSlotModal.classList.contains("hidden")) {
            closeEditSlotModal();
        }
    });

    if (document.getElementById("dashboard-section")?.classList.contains("active")) {
        loadDashboardStats();
    }
});
