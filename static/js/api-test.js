(() => {
    const loginForm = document.getElementById("test-login-form");
    const slotsButton = document.getElementById("load-slots");
    const bookingForm = document.getElementById("test-booking-form");
    const slotTableBody = document.getElementById("slots-table-body");

    async function showResponse(elementId, callback) {
        const output = document.getElementById(elementId);
        try {
            const result = await callback();
            output.textContent = JSON.stringify(result, null, 2);
            return result;
        } catch (error) {
            output.textContent = error.message;
            return null;
        }
    }

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const result = await showResponse("login-response", () =>
            window.ClinicEase.request(loginForm.dataset.endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(Object.fromEntries(new FormData(loginForm)))
            })
        );
        if (result?.role) {
            document.getElementById("active-role").textContent = result.role;
        }
    });

    slotsButton.addEventListener("click", async () => {
        const result = await showResponse("slots-response", () =>
            window.ClinicEase.request(slotsButton.dataset.endpoint)
        );
        slotTableBody.replaceChildren();
        if (!result?.slots?.length) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");
            cell.colSpan = 4;
            cell.textContent = "No appointment times were returned.";
            row.append(cell);
            slotTableBody.append(row);
            return;
        }

        result.slots.forEach((slot) => {
            const row = document.createElement("tr");
            [slot.slot_id, slot.slot_date, slot.time, slot.status].forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value ?? "";
                row.append(cell);
            });
            slotTableBody.append(row);
        });
    });

    bookingForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const fields = Object.fromEntries(new FormData(bookingForm));
        fields.slot_id = Number(fields.slot_id);
        await showResponse("booking-response", () =>
            window.ClinicEase.request(bookingForm.dataset.endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(fields)
            })
        );
    });
})();
