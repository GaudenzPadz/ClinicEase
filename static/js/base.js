(() => {
    let toastTimer;

    function showToast(message, type = "success") {
        const toast = document.getElementById("app-toast");
        if (!toast) {
            console.error("ClinicEase notification region is missing.");
            return;
        }

        toast.textContent = message;
        toast.classList.toggle("toast-error", type === "error");
        toast.setAttribute("role", type === "error" ? "alert" : "status");
        toast.hidden = false;
        window.clearTimeout(toastTimer);
        toastTimer = window.setTimeout(() => {
            toast.hidden = true;
        }, 6000);
    }

    async function request(url, options = {}) {
        const response = await fetch(url, options);
        let data;

        try {
            data = await response.json();
        } catch {
            throw new Error("The server returned an unreadable response. Please try again.");
        }

        if (!response.ok || data.status === "error") {
            const error = new Error(data.message || "The request could not be completed.");
            error.status = response.status;
            throw error;
        }

        return data;
    }

    window.ClinicEase = Object.freeze({ request, showToast });
})();
