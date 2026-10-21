# ClinicEase Project Source Code Compilation

**Generated on:** 10/22/2026 01:44:21

---

## File: $relativePath

``html
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HCI-Optimized Interactive Slot Scheduler</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(148, 163, 184, 0.3);
            border-radius: 9999px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.6);
        }
        .focus-ring {
            @apply focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900;
        }
    </style>
</head>
<body class="bg-slate-950 dark:bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-indigo-500 selection:text-white transition-colors duration-300">

    <div class="max-w-7xl mx-auto w-full p-3 sm:p-6 flex-1 flex flex-col">
        
        <!-- Top App Bar & Navigation Header (HCI Rule: Visual Hierarchy & Feedback) -->
        <header class="bg-slate-900/90 dark:bg-slate-900/90 backdrop-blur border border-slate-800 rounded-2xl p-4 mb-4 shadow-xl flex flex-col lg:flex-row justify-between items-center gap-4">
            
            <!-- Left Branding & Date Title -->
            <div class="flex items-center gap-3.5 w-full lg:w-auto">
                <div class="p-3 bg-indigo-600/20 border border-indigo-500/30 rounded-xl text-indigo-400 shrink-0 shadow-inner" aria-hidden="true">
                    <i class="fa-solid fa-calendar-week text-xl"></i>
                </div>
                <div class="flex-1">
                    <h1 id="viewDateRangeDisplay" class="text-lg sm:text-xl font-extrabold text-white tracking-wide flex items-center gap-2">
                        <span>Loading...</span>
                    </h1>
                    <p class="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                        <span id="activeViewSubtitle" class="font-medium text-slate-300">Month Overview</span>
                        <span class="inline-block w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span>
                        <span class="text-indigo-400 font-medium"><i class="fa-regular fa-clock mr-1" aria-hidden="true"></i>Interactive Scheduling Engine</span>
                    </p>
                </div>
            </div>

            <!-- Search, View Switchers, Theme & Nav Buttons -->
            <div class="flex flex-wrap items-center justify-between lg:justify-end gap-2.5 w-full lg:w-auto">
                
                <!-- Search Filter (HCI: Immediate Feedback & Flexibility) -->
                <div class="relative flex-1 sm:flex-none">
                    <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
                    <input 
                        type="text" 
                        id="searchInput" 
                        placeholder="Search booked slots..." 
                        class="w-full sm:w-44 pl-8 pr-3 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                        aria-label="Search appointments"
                    />
                </div>

                <!-- View Mode Selector (Fitts's Law: Adequate touch target padding) -->
                <nav aria-label="Calendar view navigation" class="bg-slate-950 border border-slate-800 p-1 rounded-xl flex items-center gap-1 text-xs font-semibold text-slate-400">
                    <button data-view="month" class="view-btn px-3 py-1.5 rounded-lg transition active:scale-95 focus-ring">Month</button>
                    <button data-view="week" class="view-btn px-3 py-1.5 rounded-lg transition active:scale-95 focus-ring">Week</button>
                    <button data-view="3day" class="view-btn px-3 py-1.5 rounded-lg transition active:scale-95 focus-ring">3 Days</button>
                    <button data-view="today" class="view-btn px-3 py-1.5 rounded-lg transition active:scale-95 focus-ring">Today</button>
                </nav>

                <!-- Navigation Controls -->
                <div class="flex items-center gap-1 bg-slate-950 border border-slate-800 p-1 rounded-xl">
                    <button id="todayNavBtn" class="px-3 py-1.5 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg transition active:scale-95 focus-ring" title="Shortcut: Press 'T'">
                        Today
                    </button>
                    <div class="h-4 w-px bg-slate-800 mx-0.5"></div>
                    <button id="prevNavBtn" class="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition active:scale-95 focus-ring" aria-label="Previous Period">
                        <i class="fa-solid fa-chevron-left text-xs" aria-hidden="true"></i>
                    </button>
                    <button id="nextNavBtn" class="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition active:scale-95 focus-ring" aria-label="Next Period">
                        <i class="fa-solid fa-chevron-right text-xs" aria-hidden="true"></i>
                    </button>
                </div>
            </div>
        </header>

        <!-- Main Dynamic View Container -->
        <main id="viewContainer" class="flex-1 bg-slate-900/60 border border-slate-800/80 rounded-2xl p-3 sm:p-5 shadow-2xl flex flex-col min-h-[600px] overflow-hidden relative">
            <!-- Dynamic calendar grids rendered here -->
        </main>

        <!-- HCI Helper Keyboard Shortcut Footer Bar -->
        <footer class="mt-3 text-[11px] text-slate-500 flex flex-wrap justify-between items-center px-2 gap-2">
            <div class="flex items-center gap-3">
                <span class="flex items-center gap-1"><kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300 font-mono text-[10px]">T</kbd> Jump Today</span>
                <span class="flex items-center gap-1"><kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300 font-mono text-[10px]">Esc</kbd> Close Dialog</span>
                <span class="flex items-center gap-1"><kbd class="px-1.5 py-0.5 bg-slate-800 border border-slate-700 rounded text-slate-300 font-mono text-[10px]">← / →</kbd> Navigate</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Open Slot
                <span class="w-2 h-2 rounded-full bg-indigo-500 ml-2"></span> Booked
            </div>
        </footer>
    </div>

    <!-- Booking & Available Slots Modal -->
    <div id="slotBookingModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center hidden z-50 p-4 transition-opacity duration-200" role="dialog" aria-modal="true" aria-labelledby="modalDateTitle">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden transform transition-all duration-200 scale-95 opacity-0" id="modalContainer">
            
            <!-- Modal Header -->
            <div class="px-6 py-4 bg-slate-950/70 border-b border-slate-800 flex justify-between items-center">
                <div class="flex items-center gap-3">
                    <div class="p-2.5 bg-indigo-600/20 border border-indigo-500/30 rounded-xl text-indigo-400">
                        <i class="fa-regular fa-calendar-check text-lg"></i>
                    </div>
                    <div>
                        <h3 id="modalDateTitle" class="text-base font-bold text-slate-100">Daily Slots Overview</h3>
                        <p id="modalDateSub" class="text-xs text-slate-400">Select an open slot to schedule your appointment</p>
                    </div>
                </div>
                <button id="closeModalBtn" class="text-slate-400 hover:text-white p-2 rounded-xl hover:bg-slate-800 transition focus-ring" aria-label="Close dialog">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>

            <!-- Modal Content Body -->
            <div class="p-6 space-y-6 max-h-[75vh] overflow-y-auto custom-scrollbar">
                
                <!-- Time Slots Grid (HCI Rule: Recognition over Recall - Visual Slot Grid) -->
                <div>
                    <div class="flex justify-between items-center mb-3">
                        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Hourly Availability Grid</span>
                        <span class="text-[11px] text-indigo-400 font-medium"><i class="fa-solid fa-circle-info mr-1"></i>Click open slot to select</span>
                    </div>
                    <div id="timeSlotsGrid" class="grid grid-cols-3 sm:grid-cols-4 gap-2">
                        <!-- Dynamic slots -->
                    </div>
                </div>

                <!-- Selected Slot Booking Form (HCI Rule: Error Prevention & Feedback) -->
                <form id="bookingForm" class="hidden space-y-4 pt-4 border-t border-slate-800/80 animate-fadeIn">
                    <div class="bg-indigo-950/40 border border-indigo-500/30 rounded-xl p-3 flex justify-between items-center">
                        <div class="flex items-center gap-2">
                            <i class="fa-regular fa-clock text-indigo-400 text-sm"></i>
                            <span class="text-xs text-slate-300 font-medium">Selected Slot:</span>
                            <span id="selectedSlotBadge" class="text-xs font-extrabold text-indigo-300 bg-indigo-600/30 border border-indigo-500/40 px-2.5 py-1 rounded-lg">--:--</span>
                        </div>
                        <button type="button" id="clearSlotSelection" class="text-xs text-slate-400 hover:text-slate-200 transition underline underline-offset-2">Change slot</button>
                    </div>

                    <div>
                        <label for="apptTitleInput" class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">
                            Appointment Title <span class="text-rose-400">*</span>
                        </label>
                        <input
                            type="text"
                            id="apptTitleInput"
                            placeholder="e.g., Client Sync / Project Review"
                            class="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
                            required
                        />
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label for="apptCategoryInput" class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Category</label>
                            <select id="apptCategoryInput" class="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition">
                                <option value="indigo">Work</option>
                                <option value="emerald">Personal</option>
                                <option value="amber">Urgent</option>
                                <option value="rose">Health</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Duration</label>
                            <input
                                type="text"
                                value="60 min"
                                disabled
                                class="w-full px-3.5 py-2.5 bg-slate-950/50 border border-slate-800/80 rounded-xl text-slate-500 text-sm cursor-not-allowed font-medium"
                            />
                        </div>
                    </div>

                    <div>
                        <label for="apptNotesInput" class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Context & Notes</label>
                        <textarea
                            id="apptNotesInput"
                            placeholder="Add agenda, video link, or key preparation context..."
                            class="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition resize-none"
                            rows="2"
                        ></textarea>
                    </div>

                    <div class="flex justify-end gap-2 pt-2">
                        <button
                            type="button"
                            id="cancelBookingBtn"
                            class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-bold transition active:scale-95 focus-ring"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-bold transition active:scale-95 shadow-lg shadow-indigo-600/30 flex items-center gap-2 focus-ring"
                        >
                            <i class="fa-solid fa-check text-xs"></i> Confirm Booking
                        </button>
                    </div>
                </form>

                <!-- Booked Appointments List -->
                <div id="existingApptsContainer" class="pt-4 border-t border-slate-800/80">
                    <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Existing Bookings for Selected Date</h4>
                    <div id="existingApptsList" class="space-y-2"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast Notification Banner for HCI Feedback -->
    <div id="toastNotification" class="fixed bottom-6 right-6 bg-indigo-600 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 translate-y-20 opacity-0 transition-all duration-300 pointer-events-none z-50 border border-indigo-400/30">
        <i id="toastIcon" class="fa-solid fa-circle-check text-base"></i>
        <span id="toastMsg" class="text-xs font-semibold">Appointment successfully updated</span>
    </div>

    <script>
        // Core Working Hours Configuration (08:00 to 18:00)
        const WORK_HOURS = [
            "08:00", "09:00", "10:00", "11:00", 
            "12:00", "13:00", "14:00", "15:00", 
            "16:00", "17:00", "18:00"
        ];

        // State Management
        let currentDate = new Date();
        let currentView = 'month'; // 'month', 'week', '3day', 'today'
        let selectedDate = new Date();
        let activeSelectedSlot = null;
        let searchQuery = '';

        // Initial Mock Appointments Data
        const todayObj = new Date();
        const todayKey = `${todayObj.getFullYear()}-${todayObj.getMonth()}-${todayObj.getDate()}`;

        let appointments = {
            [todayKey]: [
                {
                    id: 101,
                    title: "Quarterly Strategy Planning",
                    time: "10:00",
                    duration: 60,
                    category: "indigo",
                    notes: "Review product milestones & roadmap."
                },
                {
                    id: 102,
                    title: "Design System & HCI Sync",
                    time: "14:00",
                    duration: 60,
                    category: "emerald",
                    notes: "Usability testing & feedback review."
                }
            ]
        };

        // UI DOM Elements
        const viewContainer = document.getElementById('viewContainer');
        const viewDateRangeDisplay = document.getElementById('viewDateRangeDisplay');
        const activeViewSubtitle = document.getElementById('activeViewSubtitle');
        const viewButtons = document.querySelectorAll('.view-btn');
        const searchInput = document.getElementById('searchInput');
        
        const prevNavBtn = document.getElementById('prevNavBtn');
        const nextNavBtn = document.getElementById('nextNavBtn');
        const todayNavBtn = document.getElementById('todayNavBtn');

        // Modal Elements
        const slotBookingModal = document.getElementById('slotBookingModal');
        const modalContainer = document.getElementById('modalContainer');
        const closeModalBtn = document.getElementById('closeModalBtn');
        const modalDateTitle = document.getElementById('modalDateTitle');
        const modalDateSub = document.getElementById('modalDateSub');
        const timeSlotsGrid = document.getElementById('timeSlotsGrid');
        
        const bookingForm = document.getElementById('bookingForm');
        const selectedSlotBadge = document.getElementById('selectedSlotBadge');
        const clearSlotSelection = document.getElementById('clearSlotSelection');
        const apptTitleInput = document.getElementById('apptTitleInput');
        const apptCategoryInput = document.getElementById('apptCategoryInput');
        const apptNotesInput = document.getElementById('apptNotesInput');
        const cancelBookingBtn = document.getElementById('cancelBookingBtn');
        
        const existingApptsList = document.getElementById('existingApptsList');

        // Category Visual Mapping
        const categoryStyles = {
            indigo: { bg: 'bg-indigo-500/15', text: 'text-indigo-300', border: 'border-indigo-500/30', badge: 'bg-indigo-500' },
            emerald: { bg: 'bg-emerald-500/15', text: 'text-emerald-300', border: 'border-emerald-500/30', badge: 'bg-emerald-500' },
            amber: { bg: 'bg-amber-500/15', text: 'text-amber-300', border: 'border-amber-500/30', badge: 'bg-amber-500' },
            rose: { bg: 'bg-rose-500/15', text: 'text-rose-300', border: 'border-rose-500/30', badge: 'bg-rose-500' }
        };

        function formatDateKey(date) {
            return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
        }

        function isSameDay(d1, d2) {
            return d1.getFullYear() === d2.getFullYear() &&
                   d1.getMonth() === d2.getMonth() &&
                   d1.getDate() === d2.getDate();
        }

        function escapeHtml(str) {
            return (str || '').replace(/[&<>"']/g, m => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
            })[m]);
        }

        function showToast(message, isError = false) {
            const toast = document.getElementById('toastNotification');
            const toastMsg = document.getElementById('toastMsg');
            const toastIcon = document.getElementById('toastIcon');

            toastMsg.textContent = message;
            if (isError) {
                toast.className = toast.className.replace('bg-indigo-600', 'bg-rose-600');
                toastIcon.className = 'fa-solid fa-circle-exclamation text-base';
            } else {
                toast.className = toast.className.replace('bg-rose-600', 'bg-indigo-600');
                toastIcon.className = 'fa-solid fa-circle-check text-base';
            }

            toast.classList.remove('translate-y-20', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');

            setTimeout(() => {
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-20', 'opacity-0');
            }, 3000);
        }

        function renderView() {
            viewContainer.innerHTML = '';

            // Update Active Nav View Switcher UI
            viewButtons.forEach(btn => {
                if (btn.getAttribute('data-view') === currentView) {
                    btn.className = "view-btn px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-bold transition active:scale-95 shadow-sm focus-ring";
                    btn.setAttribute('aria-selected', 'true');
                } else {
                    btn.className = "view-btn px-3 py-1.5 rounded-lg hover:text-slate-200 transition active:scale-95 text-slate-400 focus-ring";
                    btn.setAttribute('aria-selected', 'false');
                }
            });

            switch (currentView) {
                case 'month':
                    renderMonthView();
                    break;
                case 'week':
                    renderWeekView();
                    break;
                case '3day':
                    render3DayView();
                    break;
                case 'today':
                    renderTodayView();
                    break;
            }
        }

        // 1. MONTH VIEW
        function renderMonthView() {
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();

            viewDateRangeDisplay.textContent = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
            activeViewSubtitle.textContent = 'Month Overview Grid';

            const firstDay = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();

            const wrapper = document.createElement('div');
            wrapper.className = 'flex-1 flex flex-col h-full';

            const dowHeader = document.createElement('div');
            dowHeader.className = 'grid grid-cols-7 gap-1 sm:gap-2 mb-2 text-center text-[11px] font-bold text-slate-400 uppercase tracking-wider';
            ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(d => {
                dowHeader.innerHTML += `<div class="p-1.5 bg-slate-950/60 rounded-lg border border-slate-800/60">${d}</div>`;
            });
            wrapper.appendChild(dowHeader);

            const grid = document.createElement('div');
            grid.className = 'grid grid-cols-7 gap-1 sm:gap-2 flex-1 auto-rows-fr';

            for (let i = 0; i < firstDay; i++) {
                grid.innerHTML += `<div class="bg-slate-950/20 border border-slate-800/20 rounded-xl opacity-20 pointer-events-none"></div>`;
            }

            for (let day = 1; day <= daysInMonth; day++) {
                const dayDate = new Date(year, month, day);
                const dateKey = formatDateKey(dayDate);
                let dayAppts = appointments[dateKey] || [];
                
                if (searchQuery) {
                    dayAppts = dayAppts.filter(a => a.title.toLowerCase().includes(searchQuery) || (a.notes && a.notes.toLowerCase().includes(searchQuery)));
                }

                const isToday = isSameDay(dayDate, new Date());
                const cell = document.createElement('div');
                cell.tabIndex = 0;
                cell.className = `min-h-[85px] sm:min-h-[100px] bg-slate-950/50 border ${isToday ? 'border-indigo-500 bg-indigo-950/20 ring-1 ring-indigo-500/40' : 'border-slate-800/80'} hover:border-indigo-400 hover:bg-slate-900 rounded-xl p-2 cursor-pointer transition flex flex-col group relative overflow-hidden focus-ring`;

                const bookedCount = dayAppts.length;
                const freeSlots = WORK_HOURS.length - bookedCount;

                cell.innerHTML = `
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold px-2 py-0.5 rounded-md ${isToday ? 'bg-indigo-600 text-white' : 'text-slate-300 group-hover:text-white'}">${day}</span>
                        <span class="text-[10px] ${freeSlots > 0 ? 'text-emerald-400 bg-emerald-500/10 border border-emerald-500/20' : 'text-rose-400 bg-rose-500/10 border border-rose-500/20'} px-1.5 py-0.5 rounded-full font-medium">
                            ${freeSlots} slots
                        </span>
                    </div>
                    <div class="space-y-1 flex-1 overflow-hidden custom-scrollbar pr-0.5">
                        ${dayAppts.slice(0, 3).map(a => {
                            const style = categoryStyles[a.category || 'indigo'];
                            return `
                                <div class="${style.bg} ${style.text} border ${style.border} px-1.5 py-0.5 rounded text-[10px] font-medium truncate flex items-center gap-1">
                                    <span class="w-1.5 h-1.5 rounded-full ${style.badge} shrink-0"></span>
                                    <span class="font-bold">${a.time}</span>
                                    <span class="truncate">${escapeHtml(a.title)}</span>
                                </div>
                            `;
                        }).join('')}
                        ${dayAppts.length > 3 ? `<div class="text-[10px] text-slate-400 font-bold text-center">+${dayAppts.length - 3} more</div>` : ''}
                    </div>
                `;

                cell.addEventListener('click', () => openSlotBookingModal(dayDate));
                cell.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        openSlotBookingModal(dayDate);
                    }
                });
                grid.appendChild(cell);
            }

            wrapper.appendChild(grid);
            viewContainer.appendChild(wrapper);
        }

        // 2. WEEK VIEW
        function renderWeekView() {
            const startOfWeek = new Date(currentDate);
            startOfWeek.setDate(currentDate.getDate() - currentDate.getDay());
            renderColumnTimelineView(startOfWeek, 7, '7-Day Slot Grid Overview');
        }

        // 3. 3-DAY VIEW
        function render3DayView() {
            const startDate = new Date(currentDate);
            renderColumnTimelineView(startDate, 3, '3-Day Slot Focus');
        }

        // HELPER: Multi-Column Timeline Builder
        function renderColumnTimelineView(startDate, dayCount, subtitle) {
            const endDate = new Date(startDate);
            endDate.setDate(startDate.getDate() + dayCount - 1);

            viewDateRangeDisplay.textContent = `${startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${endDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
            activeViewSubtitle.textContent = subtitle;

            const wrapper = document.createElement('div');
            wrapper.className = 'flex-1 flex flex-col h-full overflow-x-auto custom-scrollbar';

            const days = [];
            for (let i = 0; i < dayCount; i++) {
                const d = new Date(startDate);
                d.setDate(startDate.getDate() + i);
                days.push(d);
            }

            const header = document.createElement('div');
            header.className = `grid grid-cols-[60px_repeat(${dayCount},minmax(130px,1fr))] gap-2 mb-2 text-center border-b border-slate-800 pb-2`;
            header.innerHTML = `<div class="text-xs font-bold text-slate-500 py-1">Time</div>`;
            
            days.forEach(d => {
                const isToday = isSameDay(d, new Date());
                header.innerHTML += `
                    <div class="p-2 rounded-xl ${isToday ? 'bg-indigo-600/20 border border-indigo-500/40 text-indigo-300' : 'bg-slate-950/60 border border-slate-800 text-slate-300'} cursor-pointer hover:border-indigo-400 transition focus-ring" tabIndex="0" onclick="openSlotBookingModal(new Date(${d.getTime()}))">
                        <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400">${d.toLocaleDateString('en-US', { weekday: 'short' })}</div>
                        <div class="text-sm font-extrabold ${isToday ? 'text-indigo-400' : 'text-slate-200'}">${d.getDate()} ${d.toLocaleDateString('en-US', { month: 'short' })}</div>
                    </div>
                `;
            });
            wrapper.appendChild(header);

            const body = document.createElement('div');
            body.className = `flex-1 grid grid-cols-[60px_repeat(${dayCount},minmax(130px,1fr))] gap-2 overflow-y-auto custom-scrollbar max-h-[500px]`;

            WORK_HOURS.forEach(timeSlot => {
                body.innerHTML += `<div class="text-[11px] font-semibold text-slate-500 flex items-center justify-center">${timeSlot}</div>`;

                days.forEach(d => {
                    const dateKey = formatDateKey(d);
                    let dayAppts = appointments[dateKey] || [];
                    if (searchQuery) {
                        dayAppts = dayAppts.filter(a => a.title.toLowerCase().includes(searchQuery));
                    }

                    const bookedAppt = dayAppts.find(a => a.time === timeSlot);
                    const slotCell = document.createElement('div');
                    
                    if (bookedAppt) {
                        const style = categoryStyles[bookedAppt.category || 'indigo'];
                        slotCell.className = `${style.bg} border ${style.border} rounded-lg p-2 flex flex-col justify-between cursor-pointer hover:brightness-125 transition text-xs shadow-sm focus-ring`;
                        slotCell.innerHTML = `
                            <div class="font-bold ${style.text} truncate">${escapeHtml(bookedAppt.title)}</div>
                            <div class="text-[10px] text-slate-400 flex justify-between items-center mt-1">
                                <span><i class="fa-regular fa-clock text-[9px] mr-0.5"></i>${bookedAppt.time}</span>
                                <span class="bg-slate-950/60 px-1 rounded text-[9px]">Booked</span>
                            </div>
                        `;
                    } else {
                        slotCell.className = `bg-slate-950/40 border border-slate-800/60 hover:border-emerald-500/50 hover:bg-emerald-950/10 rounded-lg p-2 flex items-center justify-between cursor-pointer group transition focus-ring`;
                        slotCell.innerHTML = `
                            <span class="text-[11px] text-slate-600 group-hover:text-emerald-400 font-medium transition">Open</span>
                            <i class="fa-solid fa-plus text-[10px] text-slate-600 group-hover:text-emerald-400 transition"></i>
                        `;
                    }

                    slotCell.tabIndex = 0;
                    slotCell.addEventListener('click', () => openSlotBookingModal(d, timeSlot));
                    slotCell.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter') openSlotBookingModal(d, timeSlot);
                    });
                    body.appendChild(slotCell);
                });
            });

            wrapper.appendChild(body);
            viewContainer.appendChild(wrapper);
        }

        // 4. TODAY VIEW
        function renderTodayView() {
            const today = new Date();
            viewDateRangeDisplay.textContent = today.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
            activeViewSubtitle.textContent = "Today's Agenda Focus";

            const dateKey = formatDateKey(today);
            let todayAppts = appointments[dateKey] || [];
            if (searchQuery) {
                todayAppts = todayAppts.filter(a => a.title.toLowerCase().includes(searchQuery));
            }

            const wrapper = document.createElement('div');
            wrapper.className = 'flex-1 flex flex-col lg:flex-row gap-6 overflow-hidden';

            const overviewPanel = document.createElement('div');
            overviewPanel.className = 'w-full lg:w-1/3 bg-slate-950/60 border border-slate-800/80 rounded-2xl p-5 flex flex-col justify-between';
            
            const bookedCount = (appointments[dateKey] || []).length;
            const freeSlotsCount = WORK_HOURS.length - bookedCount;

            overviewPanel.innerHTML = `
                <div>
                    <div class="flex items-center gap-3.5 mb-4">
                        <div class="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-black text-xl">
                            ${today.getDate()}
                        </div>
                        <div>
                            <h2 class="text-base font-bold text-white">${today.toLocaleDateString('en-US', { weekday: 'long' })}</h2>
                            <p class="text-xs text-slate-400">${today.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</p>
                        </div>
                    </div>

                    <div class="space-y-3 my-6">
                        <div class="bg-slate-900 border border-slate-800 p-3 rounded-xl flex justify-between items-center">
                            <span class="text-xs text-slate-400">Total Slot Window</span>
                            <span class="text-sm font-bold text-slate-200">${WORK_HOURS.length} Hours</span>
                        </div>
                        <div class="bg-emerald-950/20 border border-emerald-500/30 p-3 rounded-xl flex justify-between items-center">
                            <span class="text-xs text-emerald-300">Available Slots</span>
                            <span class="text-sm font-bold text-emerald-400">${freeSlotsCount} Open</span>
                        </div>
                        <div class="bg-indigo-950/20 border border-indigo-500/30 p-3 rounded-xl flex justify-between items-center">
                            <span class="text-xs text-indigo-300">Scheduled Meetings</span>
                            <span class="text-sm font-bold text-indigo-400">${bookedCount} Booked</span>
                        </div>
                    </div>
                </div>

                <button onclick="openSlotBookingModal(new Date())" class="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 focus-ring">
                    <i class="fa-solid fa-plus text-xs"></i> Quick Book Slot Today
                </button>
            `;

            const timelinePanel = document.createElement('div');
            timelinePanel.className = 'flex-1 bg-slate-950/40 border border-slate-800/80 rounded-2xl p-4 overflow-y-auto custom-scrollbar space-y-3 max-h-[500px]';

            WORK_HOURS.forEach(slot => {
                const appt = todayAppts.find(a => a.time === slot);
                const row = document.createElement('div');

                if (appt) {
                    const style = categoryStyles[appt.category || 'indigo'];
                    row.className = `${style.bg} border ${style.border} rounded-xl p-3.5 flex justify-between items-start transition shadow-sm`;
                    row.innerHTML = `
                        <div class="flex gap-3">
                            <span class="text-xs font-bold text-indigo-400 bg-slate-950 px-2 py-1 rounded-lg border border-slate-800 h-fit">${slot}</span>
                            <div>
                                <h3 class="text-sm font-bold ${style.text}">${escapeHtml(appt.title)}</h3>
                                ${appt.notes ? `<p class="text-xs text-slate-400 mt-1">${escapeHtml(appt.notes)}</p>` : ''}
                                <span class="inline-block mt-2 text-[10px] bg-slate-950/60 px-2 py-0.5 rounded text-slate-300 border border-slate-800">
                                    <i class="fa-regular fa-clock mr-1"></i>${appt.duration || 60} mins
                                </span>
                            </div>
                        </div>
                        <button onclick="confirmDeleteAppointment('${dateKey}', ${appt.id})" class="text-slate-400 hover:text-rose-400 p-1.5 transition rounded-lg hover:bg-slate-900" title="Cancel Booking">
                            <i class="fa-regular fa-trash-can text-sm"></i>
                        </button>
                    `;
                } else {
                    row.className = `bg-slate-900/50 border border-slate-800/60 hover:border-emerald-500/40 hover:bg-emerald-950/10 rounded-xl p-3.5 flex justify-between items-center cursor-pointer group transition focus-ring`;
                    row.tabIndex = 0;
                    row.innerHTML = `
                        <div class="flex items-center gap-3">
                            <span class="text-xs font-bold text-slate-500 group-hover:text-emerald-400 transition">${slot}</span>
                            <span class="text-xs text-slate-500 group-hover:text-slate-300 font-medium transition">Open Time Slot</span>
                        </div>
                        <span class="text-xs font-bold text-emerald-400 opacity-0 group-hover:opacity-100 transition flex items-center gap-1">
                            Book Slot <i class="fa-solid fa-arrow-right text-[10px]"></i>
                        </span>
                    `;
                    row.addEventListener('click', () => openSlotBookingModal(today, slot));
                }
                timelinePanel.appendChild(row);
            });

            wrapper.appendChild(overviewPanel);
            wrapper.appendChild(timelinePanel);
            viewContainer.appendChild(wrapper);
        }

        function openSlotBookingModal(date, preselectedSlot = null) {
            selectedDate = date;
            const dateKey = formatDateKey(date);
            const dayAppts = appointments[dateKey] || [];

            modalDateTitle.textContent = `Schedule: ${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
            modalDateSub.textContent = `Select an open slot or manage existing appointments.`;

            timeSlotsGrid.innerHTML = '';
            WORK_HOURS.forEach(slot => {
                const isBooked = dayAppts.some(a => a.time === slot);
                const btn = document.createElement('button');
                btn.type = 'button';

                if (isBooked) {
                    btn.disabled = true;
                    btn.className = 'py-2 px-3 rounded-xl border border-slate-800 bg-slate-950/40 text-slate-600 text-xs font-bold cursor-not-allowed flex items-center justify-between opacity-50';
                    btn.innerHTML = `<span>${slot}</span> <i class="fa-solid fa-lock text-[10px]"></i>`;
                } else {
                    btn.className = `slot-btn py-2 px-3 rounded-xl border ${preselectedSlot === slot ? 'border-indigo-500 bg-indigo-600/30 text-indigo-200' : 'border-slate-800 bg-slate-950 hover:border-indigo-500 hover:text-indigo-400'} text-slate-300 text-xs font-bold transition flex items-center justify-between focus-ring`;
                    btn.innerHTML = `<span>${slot}</span> <i class="fa-solid fa-plus text-[10px] text-slate-500"></i>`;
                    btn.addEventListener('click', () => selectSlotForBooking(slot));
                }

                timeSlotsGrid.appendChild(btn);
            });

            renderBookedListForModal(dateKey);

            if (preselectedSlot && !dayAppts.some(a => a.time === preselectedSlot)) {
                selectSlotForBooking(preselectedSlot);
            } else {
                resetBookingForm();
            }

            slotBookingModal.classList.remove('hidden');
            setTimeout(() => {
                modalContainer.classList.remove('scale-95', 'opacity-0');
                modalContainer.classList.add('scale-100', 'opacity-100');
            }, 10);
        }

        function selectSlotForBooking(slot) {
            activeSelectedSlot = slot;
            selectedSlotBadge.textContent = slot;
            bookingForm.classList.remove('hidden');
            apptTitleInput.focus();

            document.querySelectorAll('.slot-btn').forEach(btn => {
                if (btn.textContent.includes(slot)) {
                    btn.className = 'slot-btn py-2 px-3 rounded-xl border-2 border-indigo-500 bg-indigo-600/30 text-indigo-200 text-xs font-bold transition flex items-center justify-between shadow-lg shadow-indigo-500/20';
                } else {
                    btn.className = 'slot-btn py-2 px-3 rounded-xl border border-slate-800 bg-slate-950 hover:border-indigo-500 hover:text-indigo-400 text-slate-300 text-xs font-semibold transition flex items-center justify-between';
                }
            });
        }

        function resetBookingForm() {
            activeSelectedSlot = null;
            bookingForm.classList.add('hidden');
            apptTitleInput.value = '';
            apptNotesInput.value = '';
        }

        function renderBookedListForModal(dateKey) {
            const dayAppts = appointments[dateKey] || [];
            existingApptsList.innerHTML = '';

            if (dayAppts.length === 0) {
                existingApptsList.innerHTML = `<p class="text-xs text-slate-500 italic">No appointments booked for this date yet.</p>`;
                return;
            }

            dayAppts.forEach(appt => {
                const style = categoryStyles[appt.category || 'indigo'];
                const item = document.createElement('div');
                item.className = `p-3 rounded-xl ${style.bg} border ${style.border} flex justify-between items-center text-xs`;
                item.innerHTML = `
                    <div>
                        <div class="font-semibold ${style.text} flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full ${style.badge}"></span>
                            <span class="font-bold">${appt.time}</span>
                            <span class="text-slate-100 font-bold ml-1">${escapeHtml(appt.title)}</span>
                        </div>
                        ${appt.notes ? `<p class="text-slate-400 text-[11px] mt-1 pl-4">${escapeHtml(appt.notes)}</p>` : ''}
                    </div>
                    <button class="delete-appt-btn text-slate-400 hover:text-rose-400 p-1.5 transition rounded-lg hover:bg-slate-950/50" title="Cancel Booking">
                        <i class="fa-regular fa-trash-can"></i>
                    </button>
                `;

                item.querySelector('.delete-appt-btn').addEventListener('click', () => {
                    confirmDeleteAppointment(dateKey, appt.id);
                });

                existingApptsList.appendChild(item);
            });
        }

        // HCI Principle: Error Prevention & Safe Confirmation
        function confirmDeleteAppointment(dateKey, id) {
            if (confirm("Are you sure you want to cancel this slot booking?")) {
                deleteAppointment(dateKey, id);
                showToast("Slot booking canceled successfully.");
            }
        }

        function deleteAppointment(dateKey, id) {
            if (appointments[dateKey]) {
                appointments[dateKey] = appointments[dateKey].filter(a => a.id !== id);
                if (appointments[dateKey].length === 0) {
                    delete appointments[dateKey];
                }
            }
            if (!slotBookingModal.classList.contains('hidden')) {
                openSlotBookingModal(selectedDate);
            }
            renderView();
        }

        // Form Submit Listener
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const title = apptTitleInput.value.trim();
            const category = apptCategoryInput.value;
            const notes = apptNotesInput.value.trim();

            if (!title || !activeSelectedSlot || !selectedDate) return;

            const dateKey = formatDateKey(selectedDate);
            if (!appointments[dateKey]) {
                appointments[dateKey] = [];
            }

            appointments[dateKey].push({
                id: Date.now(),
                title,
                time: activeSelectedSlot,
                duration: 60,
                category,
                notes
            });

            appointments[dateKey].sort((a, b) => a.time.localeCompare(b.time));

            closeModal();
            renderView();
            showToast(`Booked slot at ${activeSelectedSlot} for "${title}"`);
        });

        function closeModal() {
            modalContainer.classList.remove('scale-100', 'opacity-100');
            modalContainer.classList.add('scale-95', 'opacity-0');
            setTimeout(() => {
                slotBookingModal.classList.add('hidden');
                resetBookingForm();
            }, 150);
        }

        closeModalBtn.addEventListener('click', closeModal);
        cancelBookingBtn.addEventListener('click', closeModal);
        clearSlotSelection.addEventListener('click', resetBookingForm);
        slotBookingModal.addEventListener('click', (e) => {
            if (e.target === slotBookingModal) closeModal();
        });

        // Search Filter Event
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            renderView();
        });

        // View Mode Switches
        viewButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                currentView = btn.getAttribute('data-view');
                renderView();
            });
        });

        // Navigation Controllers
        prevNavBtn.addEventListener('click', () => navigatePeriod(-1));
        nextNavBtn.addEventListener('click', () => navigatePeriod(1));
        todayNavBtn.addEventListener('click', () => {
            currentDate = new Date();
            renderView();
        });

        function navigatePeriod(direction) {
            if (currentView === 'month') {
                currentDate.setMonth(currentDate.getMonth() + direction);
            } else if (currentView === 'week') {
                currentDate.setDate(currentDate.getDate() + (direction * 7));
            } else if (currentView === '3day') {
                currentDate.setDate(currentDate.getDate() + (direction * 3));
            } else if (currentView === 'today') {
                currentDate.setDate(currentDate.getDate() + direction);
            }
            renderView();
        }

        // HCI Shortcut Keys Listener
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !slotBookingModal.classList.contains('hidden')) {
                closeModal();
            } else if (document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
                if (e.key === 't' || e.key === 'T') {
                    currentDate = new Date();
                    renderView();
                } else if (e.key === 'ArrowLeft') {
                    navigatePeriod(-1);
                } else if (e.key === 'ArrowRight') {
                    navigatePeriod(1);
                }
            }
        });

        // Initialize App View
        renderView();
    </script>
</body>
</html>
``

---

## File: $relativePath

``html
{% extends "base.html" %}

{% block title %}Create Account - ClinicEase{% endblock %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/auth.css') }}">
{% endblock %}

{% block content %}
<div class="container auth-page auth-page-create">
    <section class="card auth-card" aria-labelledby="auth-title">
        <header class="auth-heading">
            <h1 id="auth-title">Welcome to ClinicEase</h1>
            <p>Sign in to manage appointments, or create an account and request your first visit.</p>
        </header>

        <div class="auth-tabs" role="tablist" aria-label="Account options">
            <button class="auth-tab" id="sign-in-tab" type="button" role="tab"
                    aria-selected="false" aria-controls="sign-in-panel" tabindex="-1">
                Sign In
            </button>
            <button class="auth-tab" id="create-account-tab" type="button" role="tab"
                    aria-selected="true" aria-controls="create-account-panel" tabindex="0">
                Create Account
            </button>
        </div>

        <section id="sign-in-panel" role="tabpanel" aria-labelledby="sign-in-tab" hidden>
            <div id="sign-in-feedback" class="alert alert-error" role="alert" hidden></div>
            <form id="sign-in-form" action="{{ url_for('login_page') }}" data-api-url="{{ url_for('api_login') }}"
                  data-dashboard-url="{{ url_for('dashboard') }}" method="post">
                <div class="form-group">
                    <label class="form-label" for="sign-in-email">Email address</label>
                    <input class="form-input" id="sign-in-email" name="email" type="email"
                           autocomplete="email" required>
                </div>
                <div class="form-group">
                    <label class="form-label" for="sign-in-password">Password</label>
                    <input class="form-input" id="sign-in-password" name="password" type="password"
                           autocomplete="current-password" required>
                </div>
                <button class="btn btn-primary btn-block" type="submit">Sign In</button>
            </form>
        </section>

        <section id="create-account-panel" role="tabpanel" aria-labelledby="create-account-tab">
            {% if error %}
                <div class="alert alert-error" role="alert">{{ error }}</div>
            {% endif %}
            <div id="create-account-feedback" class="alert alert-error" role="alert" hidden></div>

            <form id="create-account-form" action="{{ url_for('register_page') }}"
                  data-api-url="{{ url_for('api_register_and_book') }}"
                  data-dashboard-url="{{ url_for('patient_dashboard_view') }}"
                  data-confirm-message="Save this appointment?" method="post">
            <div class="registration-layout">
                <div class="registration-fields">
                    <div class="form-group">
                        <label class="form-label" for="create-name">Full name</label>
                        <input class="form-input" id="create-name" name="name" type="text"
                               autocomplete="name" maxlength="100"
                               value="{{ form_data.get('name', '') }}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="create-email">Email address</label>
                        <input class="form-input" id="create-email" name="email" type="email"
                               autocomplete="email" maxlength="100"
                               value="{{ form_data.get('email', '') }}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="create-contact-number">Contact number (optional)</label>
                        <input class="form-input" id="create-contact-number" name="contact_number" type="tel"
                               autocomplete="tel" inputmode="tel" maxlength="20"
                               value="{{ form_data.get('contact_number', '') }}">
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="create-password">Password</label>
                        <input class="form-input" id="create-password" name="password" type="password"
                               autocomplete="new-password" maxlength="1024" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="initial-purpose">Purpose of visit</label>
                        <textarea class="form-textarea" id="initial-purpose" name="purpose"
                                  maxlength="255" rows="3" required>{{ form_data.get('purpose', '') }}</textarea>
                    </div>
                </div>

                <section class="availability-panel" aria-labelledby="availability-title">
                    <div class="availability-heading">
                        <div>
                            <h2 id="availability-title">Choose an appointment</h2>
                            <p>Select a date, then choose an available time.</p>
                        </div>
                        <div class="calendar-navigation" aria-label="Calendar navigation">
                            <button class="calendar-nav-button" id="calendar-previous" type="button"
                                    aria-label="Show previous month">&larr;</button>
                            <p class="calendar-month" id="calendar-month" aria-live="polite"></p>
                            <button class="calendar-nav-button" id="calendar-next" type="button"
                                    aria-label="Show next month">&rarr;</button>
                        </div>
                    </div>
                    {% if slots_error %}
                        <p class="form-help availability-message" role="status">{{ slots_error }}</p>
                    {% elif not initial_request_slots %}
                        <p class="form-help availability-message" role="status">
                            No appointment times are available yet. Please ask clinic staff to generate upcoming slots.
                        </p>
                    {% endif %}
                    <div id="availability-calendar" class="availability-calendar" tabindex="-1"
                         role="group" aria-label="Available appointment dates"></div>
                    <div class="available-times">
                        <h3 id="available-times-title">Available times</h3>
                        <p id="calendar-instructions" class="form-help">
                            Choose a date on the calendar to see available times.
                        </p>
                        <div id="available-times-list" class="available-times-list"
                             aria-labelledby="available-times-title"></div>
                    </div>
                    <input type="hidden" id="initial-slot-id" name="slot_id"
                           value="{{ form_data.get('slot_id', '') }}">
                    <noscript>
                        <div class="form-group">
                            <label class="form-label" for="fallback-slot-id">Preferred appointment time</label>
                            <select class="form-input" id="fallback-slot-id" name="slot_id" required>
                                <option value="">Choose an available date and time</option>
                                {% for slot in initial_request_slots %}
                                    <option value="{{ slot.slot_id }}"
                                            {% if form_data.get('slot_id')|string == slot.slot_id|string %}selected{% endif %}>
                                        {{ slot.slot_date }} at {{ slot.time }}
                                    </option>
                                {% endfor %}
                            </select>
                        </div>
                    </noscript>
                    <div id="calendar-feedback" class="alert alert-error calendar-feedback"
                         role="alert" aria-live="assertive" hidden></div>
                    <div id="available-slot-data" class="visually-hidden" aria-hidden="true">
                        {% for slot in initial_request_slots %}
                            <span data-slot-option data-slot-id="{{ slot.slot_id }}"
                                  data-slot-date="{{ slot.slot_date }}"
                                  data-slot-time="{{ slot.time }}"></span>
                        {% endfor %}
                    </div>
                </section>
            </div>
            <button class="btn btn-primary btn-block" type="submit">
                Create Account and Request Appointment
            </button>
            </form>
        </section>
    </section>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/auth.js') }}"></script>
{% endblock %}

``

---

## File: $relativePath

``sql
DROP DATABASE IF EXISTS clinicease_db;
CREATE DATABASE clinicease_db;
USE clinicease_db;

-- ============================================================================
-- 1. USERS TABLE
-- Encapsulates core user account information with role-based segregation.
-- ============================================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contact_number VARCHAR(20) NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Patient', 'Clinic Staff') NOT NULL
) ENGINE=InnoDB;

-- Existing database migration (run only when the column is still named
-- phone_number): ALTER TABLE users CHANGE COLUMN phone_number contact_number VARCHAR(20) NULL;

-- Seed Data: All test accounts have the password 'password123'
-- MySQL's SHA2('password123', 256) exactly matches Python's hashlib.sha256
INSERT INTO users (name, email, password_hash, role) VALUES 
('Gaudenz Padullon', 'gaudenz@example.com', SHA2('password123', 256), 'Clinic Staff'),
('Dr. Sarah Jenkins', 'staff.sarah@example.com', SHA2('password123', 256), 'Clinic Staff'),
('Maria Santos', 'maria.patient@example.com', SHA2('password123', 256), 'Patient'),
('Juan Dela Cruz', 'juan.patient@example.com', SHA2('password123', 256), 'Patient');

-- ============================================================================
-- 2. APPOINTMENT SLOTS TABLE
-- Manages time slots with availability status.
-- ============================================================================
CREATE TABLE IF NOT EXISTS appointment_slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_date DATE NOT NULL,
    time VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Available',
    UNIQUE KEY uq_appointment_slots_date_time (slot_date, time)
) ENGINE=InnoDB;

-- ============================================================================
-- 2A. RECURRING CLINIC HOURS AND CLOSED DATES
-- weekday uses Python's weekday convention: Monday=0 through Sunday=6.
-- ============================================================================
CREATE TABLE IF NOT EXISTS clinic_schedule (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    weekday TINYINT UNSIGNED NOT NULL,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL,
    slot_duration_minutes SMALLINT UNSIGNED NOT NULL DEFAULT 30,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_clinic_schedule_weekday CHECK (weekday BETWEEN 0 AND 6),
    CONSTRAINT chk_clinic_schedule_duration CHECK (slot_duration_minutes = 30),
    CONSTRAINT chk_clinic_schedule_hours CHECK (open_time < close_time),
    UNIQUE KEY uq_clinic_schedule_hours (weekday, open_time, close_time)
);

CREATE TABLE IF NOT EXISTS blocked_dates (
    blocked_date DATE PRIMARY KEY,
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Default clinic hours: weekdays 08:00–17:00 and weekends 08:00–12:00,
-- with 30-minute slots. The generator creates the final slot only when its
-- full duration ends by the configured closing time.
INSERT IGNORE INTO clinic_schedule
    (weekday, open_time, close_time, slot_duration_minutes, is_active)
VALUES
    (0, '08:00:00', '17:00:00', 30, TRUE),
    (1, '08:00:00', '17:00:00', 30, TRUE),
    (2, '08:00:00', '17:00:00', 30, TRUE),
    (3, '08:00:00', '17:00:00', 30, TRUE),
    (4, '08:00:00', '17:00:00', 30, TRUE),
    (5, '08:00:00', '12:00:00', 30, TRUE),
    (6, '08:00:00', '12:00:00', 30, TRUE);

INSERT IGNORE INTO blocked_dates (blocked_date, reason)
VALUES ('2026-12-25', 'Christmas Day');

-- Seed selectable appointment times for the next 30 days so the calendar is usable
-- immediately after a fresh install. This uses the same weekly hours and closures
-- as the monthly slot-generation service; rerunning it does not duplicate slots.
INSERT IGNORE INTO appointment_slots (slot_date, time, status)
WITH RECURSIVE
calendar_days AS (
    SELECT DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY) AS slot_date
    UNION ALL
    SELECT DATE_ADD(slot_date, INTERVAL 1 DAY)
    FROM calendar_days
    WHERE slot_date < DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
),
schedule_times AS (
    SELECT
        weekday,
        close_time,
        slot_duration_minutes,
        open_time AS slot_start
    FROM clinic_schedule
    WHERE is_active = TRUE

    UNION ALL

    SELECT
        weekday,
        close_time,
        slot_duration_minutes,
        ADDTIME(slot_start, SEC_TO_TIME(slot_duration_minutes * 60))
    FROM schedule_times
    WHERE ADDTIME(slot_start, SEC_TO_TIME(slot_duration_minutes * 60)) < close_time
)
SELECT
    calendar_days.slot_date,
    DATE_FORMAT(schedule_times.slot_start, '%h:%i %p'),
    'Available'
FROM calendar_days
JOIN schedule_times
    ON WEEKDAY(calendar_days.slot_date) = schedule_times.weekday
WHERE ADDTIME(
          schedule_times.slot_start,
          SEC_TO_TIME(schedule_times.slot_duration_minutes * 60)
      ) <= schedule_times.close_time
  AND NOT EXISTS (
      SELECT 1
      FROM blocked_dates
      WHERE blocked_dates.blocked_date = calendar_days.slot_date
  );

-- ============================================================================
-- 3. APPOINTMENTS TABLE
-- Tracks appointment records, patient assignments, and lifecycle statuses.
-- ============================================================================
DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    user_id INT NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    contact_number VARCHAR(30) NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_id) REFERENCES appointment_slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

``

---

## File: $relativePath

``markdown
# ClinicEase: Web-Based Appointment Management System

ClinicEase is a web-based clinic appointment management system built with Flask and MySQL. It provides appointment scheduling, slot management, and role-based access for patients and clinic staff.

Patient email addresses are required for accounts and appointment updates. Contact numbers are optional during sign-up and appointment booking.

---

## Architecture and Design Patterns

The backend follows Object-Oriented Programming (OOP) principles and design patterns.

### 1. Object-Oriented Principles

* **Encapsulation:**
  * `User`: Stores its password hash privately. New passwords use Werkzeug's password hashing; legacy SHA-256 hashes are upgraded after successful login.
  * `Appointment`: Private `__status` attribute managed via `@property` and `@status.setter` with validation on permitted state transitions (`Pending` -> `Confirmed` -> `Completed` or `Cancelled`).
  * `AppointmentSlot`: Private `__status` attribute managed via `@property` and `@status.setter`. `book_atomically()` claims an Available, future slot with a conditional SQL update.

* **Inheritance and Polymorphism:**
  * Base class `User` defines the polymorphic method `get_user_role()`.
  * `Patient` inherits from `User` and overrides `get_user_role()` to return `"Patient"`.
  * `ClinicStaff` inherits from `User` and overrides `get_user_role()` to return `"Clinic Staff"`.
  * `User.login()` returns polymorphic subclasses (`Patient` or `ClinicStaff`) based on the database record.

* **Abstraction:**
  * `BaseDashboard` defines abstract contract `get_slots()` for role-based slot retrieval.
  * `BaseNotificationService` defines abstract contract `send_notification(recipient, subject, body)`.
  * `BookingValidationStrategy` defines abstract contract `validate(patient_id, slot, db_connection)`.

### 2. Design Patterns

* **Adapter Pattern (Structural):**
  * `PasswordHasherAdapter` encapsulates password hashing and verification (`hash_password`, `verify_password`), decoupling password handling from entity classes.

* **Factory Method Pattern (Creational):**
  * `DashboardFactory`: Instantiates `PatientDashboard` or `StaffDashboard` based on the user's role.
  * `NotificationServiceFactory`: Instantiates `ConsoleNotificationService` or `EmailNotificationService` based on dispatch mode.

* **Strategy Pattern (Behavioral):**
  * `StandardValidationStrategy`: Validates slot availability.
  * `StrictValidationStrategy`: Validates slot availability and prevents concurrent duplicate pending bookings for the same patient.
  * `RegistrationBookingValidationStrategy`: Checks account-email and selected-slot availability during the combined first-request flow.

* **Generator Pattern (Behavioral):**
  * `generate_appointment_report(appointments_list)`: Uses `yield` to stream formatted appointment summary rows without loading full report structures into memory.

---

## Project Structure

```
ClinicEase/
├── ClinicEase.sql                  # Database schema, table definitions, and seed data
├── migrations/
│   ├── 20261021_add_contact_numbers.sql # Adds registration and booking contact fields
│   └── 20261021_add_dynamic_calendar.sql # Schedule, closures, and unique slot keys
├── database.py                     # Centralized MySQL connection provider
├── app.py                          # Flask application routes, session handling, and API
├── README.MD                       # Project documentation
├── models/
│   ├── __init__.py                 # Package exports
│   ├── user.py                     # User, Patient, ClinicStaff, PasswordHasherAdapter
│   ├── appointment.py              # Appointment model with status transition guards
│   ├── slot.py                     # AppointmentSlot model with concurrency control
│   └── reports.py                  # Generator function for appointment reporting
├── services/
│   ├── __init__.py                 # Package exports
│   ├── dashboard_service.py        # BaseDashboard, PatientDashboard, StaffDashboard, DashboardFactory
│   ├── notification_service.py     # BaseNotificationService, ConsoleNotificationService, EmailNotificationService, NotificationServiceFactory
│   ├── registration_service.py     # Transactional account creation and initial appointment request
│   ├── slot_generator_service.py   # Calendar generation strategy, factory, and monthly slot service
│   ├── validation_strategy.py      # Booking and registration validation strategies
│   └── validation_service.py       # Input validation facade for login, registration, and booking
├── templates/
│   ├── base.html                   # Base layout template
│   ├── landing_page.html           # Initial landing page
│   ├── login.html                  # Patient and staff sign-in
│   ├── register.html               # Patient registration and initial appointment request
│   ├── patient/
│   │   └── patient_dashboard.html  # Patient booking and appointment history
│   ├── clinic_staff/
│   │   └── staff_dashboard.html    # Staff request and slot management
│   └── index.html                  # Backend API interactive test panel
└── static/
    ├── css/
    │   ├── base.css                # Design tokens, reset, shared shell
    │   ├── components.css          # Shared buttons, cards, forms, tables, badges
    │   └── pages/                  # Landing, auth, dashboard, test-panel styles
    └── js/
        ├── base.js                 # Shared request and toast utilities
        ├── auth.js                 # Login and account creation interactions
        ├── patient-dashboard.js    # Appointment booking interactions
        ├── staff-dashboard.js      # Staff actions and slot management
        └── api-test.js             # Developer test-panel interactions
```

---

## Database Setup

1. Ensure MySQL Server is running.
2. Import `ClinicEase.sql` into MySQL:
   ```bash
   mysql -u root -p < ClinicEase.sql
   ```
   For an existing database whose `users` table still has `phone_number`, migrate the
   optional field with:
   ```sql
   ALTER TABLE users CHANGE COLUMN phone_number contact_number VARCHAR(20) NULL;
   ```
   For an existing database, apply `migrations/20261021_add_dynamic_calendar.sql`.
   If the contact-number migration has not been applied yet, apply
   `migrations/20261021_add_contact_numbers.sql` first.
   If the existing `appointment_slots` table contains duplicate date/time pairs, resolve
   those conflicts first; the migration requires the unique key used for idempotent generation.
3. Configure the connection through `CLINICEASE_DB_HOST`, `CLINICEASE_DB_NAME`,
   `CLINICEASE_DB_USER`, and `CLINICEASE_DB_PASSWORD`. Set a stable, private
   `CLINICEASE_SECRET_KEY` for Flask sessions. For HTTPS deployments, set
   `CLINICEASE_HTTPS=true` so session cookies are marked Secure.
4. For SMTP delivery, set `CLINICEASE_NOTIFICATION_MODE=email`, `CLINICEASE_SMTP_HOST`,
   `CLINICEASE_SMTP_SENDER`, and (when required) `CLINICEASE_SMTP_USERNAME`,
   `CLINICEASE_SMTP_PASSWORD`, and `CLINICEASE_SMTP_PORT` in the environment.
   Email mode is the default. Set `CLINICEASE_NOTIFICATION_MODE=console` only for local
   development; the app reports a warning if an email cannot be delivered.

### Dynamic Calendar

The fresh-install schema and `migrations/20261021_add_dynamic_calendar.sql` create
`clinic_schedule` (Monday=0 through Sunday=6), `blocked_dates`, and the unique
`appointment_slots(slot_date, time)` key. The sample weekly schedule is Monday–Friday,
08:00–17:00 in 30-minute increments; Christmas Day 2026 is seeded as a closure.
When started with `python app.py`, ClinicEase generates missing slots for today and
the next 29 days. Staff can also generate slots from the dashboard or POST
`{"year": 2027, "month": 1}` to `/api/slots/generate`. Generated values are
normalized to the existing `HH:MM AM/PM` time format. `INSERT IGNORE` plus the unique
key makes generation idempotent.

To change clinic hours, update `clinic_schedule` rows; startup and dashboard generation
both use the active schedule. To block a date, staff POST
`{"blocked_date": "2027-01-01", "reason": "Holiday"}` to `/api/staff/blocked_dates`;
this disables unbooked slots already generated for that date. Existing booked
appointments are left intact.

### Default Seed Accounts

* **Clinic Staff Accounts (Password: `password123`):**
  * `gaudenz@example.com` (Gaudenz Padullon)
  * `staff.sarah@example.com` (Dr. Sarah Jenkins)
* **Patient Accounts (Password: `password123`):**
  * `maria.patient@example.com` (Maria Santos)
  * `juan.patient@example.com` (Juan Dela Cruz)

---

## Installation and Execution

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Access the application:
   * Landing Page: `http://localhost:5000/`
   * Sign in or create an account and request its first appointment: `http://localhost:5000/login`
   * Interactive API Test Panel: `http://localhost:5000/test-panel`

---

## Endpoints

### UI Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/login` | GET, POST | Sign-in and combined patient registration/appointment request page |
| `/register` / `/signup` | GET, POST | Combined patient account and initial appointment request |
| `/logout` | GET, POST | Clears session and redirects |
| `/dashboard` | GET | Role-based dashboard redirect |
| `/patient/dashboard` | GET | Patient dashboard view |
| `/staff/dashboard` | GET | Clinic staff dashboard view |
| `/test-panel` | GET | Interactive API testing panel |

### REST API Endpoints

| Endpoint | Method | Role | Description |
|---|---|---|---|
| `/api/register` | POST | Public | Create a patient account and first Pending appointment atomically |
| `/api/register_and_book` | POST | Public | Atomically create the account and Pending request, then sign the patient in |
| `/api/login` | POST | Public | Authenticate user and initialize session |
| `/api/logout` | POST | Authenticated | Terminate session |
| `/api/dashboard/slots` | GET | Authenticated | Retrieve slots (Available only for Patient, All for Staff) |
| `/api/slots/book` | POST | Patient | Book an available slot |
| `/api/staff/blocked_dates` | POST | Clinic Staff | Add a closure date and disable unbooked slots on it |
| `/api/slots/generate` | POST | Clinic Staff | Generate missing slots from clinic hours for a month |
| `/api/staff/appointments/pending` | GET | Clinic Staff | Fetch pending appointment requests |
| `/api/staff/appointments/<id>/action` | POST | Clinic Staff | Confirm, cancel, or complete an appointment |
| `/api/staff/slots/<id>` | PATCH, DELETE | Clinic Staff | Update, enable, disable, or remove an unused appointment time |
| `/api/staff/report` | GET | Clinic Staff | Generate streaming appointment report |

### Activity Diagram Execution Mapping

1. **Register & Book:** The sign-up tab collects name, email, password, a preferred available slot, and purpose; contact number is optional. `RegistrationService` checks required fields, email uniqueness, and slot availability. It creates the account, conditionally claims the slot, and inserts a Pending appointment in one MySQL transaction. Any failure rolls back all three writes. Notifications are attempted only after commit.
2. **Authenticate & Route:** `User.login()` returns a `Patient` or `ClinicStaff`. The dashboard route reads `get_user_role()` and redirects to that role's dashboard.
   Staff can generate a month of 30-minute slots from active `clinic_schedule` rows.
   `blocked_dates` prevents generation on closures and disables unbooked slots already created for those dates; existing booked appointments are preserved.
3. **Request a Visit:** Patient booking uses `SELECT ... FOR UPDATE`, then calls the encapsulated `AppointmentSlot.book()` while holding the row lock. The slot update and Pending appointment insert commit together; a competing request sees the updated status and is rejected without creating an appointment.
4. **Review & Complete:** Staff can confirm or cancel a Pending appointment. Cancellation returns its slot to Available in the same transaction. Only Confirmed appointments may transition to Completed.

The model classes remain in the repository's `models/` package instead of a monolithic
`models.py`; `models/__init__.py` exports the public classes. This preserves the established
module boundaries while keeping each class focused.

### DEBUGGING CODE

\source "c:/PYP/HCI Website/ClinicEase/ClinicEase.sql"
``

---

## File: $relativePath

``python
from datetime import date, datetime, timedelta
import os
import secrets

from flask import (
    Flask,
    jsonify,
    session,
    request,
    render_template,
    redirect,
    url_for,
)
import mysql.connector
from database import get_connection
from models.user import User
from models.slot import AppointmentSlot
from models.appointment import Appointment
from models.reports import generate_appointment_report
from services.dashboard_service import DashboardFactory
from services.notification_service import NotificationServiceFactory
from services.registration_service import InitialRequestError, RegistrationService
from services.slot_generator_service import CalendarSlotService
from services.validation_service import ValidationService

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("CLINICEASE_SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv(
    "CLINICEASE_HTTPS", ""
).strip().lower() in {"1", "true", "yes"}
if not os.getenv("CLINICEASE_SECRET_KEY"):
    app.logger.warning(
        "CLINICEASE_SECRET_KEY is unset; sessions will not persist across restarts."
    )


def send_notifications(notifications):
    if not notifications:
        return None

    try:
        mode = os.getenv("CLINICEASE_NOTIFICATION_MODE", "email")
        notifier = NotificationServiceFactory.create_service(mode=mode)
        for notification in notifications:
            notifier.send_notification(**notification)
    except Exception:
        app.logger.exception("Appointment notification delivery failed.")
        return "The appointment was saved, but an email notification could not be delivered."
    return None


def available_registration_slots():
    conn = get_connection()
    if not conn:
        return [], "Appointment times are temporarily unavailable. Please try again."

    try:
        dashboard = DashboardFactory.create_dashboard("Patient", conn)
        return dashboard.get_slots(), None
    except Exception:
        app.logger.exception("Failed to retrieve available registration slots.")
        return [], "Appointment times are temporarily unavailable. Please try again."
    finally:
        conn.close()


def render_auth_page(
    page="login",
    error=None,
    message=None,
    form_data=None,
    status_code=200,
):
    template = "register.html" if page == "register" else "login.html"
    slots, slots_error = (
        available_registration_slots() if page == "register" else ([], None)
    )
    return (
        render_template(
            template,
            error=error,
            message=message,
            form_data=form_data or {},
            initial_request_slots=slots,
            slots_error=slots_error,
        ),
        status_code,
    )


def create_initial_request(data):
    # Figure 2: registration and the first Pending appointment commit together.
    receipt = RegistrationService().create_initial_request(data)
    notifications = [
        {
            "recipient": receipt["email"],
            "subject": "ClinicEase account created and appointment request received",
            "body": (
                f"Hello {receipt['name']}, your ClinicEase account has been created. "
                f"Your appointment request for {receipt['slot_date']} at "
                f"{receipt['slot_time']} was received and is Pending review."
            ),
        },
        *[
            {
                "recipient": recipient,
                "subject": "New appointment request",
                "body": (
                    f"{receipt['name']} created a ClinicEase account and requested an "
                    f"appointment for {receipt['slot_date']} at {receipt['slot_time']}. "
                    "Please review it in ClinicEase."
                ),
            }
            for recipient in receipt["staff_recipients"]
        ],
    ]
    warning = send_notifications(notifications)
    return {
        "status": "success",
        "message": "Account created and appointment request saved as Pending.",
        "warning": warning,
        "patient_id": receipt["patient_id"],
        "name": receipt["name"],
        "email": receipt["email"],
        "contact_number": receipt["contact_number"],
    }


def start_patient_session(user_data):
    session.clear()
    session["user_id"] = user_data["patient_id"]
    session["role"] = "Patient"
    session["name"] = user_data["name"]
    session["email"] = user_data["email"]
    session["contact_number"] = user_data.get("contact_number")


# UI Views
@app.route("/")
def home():
    return render_template("landing_page.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_auth_page(page="login")

    email = request.form.get("email")
    password = request.form.get("password")

    is_valid, err = ValidationService.validate_login(
        {"email": email, "password": password}
    )
    if not is_valid:
        return render_auth_page(page="login", error=err, status_code=400)

    user_obj = User.login(email, password)
    if user_obj:
        session["user_id"] = user_obj.user_id
        session["role"] = user_obj.get_user_role()
        session["name"] = user_obj.name
        session["email"] = user_obj.email
        session["contact_number"] = user_obj.contact_number
        return redirect(url_for("dashboard"))

    return render_auth_page(
        page="login", error="Invalid email or password.", status_code=401
    )


@app.route("/signup", methods=["GET"])
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_auth_page(page="register")

    form_data = request.form.to_dict()
    try:
        result = create_initial_request(form_data)
    except InitialRequestError as error:
        return render_auth_page(
            page="register",
            error=str(error),
            form_data=form_data,
            status_code=error.status_code,
        )
    except Exception:
        app.logger.exception("Failed to create initial patient request.")
        return render_auth_page(
            page="register",
            error="The account and appointment request could not be saved. Please try again.",
            form_data=form_data,
            status_code=500,
        )

    message = result["message"]
    if result["warning"]:
        message = f"{message} {result['warning']}"
    start_patient_session(result)
    return redirect(url_for("patient_dashboard_view"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    if request.is_json or request.path.startswith("/api/"):
        return (
            jsonify({"status": "success", "message": "Logged out successfully."}),
            200,
        )
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    # Figure 2: the User subclass determines which dashboard is selected.
    role = session.get("role")
    if not role:
        return redirect(url_for("login_page"))
    if role == "Clinic Staff":
        return redirect(url_for("staff_dashboard_view"))
    return redirect(url_for("patient_dashboard_view"))


@app.route("/patient/dashboard")
def patient_dashboard_view():
    if session.get("role") != "Patient":
        return redirect(url_for("login_page"))

    conn = get_connection()
    if not conn:
        return "Database connection failed", 500

    try:
        dashboard_service = DashboardFactory.create_dashboard("Patient", conn)
        slots = dashboard_service.get_slots()

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT a.appointment_id, a.purpose, a.status, a.created_at,
                   a.contact_number, s.slot_date, s.time
            FROM appointments a
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.user_id = %s
            ORDER BY s.slot_date ASC, s.time ASC
            """,
            (session.get("user_id"),),
        )
        appointments = cursor.fetchall()
        cursor.close()

        upcoming_appointments = [
            appointment
            for appointment in appointments
            if appointment["status"] in ("Pending", "Confirmed")
            and appointment["slot_date"] >= date.today()
        ]
        upcoming_ids = {
            appointment["appointment_id"] for appointment in upcoming_appointments
        }
        past_appointments = [
            appointment
            for appointment in appointments
            if appointment["appointment_id"] not in upcoming_ids
        ]
        user = {
            "name": session.get("name", "Patient"),
            "email": session.get("email", ""),
            "contact_number": session.get("contact_number", ""),
        }
        return render_template(
            "patient/patient_dashboard.html",
            user=user,
            slots=slots,
            upcoming_appointments=upcoming_appointments,
            past_appointments=past_appointments,
        )
    finally:
        conn.close()


@app.route("/staff/dashboard")
def staff_dashboard_view():
    if session.get("role") != "Clinic Staff":
        return redirect(url_for("login_page"))

    conn = get_connection()
    if not conn:
        return "Database connection failed", 500

    try:
        dashboard_service = DashboardFactory.create_dashboard("Clinic Staff", conn)
        slots = dashboard_service.get_slots()

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.appointment_id, a.purpose, a.status, a.created_at,
                   u.name as patient_name, u.email, a.contact_number,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Pending'
            ORDER BY a.created_at ASC
            """)
        pending_appointments = cursor.fetchall()
        cursor.execute("""
            SELECT a.appointment_id, a.purpose, a.status, a.created_at,
                   u.name as patient_name, u.email, a.contact_number,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Confirmed'
            ORDER BY s.slot_date ASC, s.time ASC
            """)
        confirmed_appointments = cursor.fetchall()
        cursor.close()

        for slot in slots:
            slot["slot_date_input"] = slot["slot_date"].isoformat()
            try:
                slot["time_input"] = datetime.strptime(
                    slot["time"], "%I:%M %p"
                ).strftime("%H:%M")
            except ValueError:
                slot["time_input"] = datetime.strptime(slot["time"], "%H:%M").strftime(
                    "%H:%M"
                )

        user = {
            "name": session.get("name", "Clinic Staff"),
            "email": session.get("email", ""),
        }
        return render_template(
            "clinic_staff/staff_dashboard.html",
            user=user,
            slots=slots,
            pending_appointments=pending_appointments,
            confirmed_appointments=confirmed_appointments,
            today=date.today(),
            calendar_days=[
                date.today() + timedelta(days=offset) for offset in range(15)
            ],
        )
    finally:
        conn.close()


@app.route("/test-panel")
def test_panel():
    return render_template("index.html")


# API Endpoints
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Incomplete Information."}), 400

    try:
        return jsonify(create_initial_request(data)), 201
    except InitialRequestError as error:
        return jsonify({"status": "error", "message": str(error)}), error.status_code
    except Exception:
        app.logger.exception("Failed to create initial patient request.")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The account and appointment request could not be saved. Please try again.",
                }
            ),
            500,
        )


@app.route("/api/register_and_book", methods=["POST"])
def api_register_and_book():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400

    try:
        result = create_initial_request(data)
    except InitialRequestError as error:
        return jsonify({"status": "error", "message": str(error)}), error.status_code
    except Exception:
        app.logger.exception("Failed to register patient and book initial appointment.")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The account and appointment request could not be saved. Please try again.",
                }
            ),
            500,
        )

    start_patient_session(result)
    return (
        jsonify(
            {
                "status": "success",
                "message": result["message"],
                "warning": result["warning"],
                "redirect_url": url_for("patient_dashboard_view"),
            }
        ),
        201,
    )


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}

    is_valid, err = ValidationService.validate_login(data)
    if not is_valid:
        return jsonify({"status": "error", "message": err}), 400

    email = data.get("email")
    password = data.get("password")

    user_obj = User.login(email, password)
    if user_obj:
        session["user_id"] = user_obj.user_id
        session["role"] = user_obj.get_user_role()
        session["name"] = user_obj.name
        session["email"] = user_obj.email
        session["contact_number"] = user_obj.contact_number

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Welcome Back, {user_obj.name}",
                    "role": session["role"],
                }
            ),
            200,
        )

    return jsonify({"status": "error", "message": "Invalid email or password"}), 401


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully."}), 200


@app.route("/api/dashboard/slots", methods=["GET"])
def get_dashboard_slots():
    role = session.get("role")
    if not role:
        return (
            jsonify(
                {"status": "error", "message": "Unauthorized. Please log in first."}
            ),
            401,
        )

    conn = get_connection()
    if not conn:
        return (
            jsonify({"status": "error", "message": "Database connection failed"}),
            500,
        )

    try:
        dashboard_service = DashboardFactory.create_dashboard(role, conn)
        slots = dashboard_service.get_slots()
        return jsonify({"status": "success", "role": role, "slots": slots}), 200
    finally:
        conn.close()


@app.route("/api/slots/book", methods=["POST"])
def book_appointment_slot():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400
    patient_id = session.get("user_id")

    if not patient_id or session.get("role") != "Patient":
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Unauthorized. Please log in as a patient.",
                }
            ),
            401,
        )

    is_valid_payload, err = ValidationService.validate_booking(data)
    if not is_valid_payload:
        return jsonify({"status": "error", "message": err}), 400

    slot_id = int(data.get("slot_id"))
    purpose = data.get("purpose")
    contact_number = data.get("contact_number")
    contact_number = (
        (contact_number.strip() or None) if isinstance(contact_number, str) else None
    )

    conn = get_connection()
    if not conn:
        return (
            jsonify({"status": "error", "message": "Database connection failed"}),
            500,
        )

    cursor = None
    try:
        # Pessimistic locking serializes patients competing for this slot.
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT *
            FROM appointment_slots
            WHERE slot_id = %s
            FOR UPDATE
            """,
            (slot_id,),
        )
        slot_data = cursor.fetchone()
        if not slot_data:
            conn.rollback()
            return jsonify({"status": "error", "message": "Slot not found."}), 404

        slot = AppointmentSlot(
            slot_id=slot_data["slot_id"],
            slot_date=slot_data["slot_date"],
            time=slot_data["time"],
            status=slot_data["status"],
        )
        if slot.slot_date < date.today():
            conn.rollback()
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "This appointment slot is no longer available. Please select another slot.",
                    }
                ),
                409,
            )
        # Encapsulation: book() validates and updates the model's protected status.
        slot.book()
        cursor.execute(
            """
            UPDATE appointment_slots
            SET status = %s
            WHERE slot_id = %s AND status = 'Available'
            """,
            (slot.status, slot_id),
        )
        if cursor.rowcount != 1:
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        Appointment.create_pending(
            cursor,
            patient_id=patient_id,
            slot_id=slot_id,
            purpose=purpose.strip(),
            contact_number=contact_number,
        )
        cursor.execute("SELECT email FROM users WHERE role = 'Clinic Staff'")
        staff_recipients = [row["email"] for row in cursor.fetchall()]
        conn.commit()

        notification_warning = send_notifications(
            [
                {
                    "recipient": session.get("email", ""),
                    "subject": "Appointment request received",
                    "body": (
                        f"Hello {session.get('name', 'Patient')}, your appointment request "
                        f"for {slot.slot_date} at {slot.time} was received and is Pending review."
                    ),
                },
                *[
                    {
                        "recipient": recipient,
                        "subject": "New appointment request",
                        "body": (
                            f"{session.get('name', 'A patient')} requested an appointment "
                            f"for {slot.slot_date} at {slot.time}. Please review it in ClinicEase."
                        ),
                    }
                    for recipient in staff_recipients
                ],
            ]
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Request saved as Pending. Slot status is now Booked.",
                    "warning": notification_warning,
                }
            ),
            200,
        )

    except ValueError as error:
        conn.rollback()
        return jsonify({"status": "error", "message": str(error)}), 409
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to book appointment slot %s.", slot_id)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The appointment could not be saved. Please try again.",
                }
            ),
            500,
        )
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


@app.route("/api/staff/appointments/pending", methods=["GET"])
def get_pending_appointments():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT a.appointment_id, a.purpose, a.status, u.name as patient_name,
                   u.email, a.contact_number, s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.status = 'Pending'
            ORDER BY a.created_at ASC
        """
        cursor.execute(query)
        appointments = cursor.fetchall()
        return jsonify({"status": "success", "appointments": appointments}), 200
    finally:
        cursor.close()
        conn.close()


@app.route("/api/staff/dashboard/stats", methods=["GET"])
def get_staff_dashboard_stats():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM appointments
            GROUP BY status
            """
        )
        status_counts = {
            "Pending": 0,
            "Confirmed": 0,
            "Completed": 0,
            "Cancelled": 0,
        }
        for row in cursor.fetchall():
            status_counts[row["status"]] = row["count"]

        cursor.execute(
            """
            SELECT DAYOFWEEK(s.slot_date) AS weekday_index, COUNT(*) AS count
            FROM appointments AS a
            JOIN appointment_slots AS s ON s.slot_id = a.slot_id
            WHERE s.slot_date BETWEEN CURRENT_DATE
                AND DATE_ADD(CURRENT_DATE, INTERVAL 6 DAY)
              AND a.status != 'Cancelled'
            GROUP BY DAYOFWEEK(s.slot_date)
            """
        )
        bookings_by_weekday = {
            row["weekday_index"]: row["count"] for row in cursor.fetchall()
        }
        today = date.today()
        weekly_bookings = [
            {
                "day": (today + timedelta(days=offset)).strftime("%a"),
                "count": bookings_by_weekday.get(
                    ((today + timedelta(days=offset)).isoweekday() % 7) + 1,
                    0,
                ),
            }
            for offset in range(7)
        ]

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM appointment_slots
            WHERE status = 'Available'
              AND slot_date BETWEEN CURRENT_DATE
                  AND DATE_ADD(CURRENT_DATE, INTERVAL 6 DAY)
            """
        )
        available_slots_next_7_days = cursor.fetchone()["count"]

        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN a.status = 'Pending'
                    AND a.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
                    THEN 1 ELSE 0 END) AS recent_pending,
                SUM(CASE WHEN a.status = 'Pending'
                    AND a.created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 14 DAY)
                    AND a.created_at < DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
                    THEN 1 ELSE 0 END) AS previous_pending,
                SUM(CASE WHEN s.slot_date >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
                    AND s.slot_date < DATE_ADD(LAST_DAY(CURRENT_DATE), INTERVAL 1 DAY)
                    THEN 1 ELSE 0 END) AS total_appointments_this_month,
                SUM(CASE WHEN a.status = 'Completed'
                    AND s.slot_date >= DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
                    AND s.slot_date < DATE_ADD(LAST_DAY(CURRENT_DATE), INTERVAL 1 DAY)
                    THEN 1 ELSE 0 END) AS completed_this_month,
                SUM(CASE WHEN a.status = 'Confirmed'
                    AND s.slot_date BETWEEN
                        DATE_SUB(CURRENT_DATE, INTERVAL WEEKDAY(CURRENT_DATE) DAY)
                        AND DATE_ADD(
                            DATE_SUB(CURRENT_DATE, INTERVAL WEEKDAY(CURRENT_DATE) DAY),
                            INTERVAL 6 DAY
                        )
                    THEN 1 ELSE 0 END) AS confirmed_this_week
            FROM appointments AS a
            JOIN appointment_slots AS s ON s.slot_id = a.slot_id
            """
        )
        summary = cursor.fetchone()
        recent_pending = int(summary["recent_pending"] or 0)
        previous_pending = int(summary["previous_pending"] or 0)
        total_appointments_this_month = int(
            summary["total_appointments_this_month"] or 0
        )
        completed_this_month = int(summary["completed_this_month"] or 0)
        confirmed_this_week = int(summary["confirmed_this_week"] or 0)
        if recent_pending > previous_pending:
            pending_trend = "up"
        elif recent_pending < previous_pending:
            pending_trend = "down"
        else:
            pending_trend = "flat"

        return (
            jsonify(
                {
                    "status": "success",
                    "status_counts": status_counts,
                    "weekly_bookings": weekly_bookings,
                    "available_slots_next_7_days": int(
                        available_slots_next_7_days or 0
                    ),
                    "total_appointments_this_month": total_appointments_this_month,
                    "completed_this_month": completed_this_month,
                    "confirmed_this_week": confirmed_this_week,
                    "pending_trend": {
                        "direction": pending_trend,
                        "recent": recent_pending,
                        "previous": previous_pending,
                    },
                }
            ),
            200,
        )
    except Exception:
        app.logger.exception("Failed to load staff dashboard statistics.")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Dashboard statistics could not be loaded.",
                }
            ),
            500,
        )
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


@app.route("/api/staff/blocked_dates", methods=["POST"])
def create_blocked_date():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400

    raw_date = data.get("blocked_date", data.get("date"))
    reason = data.get("reason", "Clinic closed")
    try:
        blocked_date = date.fromisoformat(raw_date)
    except (TypeError, ValueError):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Enter the clinic closure date in YYYY-MM-DD format.",
                }
            ),
            400,
        )

    if not isinstance(reason, str) or not reason.strip() or len(reason.strip()) > 255:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Closure reason is required and must be 255 characters or fewer.",
                }
            ),
            400,
        )
    if blocked_date < date.today():
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "A past date cannot be added as a clinic closure.",
                }
            ),
            400,
        )

    conn = get_connection()
    if not conn:
        return (
            jsonify({"status": "error", "message": "Database connection failed."}),
            500,
        )

    cursor = None
    try:
        conn.autocommit = False
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO blocked_dates (blocked_date, reason)
            VALUES (%s, %s)
            """,
            (blocked_date, reason.strip()),
        )
        # Do not cancel booked appointments; remove newly-blocked open times from patient view.
        cursor.execute(
            """
            UPDATE appointment_slots
            SET status = 'Disabled'
            WHERE slot_date = %s AND status = 'Available'
            """,
            (blocked_date,),
        )
        disabled_count = cursor.rowcount
        conn.commit()
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Clinic closure saved.",
                    "disabled_slots": disabled_count,
                }
            ),
            201,
        )
    except mysql.connector.IntegrityError:
        conn.rollback()
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "That date is already marked as a clinic closure.",
                }
            ),
            409,
        )
    except Exception:
        conn.rollback()
        app.logger.exception("Failed to save clinic closure for %s.", blocked_date)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "The clinic closure could not be saved.",
                }
            ),
            500,
        )
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


@app.route("/api/slots/generate", methods=["POST"])
def generate_monthly_slots():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400

    year = data.get("year")
    month = data.get("month")
    if (
        isinstance(year, bool)
        or not isinstance(year, int)
        or isinstance(month, bool)
        or not isinstance(month, int)
    ):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Year and month must be integers.",
                }
            ),
            400,
        )

    try:
        inserted_count = CalendarSlotService().generate_slots_for_month(year, month)
    except ValueError as error:
        return jsonify({"status": "error", "message": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"status": "error", "message": str(error)}), 503
    except Exception:
        app.logger.exception("Failed to generate slots for %s-%02d.", year, month)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Appointment slots could not be generated.",
                }
            ),
            500,
        )

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Generated {inserted_count} new appointment slots.",
                "inserted": inserted_count,
            }
        ),
        200,
    )


@app.route("/api/staff/appointments/<int:appt_id>/action", methods=["POST"])
def staff_appointment_action(appt_id):
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400
    action = data.get("action")

    if action not in ["confirm", "cancel", "complete"]:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Invalid action. Choose confirm, cancel, or complete.",
                }
            ),
            400,
        )

    appt_data = Appointment.fetch_by_id(appt_id)
    if not appt_data:
        return jsonify({"status": "error", "message": "Appointment not found."}), 404

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Figure 2: staff review branches to Confirmed or Cancelled; only Confirmed completes.
        appt = Appointment(
            appointment_id=appt_data["appointment_id"],
            patient_id=appt_data["user_id"],
            slot_id=appt_data["slot_id"],
            purpose=appt_data["purpose"],
            status=appt_data["status"],
        )

        if action == "confirm":
            appt.confirm()
            new_status = "Confirmed"
        elif action == "cancel":
            appt.cancel()
            new_status = "Cancelled"

            cursor.execute(
                "SELECT slot_date FROM appointment_slots WHERE slot_id = %s FOR UPDATE",
                (appt.slot_id,),
            )
            slot_data = cursor.fetchone()
            if not slot_data:
                raise ValueError("The appointment time no longer exists.")
            cursor.execute(
                """
                UPDATE appointment_slots
                SET status = CASE
                    WHEN EXISTS (
                        SELECT 1 FROM blocked_dates
                        WHERE blocked_date = %s
                    ) THEN 'Disabled'
                    ELSE 'Available'
                END
                WHERE slot_id = %s
                """,
                (slot_data["slot_date"], appt.slot_id),
            )
        else:
            appt.complete()
            new_status = "Completed"

        cursor.execute(
            """
            UPDATE appointments
            SET status = %s
            WHERE appointment_id = %s AND status = %s
            """,
            (new_status, appt_id, appt_data["status"]),
        )
        if cursor.rowcount != 1:
            conn.rollback()
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "This appointment was updated by someone else. Refresh and try again.",
                    }
                ),
                409,
            )
        conn.commit()

        notification_warning = send_notifications(
            [
                {
                    "recipient": appt_data["email"],
                    "subject": f"Appointment {new_status}",
                    "body": (
                        f"Dear {appt_data['patient_name']}, your appointment has been "
                        f"{new_status.lower()}."
                    ),
                }
            ]
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Appointment {new_status} successfully.",
                    "warning": notification_warning,
                }
            ),
            200,
        )

    except ValueError as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/staff/slots/<int:slot_id>", methods=["PATCH", "DELETE"])
def manage_staff_slot(slot_id):
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid request payload."}), 400
    action = data.get("action")
    conn = get_connection()
    if not conn:
        return (
            jsonify({"status": "error", "message": "Database connection failed."}),
            500,
        )

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == "PATCH" and action == "update":
            try:
                slot_date = date.fromisoformat(data.get("slot_date", ""))
                parsed_time = datetime.strptime(data.get("time", ""), "%H:%M")
                slot_time = parsed_time.strftime("%I:%M %p")
            except (TypeError, ValueError):
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Enter a valid appointment date and time.",
                        }
                    ),
                    400,
                )

            if datetime.combine(slot_date, parsed_time.time()) < datetime.now():
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Appointment times cannot be moved into the past.",
                        }
                    ),
                    400,
                )

            cursor.execute(
                "SELECT 1 FROM blocked_dates WHERE blocked_date = %s",
                (slot_date,),
            )
            if cursor.fetchone():
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "An appointment time cannot be moved onto a clinic closure date.",
                        }
                    ),
                    409,
                )

            cursor.execute(
                """
                SELECT slot_id FROM appointment_slots
                WHERE slot_date = %s AND time = %s AND slot_id != %s
                LIMIT 1
                """,
                (slot_date, slot_time, slot_id),
            )
            if cursor.fetchone():
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "An appointment time already exists at that date and time.",
                        }
                    ),
                    409,
                )

            cursor.execute(
                """
                UPDATE appointment_slots
                SET slot_date = %s, time = %s
                WHERE slot_id = %s
                  AND status IN ('Available', 'Unavailable', 'Disabled')
                  AND NOT EXISTS (
                      SELECT 1 FROM appointments WHERE appointments.slot_id = %s
                  )
                """,
                (slot_date, slot_time, slot_id, slot_id),
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "This time cannot be changed because it is booked or has appointment history.",
                        }
                    ),
                    409,
                )
            conn.commit()
            return (
                jsonify({"status": "success", "message": "Appointment time updated."}),
                200,
            )

        if request.method == "DELETE" and action == "delete":
            cursor.execute(
                """
                DELETE FROM appointment_slots
                WHERE slot_id = %s
                  AND status IN ('Available', 'Unavailable', 'Disabled')
                  AND NOT EXISTS (
                      SELECT 1 FROM appointments WHERE appointments.slot_id = %s
                  )
                """,
                (slot_id, slot_id),
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "This time cannot be removed because it is booked or has appointment history.",
                        }
                    ),
                    409,
                )
            conn.commit()
            return (
                jsonify({"status": "success", "message": "Appointment time removed."}),
                200,
            )

        if request.method == "PATCH" and action in ("enable", "disable"):
            new_status = "Available" if action == "enable" else "Disabled"
            if action == "enable":
                cursor.execute(
                    """
                    SELECT s.slot_date,
                           EXISTS (
                               SELECT 1 FROM blocked_dates b
                               WHERE b.blocked_date = s.slot_date
                           ) AS is_blocked
                    FROM appointment_slots s
                    WHERE s.slot_id = %s
                    FOR UPDATE
                    """,
                    (slot_id,),
                )
                slot_data = cursor.fetchone()
                if not slot_data:
                    conn.rollback()
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "Appointment time not found.",
                            }
                        ),
                        404,
                    )
                if slot_data["is_blocked"]:
                    conn.rollback()
                    return (
                        jsonify(
                            {
                                "status": "error",
                                "message": "A slot on a clinic closure date cannot be enabled.",
                            }
                        ),
                        409,
                    )
            cursor.execute(
                """
                UPDATE appointment_slots
                SET status = %s
                WHERE slot_id = %s AND status IN ('Available', 'Unavailable', 'Disabled')
                """,
                (new_status, slot_id),
            )
            if cursor.rowcount != 1:
                conn.rollback()
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "This appointment time cannot be changed.",
                        }
                    ),
                    409,
                )
            conn.commit()
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": f"Appointment time {new_status.lower()}.",
                    }
                ),
                200,
            )

        return (
            jsonify({"status": "error", "message": "Invalid appointment time action."}),
            400,
        )
    except Exception as error:
        conn.rollback()
        return jsonify({"status": "error", "message": str(error)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/api/staff/report", methods=["GET"])
def get_staff_appointment_report():
    if session.get("role") != "Clinic Staff":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT a.appointment_id, a.purpose, a.status, u.name as patient_name,
                   s.slot_date, s.time
            FROM appointments a
            JOIN users u ON a.user_id = u.user_id
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            ORDER BY a.appointment_id ASC
            """)
        appointments = cursor.fetchall()

        report_generator = generate_appointment_report(appointments)
        report_lines = list(report_generator)

        return (
            jsonify(
                {
                    "status": "success",
                    "total": len(report_lines),
                    "report": report_lines,
                }
            ),
            200,
        )
    finally:
        cursor.close()
        conn.close()


@app.route("/api/patient/appointments/<int:appt_id>/cancel", methods=["POST"])
def patient_cancel_appointment(appt_id):
    if session.get("role") != "Patient":
        return jsonify({"status": "error", "message": "Unauthorized."}), 401

    conn = get_connection()
    if not conn:
        return jsonify({"status": "error", "message": "DB failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Verify this appointment belongs to the logged-in patient
        cursor.execute(
            """
            SELECT a.*, s.slot_id, s.slot_date, s.time, s.status as slot_status
            FROM appointments a
            JOIN appointment_slots s ON a.slot_id = s.slot_id
            WHERE a.appointment_id = %s AND a.user_id = %s
            """,
            (appt_id, session.get("user_id")),
        )
        appt_data = cursor.fetchone()

        if not appt_data:
            return (
                jsonify({"status": "error", "message": "Appointment not found."}),
                404,
            )

        # Only allow cancelling Pending or Confirmed appointments
        if appt_data["status"] not in ("Pending", "Confirmed"):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Cannot cancel an appointment with status '{appt_data['status']}'.",
                    }
                ),
                400,
            )

        # Update appointment status
        cursor.execute(
            "UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = %s",
            (appt_id,),
        )

        # Release the slot back to Available (only if it was Booked)
        if appt_data["slot_status"] == "Booked":
            cursor.execute(
                "UPDATE appointment_slots SET status = 'Available' WHERE slot_id = %s",
                (appt_data["slot_id"],),
            )

        conn.commit()

        return (
            jsonify(
                {"status": "success", "message": "Appointment cancelled successfully."}
            ),
            200,
        )

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    try:
        inserted_count = CalendarSlotService().generate_upcoming_slots(days_ahead=30)
        app.logger.info(
            "Generated %s appointment slots for the next 30 days.",
            inserted_count,
        )
    except Exception:
        app.logger.exception(
            "Could not generate appointment slots at startup; "
            "the server will continue without new slots."
        )

    app.run(debug=True, port=5000)

``

---

## File: $relativePath

``python
import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()  # Reads .env from the current project directory


def get_connection():
    """Return a MySQL connection, or None if configuration or connection fails."""
    config = {
        "host": os.getenv("CLINICEASE_DB_HOST", "localhost"),
        "port": int(os.getenv("CLINICEASE_DB_PORT", "3306")),
        "database": os.getenv("CLINICEASE_DB_NAME", "clinicease_db"),
        "user": os.getenv("CLINICEASE_DB_USER", "root"),
        "password": os.getenv("CLINICEASE_DB_PASSWORD"),
    }

    if not config["password"]:
        print("[DATABASE ERROR] CLINICEASE_DB_PASSWORD is missing from .env.")
        return None

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection

        connection.close()
    except Error as exc:
        # Avoid printing connection details or credentials in logs.
        print(f"[DATABASE ERROR] MySQL connection failed ({exc.__class__.__name__}).")

    return None

``

---

## File: $relativePath

``python
from models.user import (
    User,
    Patient,
    ClinicStaff,
    PasswordHasherAdapter,
)
from models.appointment import Appointment
from models.slot import AppointmentSlot
from models.reports import generate_appointment_report

``

---

## File: $relativePath

``python
from database import get_connection


# Encapsulation: Status management with property and validation setter
class Appointment:
    VALID_STATUSES = ["Pending", "Confirmed", "Cancelled", "Completed"]
    ALLOWED_TRANSITIONS = {
        "Pending": {"Confirmed", "Cancelled"},
        "Confirmed": {"Completed", "Cancelled"},
        "Cancelled": set(),
        "Completed": set(),
    }

    def __init__(
        self,
        appointment_id: int = None,
        patient_id: int = None,
        slot_id: int = None,
        purpose: str = None,
        status: str = "Pending",
    ):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.slot_id = slot_id
        self.purpose = purpose
        self.__status = None
        self.status = status

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status: '{new_status}'. Allowed values: {self.VALID_STATUSES}"
            )

        if (
            self.__status is not None
            and new_status != self.__status
            and new_status not in self.ALLOWED_TRANSITIONS[self.__status]
        ):
            raise ValueError(
                f"Appointment cannot transition from {self.__status} to {new_status}."
            )

        self.__status = new_status

    def confirm(self):
        if self.__status != "Pending":
            raise ValueError("Only Pending appointments can be confirmed.")
        self.status = "Confirmed"

    def cancel(self):
        if self.__status not in ("Pending", "Confirmed"):
            raise ValueError("Only Pending or Confirmed appointments can be cancelled.")
        self.status = "Cancelled"

    def complete(self):
        if self.__status != "Confirmed":
            raise ValueError("Only Confirmed appointments can be marked as Completed.")
        self.status = "Completed"

    @classmethod
    def create_pending(
        cls,
        cursor,
        patient_id: int,
        slot_id: int,
        purpose: str,
        contact_number=None,
    ) -> int:
        appointment = cls(
            patient_id=patient_id,
            slot_id=slot_id,
            purpose=purpose,
            status="Pending",
        )
        cursor.execute(
            """
            INSERT INTO appointments (user_id, slot_id, purpose, contact_number, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (patient_id, slot_id, purpose, contact_number, appointment.status),
        )
        return cursor.lastrowid

    @staticmethod
    def fetch_by_id(appointment_id: int):
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT a.*, u.email, u.name as patient_name 
                FROM appointments a 
                JOIN users u ON a.user_id = u.user_id 
                WHERE a.appointment_id = %s
            """
            cursor.execute(query, (appointment_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

``

---

## File: $relativePath

``python
from services.dashboard_service import (
    BaseDashboard,
    PatientDashboard,
    StaffDashboard,
    DashboardFactory,
)

``

---

## File: $relativePath

``python
from models.user import PasswordHasherAdapter

``

---

## File: $relativePath

``python
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

``

---

## File: $relativePath

``python
from database import get_connection


# Encapsulation: State protection and concurrency control
class AppointmentSlot:
    VALID_STATUSES = ["Available", "Booked", "Unavailable", "Disabled"]

    def __init__(
        self,
        slot_id: int = None,
        slot_date: str = None,
        time: str = None,
        status: str = "Available",
    ):
        self.slot_id = slot_id
        self.slot_date = slot_date
        self.time = time
        self.__status = None
        self.status = status

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid slot status: '{value}'. Must be one of {self.VALID_STATUSES}."
            )
        self.__status = value

    def is_available(self) -> bool:
        return self.__status == "Available"

    def book(self) -> bool:
        if not self.is_available():
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )
        self.status = "Booked"
        return True

    def book_atomically(self, cursor) -> bool:
        """Claim the slot only if it is still Available in the database."""
        if not self.is_available():
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        cursor.execute(
            """
            UPDATE appointment_slots
            SET status = 'Booked'
            WHERE slot_id = %s
              AND status = 'Available'
              AND slot_date >= CURRENT_DATE
            """,
            (self.slot_id,),
        )
        if cursor.rowcount != 1:
            raise ValueError(
                "This appointment slot is no longer available. Please select another slot."
            )

        self.status = "Booked"
        return True

    def release(self) -> bool:
        self.status = "Available"
        return True

    def disable(self) -> bool:
        self.status = "Disabled"
        return True

    def to_dict(self) -> dict:
        return {
            "slot_id": self.slot_id,
            "slot_date": str(self.slot_date) if self.slot_date else None,
            "time": self.time,
            "status": self.status,
        }

    @staticmethod
    def fetch_by_id(slot_id: int):
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            return AppointmentSlot.fetch_with_cursor(cursor, slot_id)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def fetch_with_cursor(cursor, slot_id: int):
        cursor.execute(
            """
            SELECT slot_id, slot_date, time, status
            FROM appointment_slots
            WHERE slot_id = %s
            """,
            (slot_id,),
        )
        slot_data = cursor.fetchone()
        if not slot_data:
            return None

        return AppointmentSlot(
            slot_id=slot_data["slot_id"],
            slot_date=slot_data["slot_date"],
            time=slot_data["time"],
            status=slot_data["status"],
        )

``

---

## File: $relativePath

``python
import hashlib
import hmac
from typing import Optional

from database import get_connection
from werkzeug.security import check_password_hash, generate_password_hash


# Adapter: password hashing is isolated from the user entity.
class PasswordHasherAdapter:
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if hashed_password.startswith(("scrypt:", "pbkdf2:")):
            return check_password_hash(hashed_password, plain_password)

        legacy_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(legacy_hash, hashed_password)

    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        return not hashed_password.startswith(("scrypt:", "pbkdf2:"))


# Inheritance and Polymorphism: Base user class with private password hash
class User:
    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        password_hash: str,
        contact_number: Optional[str] = None,
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.contact_number = contact_number or None
        self.__password_hash = password_hash

    @property
    def password_hash(self) -> str:
        return self.__password_hash

    def get_user_role(self) -> str:
        return "Base User"

    @staticmethod
    def login(email: str, password: str):
        conn = get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()

            if not user_data:
                return None

            stored_hash = user_data["password_hash"]
            if not PasswordHasherAdapter.verify_password(password, stored_hash):
                return None

            if PasswordHasherAdapter.needs_rehash(stored_hash):
                upgraded_hash = PasswordHasherAdapter.hash_password(password)
                cursor.execute(
                    """
                    UPDATE users
                    SET password_hash = %s
                    WHERE user_id = %s AND password_hash = %s
                    """,
                    (upgraded_hash, user_data["user_id"], stored_hash),
                )
                conn.commit()
                stored_hash = upgraded_hash

            role = user_data["role"]
            if role == "Patient":
                return Patient(
                    user_id=user_data["user_id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=stored_hash,
                    contact_number=user_data.get(
                        "contact_number", user_data.get("phone_number")
                    ),
                )
            elif role == "Clinic Staff":
                return ClinicStaff(
                    user_id=user_data["user_id"],
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=stored_hash,
                    contact_number=user_data.get(
                        "contact_number", user_data.get("phone_number")
                    ),
                )

            return None
        finally:
            cursor.close()
            conn.close()


class Patient(User):
    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        password_hash: str,
        contact_number: Optional[str] = None,
    ):
        super().__init__(
            user_id=user_id,
            name=name,
            email=email,
            password_hash=password_hash,
            contact_number=contact_number,
        )

    def get_user_role(self) -> str:
        return "Patient"

    @classmethod
    def create(
        cls,
        cursor,
        name: str,
        email: str,
        contact_number: Optional[str],
        password: str,
    ) -> int:
        password_hash = PasswordHasherAdapter.hash_password(password)
        return cls.create_with_hash(
            cursor,
            name=name,
            email=email,
            contact_number=contact_number,
            password_hash=password_hash,
        )

    @classmethod
    def create_with_hash(
        cls,
        cursor,
        name: str,
        email: str,
        password_hash: str,
        contact_number: Optional[str] = None,
    ) -> int:
        cursor.execute(
            """
            INSERT INTO users (name, email, contact_number, password_hash, role)
            VALUES (%s, %s, %s, %s, 'Patient')
            """,
            (name, email, contact_number, password_hash),
        )
        return cursor.lastrowid


class ClinicStaff(User):
    def get_user_role(self) -> str:
        return "Clinic Staff"

``

---

## File: $relativePath

``python
from models.user import User, Patient, ClinicStaff, PasswordHasherAdapter

``

---

## File: $relativePath

``text
Flask==3.0.3
mysql-connector-python==8.3.0
python-dotenv==1.2.4
``

---

## File: $relativePath

``python
from services.notification_service import (
    BaseNotificationService,
    ConsoleNotificationService,
    EmailNotificationService,
    NotificationServiceFactory,
)
from services.validation_strategy import (
    BookingValidationStrategy,
    StandardValidationStrategy,
    StrictValidationStrategy,
    RegistrationBookingValidationStrategy,
)
from services.dashboard_service import (
    BaseDashboard,
    PatientDashboard,
    StaffDashboard,
    DashboardFactory,
)
from services.validation_service import ValidationService
from services.registration_service import InitialRequestError, RegistrationService
from services.slot_generator_service import (
    CalendarSlotService,
    SlotGenerationStrategy,
    SlotGeneratorFactory,
    Standard30MinStrategy,
)

``

---

## File: $relativePath

``python
from abc import ABC, abstractmethod


# Abstraction: Base dashboard service contract
class BaseDashboard(ABC):
    def __init__(self, db_connection):
        self.db = db_connection

    @abstractmethod
    def get_slots(self):
        pass


# Concrete dashboard implementations
class PatientDashboard(BaseDashboard):
    def get_slots(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM appointment_slots
            WHERE status = 'Available' AND slot_date >= CURRENT_DATE
            ORDER BY slot_date ASC, time ASC
            """
        )
        slots = cursor.fetchall()
        cursor.close()
        return slots


class StaffDashboard(BaseDashboard):
    def get_slots(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT slots.*,
                   EXISTS (
                       SELECT 1 FROM appointments
                       WHERE appointments.slot_id = slots.slot_id
                   ) AS has_appointments
            FROM appointment_slots AS slots
            WHERE slots.slot_date BETWEEN CURRENT_DATE
                AND DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)
            ORDER BY slots.slot_date ASC, slots.time ASC
            """
        )
        slots = cursor.fetchall()
        cursor.close()
        return slots


# Factory Pattern: Instantiates dashboard service based on user role
class DashboardFactory:
    @staticmethod
    def create_dashboard(user_role: str, db_connection) -> BaseDashboard:
        if user_role == "Patient":
            return PatientDashboard(db_connection)
        elif user_role == "Clinic Staff":
            return StaffDashboard(db_connection)
        else:
            raise ValueError(f"Unknown user role: '{user_role}'")

``

---

## File: $relativePath

``python
from abc import ABC, abstractmethod
from email.message import EmailMessage
import os
import smtplib
import ssl


# Abstraction: Base notification service contract
class BaseNotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        pass


# Concrete notification implementations
class ConsoleNotificationService(BaseNotificationService):
    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        print("[CONSOLE NOTIFICATION]")
        print(f"Recipient: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        return True


class EmailNotificationService(BaseNotificationService):
    def send_notification(self, recipient: str, subject: str, body: str) -> bool:
        host = os.getenv("CLINICEASE_SMTP_HOST")
        sender = os.getenv("CLINICEASE_SMTP_SENDER")
        if not host or not sender:
            raise RuntimeError(
                "SMTP email requires CLINICEASE_SMTP_HOST and CLINICEASE_SMTP_SENDER."
            )

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        port = int(os.getenv("CLINICEASE_SMTP_PORT", "587"))
        username = os.getenv("CLINICEASE_SMTP_USERNAME")
        password = os.getenv("CLINICEASE_SMTP_PASSWORD")
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls(context=ssl.create_default_context())
            if username:
                server.login(username, password or "")
            refused_recipients = server.send_message(message)
            if refused_recipients:
                raise smtplib.SMTPRecipientsRefused(refused_recipients)
        return True


# Factory Pattern: Instantiates notification service based on mode
class NotificationServiceFactory:
    @staticmethod
    def create_service(mode: str = "console") -> BaseNotificationService:
        mode_clean = (mode or "console").strip().lower()

        if mode_clean == "console":
            return ConsoleNotificationService()
        elif mode_clean == "email":
            return EmailNotificationService()
        else:
            raise ValueError(f"Unknown notification mode: '{mode}'. Expected 'console' or 'email'.")

``

---

## File: $relativePath

``python
import mysql.connector

from database import get_connection
from models.appointment import Appointment
from models.slot import AppointmentSlot
from models.user import PasswordHasherAdapter, Patient
from services.validation_service import ValidationService
from services.validation_strategy import (
    RegistrationBookingValidationStrategy,
    StandardValidationStrategy,
)


class InitialRequestError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


class RegistrationService:
    """Creates a patient account and its first appointment in one transaction."""

    def __init__(
        self,
        connection_factory=None,
        validation_strategy=None,
        slot_validation_strategy=None,
    ):
        self.connection_factory = connection_factory or get_connection
        self.validation_strategy = (
            validation_strategy or RegistrationBookingValidationStrategy()
        )
        self.slot_validation_strategy = (
            slot_validation_strategy or StandardValidationStrategy()
        )

    def create_initial_request(self, data):
        is_valid, error = ValidationService.validate_initial_request(data)
        if not is_valid:
            raise InitialRequestError(error or "Incomplete Information.")

        name = data["name"].strip()
        email = data["email"].strip()
        password = data["password"]
        purpose = data["purpose"].strip()
        slot_id = int(data["slot_id"])
        raw_contact_number = data.get("contact_number")
        contact_number = (
            raw_contact_number.strip()
            if isinstance(raw_contact_number, str) and raw_contact_number.strip()
            else None
        )
        password_hash = PasswordHasherAdapter.hash_password(password)

        conn = self.connection_factory()
        if not conn:
            raise InitialRequestError(
                "The appointment service is temporarily unavailable. Please try again.",
                503,
            )

        cursor = None
        try:
            conn.autocommit = False
            conn.start_transaction()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            email_available = cursor.fetchone() is None

            # Lock the database row before validating or changing its encapsulated state.
            cursor.execute(
                """
                SELECT slot_id, slot_date, time, status
                FROM appointment_slots
                WHERE slot_id = %s
                FOR UPDATE
                """,
                (slot_id,),
            )
            slot_data = cursor.fetchone()
            if not slot_data:
                raise InitialRequestError(
                    "This appointment slot is no longer available. Please select another slot.",
                    409,
                )
            slot = AppointmentSlot(
                slot_id=slot_data["slot_id"],
                slot_date=slot_data["slot_date"],
                time=slot_data["time"],
                status=slot_data["status"],
            )

            is_valid, error = self.validation_strategy.validate(
                email_available=email_available,
                slot=slot,
            )
            if not is_valid:
                raise InitialRequestError(error or "The request could not be validated.", 409)

            is_valid, error = self.slot_validation_strategy.validate(
                patient_id=None,
                slot=slot,
            )
            if not is_valid:
                raise InitialRequestError(
                    error or "The appointment slot is not available.",
                    409,
                )

            # Encapsulation: update the model's protected state only through book().
            slot.book()

            try:
                patient_id = Patient.create_with_hash(
                    cursor,
                    name=name,
                    email=email,
                    contact_number=contact_number,
                    password_hash=password_hash,
                )
            except mysql.connector.IntegrityError as error:
                raise InitialRequestError(
                    "This email is already registered.",
                    409,
                ) from error

            Appointment.create_pending(
                cursor,
                patient_id=patient_id,
                slot_id=slot.slot_id,
                purpose=purpose,
                contact_number=contact_number,
            )
            cursor.execute(
                """
                UPDATE appointment_slots
                SET status = %s
                WHERE slot_id = %s AND status = 'Available'
                """,
                (slot.status, slot.slot_id),
            )
            if cursor.rowcount != 1:
                raise InitialRequestError(
                    "This appointment slot is no longer available. Please select another slot.",
                    409,
                )

            cursor.execute("SELECT email FROM users WHERE role = 'Clinic Staff'")
            staff_recipients = [row["email"] for row in cursor.fetchall()]
            conn.commit()

            return {
                "patient_id": patient_id,
                "name": name,
                "email": email,
                "contact_number": contact_number,
                "slot_date": slot.slot_date,
                "slot_time": slot.time,
                "staff_recipients": staff_recipients,
            }
        except InitialRequestError:
            conn.rollback()
            raise
        except ValueError as error:
            conn.rollback()
            raise InitialRequestError(str(error), 409) from error
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

``

---

## File: $relativePath

``python
import calendar
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from typing import Callable, Iterable, List, Optional, Union

from database import get_connection


TimeValue = Union[str, time, timedelta]


class SlotGenerationStrategy(ABC):
    """Strategy contract for splitting clinic hours into appointment times."""

    @abstractmethod
    def generate_slots(
        self,
        start_time: TimeValue,
        end_time: TimeValue,
        duration_minutes: int = 30,
    ) -> Iterable[time]:
        raise NotImplementedError


class Standard30MinStrategy(SlotGenerationStrategy):
    """Generate adjacent 30-minute appointment starts that fit clinic hours."""

    def generate_slots(
        self,
        start_time: TimeValue,
        end_time: TimeValue,
        duration_minutes: int = 30,
    ) -> List[time]:
        if duration_minutes != 30:
            raise ValueError("Standard30MinStrategy requires a 30-minute duration.")

        start = _as_time(start_time)
        end = _as_time(end_time)
        if start >= end:
            raise ValueError("Clinic closing time must be later than opening time.")

        current = datetime.combine(date.min, start)
        closing = datetime.combine(date.min, end)
        duration = timedelta(minutes=duration_minutes)
        slots = []
        while current + duration <= closing:
            slots.append(current.time())
            current += duration
        return slots


class SlotGeneratorFactory:
    """Factory for selecting the clinic's slot-generation strategy."""

    @staticmethod
    def create(strategy_name: str = "standard_30_min") -> SlotGenerationStrategy:
        if strategy_name == "standard_30_min":
            return Standard30MinStrategy()
        raise ValueError(f"Unknown slot-generation strategy: {strategy_name!r}.")


def _as_time(value: TimeValue) -> time:
    if isinstance(value, time):
        return value.replace(tzinfo=None)
    if isinstance(value, timedelta):
        seconds = int(value.total_seconds()) % (24 * 60 * 60)
        return (datetime.min + timedelta(seconds=seconds)).time()
    if isinstance(value, str):
        for format_string in ("%H:%M:%S", "%H:%M", "%I:%M %p"):
            try:
                return datetime.strptime(value, format_string).time()
            except ValueError:
                continue
    raise ValueError(f"Invalid clinic schedule time: {value!r}.")


class CalendarSlotService:
    """Create missing appointment slots from the recurring clinic calendar."""

    def __init__(
        self,
        connection_factory: Optional[Callable] = None,
        strategy: Optional[SlotGenerationStrategy] = None,
        strategy_name: str = "standard_30_min",
        today_provider: Optional[Callable[[], date]] = None,
    ):
        self.connection_factory = connection_factory or get_connection
        self.strategy = strategy or SlotGeneratorFactory.create(strategy_name)
        self.today_provider = today_provider or date.today

    def generate_slots_for_month(self, year: int, month: int) -> int:
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        if isinstance(month, bool) or not isinstance(month, int) or not 1 <= month <= 12:
            raise ValueError("Month must be an integer from 1 to 12.")
        if not 2000 <= year <= 9999:
            raise ValueError("Year must be between 2000 and 9999.")

        month_start = date(year, month, 1)
        month_end = date(year, month, calendar.monthrange(year, month)[1])
        today = self.today_provider()
        if month_end < today:
            raise ValueError("Appointment slots cannot be generated for a past month.")

        return self._generate_slots_for_range(max(month_start, today), month_end)

    def generate_upcoming_slots(self, days_ahead: int = 30) -> int:
        """Generate missing slots for today and the following days."""
        if isinstance(days_ahead, bool) or not isinstance(days_ahead, int) or days_ahead < 1:
            raise ValueError("days_ahead must be a positive integer.")

        start_date = self.today_provider()
        end_date = start_date + timedelta(days=days_ahead - 1)
        return self._generate_slots_for_range(start_date, end_date)

    def _generate_slots_for_range(self, start_date: date, end_date: date) -> int:
        conn = self.connection_factory()
        if not conn:
            raise RuntimeError("Database connection failed while generating slots.")

        cursor = None
        try:
            conn.autocommit = False
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT weekday, open_time, close_time, slot_duration_minutes
                FROM clinic_schedule
                WHERE is_active = 1
                ORDER BY weekday, open_time
                """
            )
            schedule_rows = cursor.fetchall()
            if not schedule_rows:
                raise ValueError(
                    "Clinic hours are not configured. Add an active weekly schedule first."
                )

            cursor.execute(
                """
                SELECT blocked_date
                FROM blocked_dates
                WHERE blocked_date BETWEEN %s AND %s
                """,
                (start_date, end_date),
            )
            blocked_dates = {row["blocked_date"] for row in cursor.fetchall()}

            schedules_by_weekday = {}
            for schedule in schedule_rows:
                weekday = schedule["weekday"]
                if not isinstance(weekday, int) or not 0 <= weekday <= 6:
                    raise ValueError(f"Invalid clinic schedule weekday: {weekday!r}.")
                schedules_by_weekday.setdefault(weekday, []).append(schedule)

            inserted_count = 0
            current_date = start_date
            while current_date <= end_date:
                if (
                    current_date not in blocked_dates
                    and current_date.weekday() in schedules_by_weekday
                ):
                    for schedule in schedules_by_weekday[current_date.weekday()]:
                        duration = schedule["slot_duration_minutes"]
                        if duration != 30:
                            raise ValueError(
                                "The standard slot strategy supports 30-minute schedules only."
                            )
                        for slot_time in self.strategy.generate_slots(
                            schedule["open_time"],
                            schedule["close_time"],
                            duration,
                        ):
                            cursor.execute(
                                """
                                INSERT IGNORE INTO appointment_slots
                                    (slot_date, time, status)
                                VALUES (%s, %s, 'Available')
                                """,
                                (current_date, slot_time.strftime("%I:%M %p")),
                            )
                            inserted_count += max(cursor.rowcount, 0)
                current_date += timedelta(days=1)

            conn.commit()
            return inserted_count
        except Exception:
            conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

``

---

## File: $relativePath

``python
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class BaseValidator(ABC):
    """
    Abstract Base Class defining the contract for input validation.
    Demonstrates Abstraction and Single Responsibility Principle.
    """

    @abstractmethod
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate input value.

        :param value: Value or payload to validate
        :return: (is_valid: bool, error_message: Optional[str])
        """
        pass


class EmailValidator(BaseValidator):
    """
    Validates standard email format and ensures non-empty value.
    """

    EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if not value or not isinstance(value, str) or not value.strip():
            return False, "Email address is required."

        email = value.strip()
        if len(email) > 100:
            return False, "Email address must be 100 characters or fewer."
        if not self.EMAIL_REGEX.match(email):
            return False, "Invalid email format. Please provide a valid email."

        return True, None


class PasswordValidator(BaseValidator):
    """
    Validates password constraints (length, non-empty).
    """

    def __init__(self, min_length: int = 6):
        self.min_length = min_length

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if not value or not isinstance(value, str):
            return False, "Password is required."

        if len(value) < self.min_length:
            return False, f"Password must be at least {self.min_length} characters long."
        if len(value) > 1024:
            return False, "Password must be 1024 characters or fewer."

        return True, None


class NameValidator(BaseValidator):
    """
    Validates full name field.
    """

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if not value or not isinstance(value, str) or not value.strip():
            return False, "Name is required."

        name = value.strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters long."
        if len(name) > 100:
            return False, "Name must be 100 characters or fewer."

        return True, None


class ContactNumberValidator(BaseValidator):
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        if value is None or value == "":
            return True, None
        if not isinstance(value, str):
            return False, "Contact number must be text."

        if not value.strip():
            return True, None

        number = value.strip()
        digits = re.sub(r"\D", "", number)
        if len(digits) < 7 or len(digits) > 15:
            return False, "Enter a contact number with 7 to 15 digits."
        if len(number) > 20:
            return False, "Contact number must be 20 characters or fewer."
        if not re.fullmatch(r"\+?[0-9][0-9().\-\s]*", number):
            return False, "Contact number contains unsupported characters."
        return True, None


class RegistrationValidator(BaseValidator):
    """
    Validates user registration payload (name, email, password).
    """

    def __init__(self):
        self.name_validator = NameValidator()
        self.email_validator = EmailValidator()
        self.contact_number_validator = ContactNumberValidator()
        self.password_validator = PasswordValidator()

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid request payload."

        name = data.get("name")
        email = data.get("email")
        contact_number = data.get("contact_number")
        password = data.get("password")

        is_valid_name, err_name = self.name_validator.validate(name)
        if not is_valid_name:
            return False, err_name

        is_valid_email, err_email = self.email_validator.validate(email)
        if not is_valid_email:
            return False, err_email

        if contact_number is not None:
            is_valid_contact_number, err_contact_number = self.contact_number_validator.validate(
                contact_number
            )
            if not is_valid_contact_number:
                return False, err_contact_number

        is_valid_pass, err_pass = self.password_validator.validate(password)
        if not is_valid_pass:
            return False, err_pass

        return True, None


class LoginValidator(BaseValidator):
    """
    Validates login credentials payload.
    """

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid request payload."

        email = data.get("email")
        password = data.get("password")

        if not email or not isinstance(email, str) or not email.strip():
            return False, "Email is required."

        if not password or not isinstance(password, str):
            return False, "Password is required."

        return True, None


class BookingValidator(BaseValidator):
    """
    Validates appointment booking payload.
    """

    def validate(self, data: Any) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Invalid request payload."

        slot_id = data.get("slot_id")
        if slot_id is None:
            return False, "Slot ID is required."

        try:
            int(slot_id)
        except (ValueError, TypeError):
            return False, "Slot ID must be a valid integer."

        purpose = data.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            return False, "Purpose of visit is required."
        if len(purpose.strip()) > 255:
            return False, "Purpose exceeds maximum allowed length of 255 characters."

        contact_number = data.get("contact_number")
        if contact_number is not None:
            is_valid_contact_number, err_contact_number = ContactNumberValidator().validate(
                contact_number
            )
            if not is_valid_contact_number:
                return False, err_contact_number

        return True, None


class ValidationService:
    """
    Service Layer / Facade providing high-level validation routines.
    """

    _email_validator = EmailValidator()
    _password_validator = PasswordValidator()
    _name_validator = NameValidator()
    _registration_validator = RegistrationValidator()
    _login_validator = LoginValidator()
    _booking_validator = BookingValidator()

    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, Optional[str]]:
        return cls._email_validator.validate(email)

    @classmethod
    def validate_password(cls, password: str, min_length: int = 6) -> Tuple[bool, Optional[str]]:
        return PasswordValidator(min_length=min_length).validate(password)

    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, Optional[str]]:
        return cls._name_validator.validate(name)

    @classmethod
    def validate_registration(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return cls._registration_validator.validate(data)

    @classmethod
    def validate_initial_request(
        cls, data: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        if not isinstance(data, dict):
            return False, "Incomplete Information."

        required_fields = ("name", "email", "password", "slot_id", "purpose")
        if any(
            data.get(field) is None
            or not isinstance(data.get(field), (str, int))
            or not str(data.get(field)).strip()
            for field in required_fields
        ):
            return False, "Incomplete Information."

        is_valid, error = cls.validate_registration(data)
        if not is_valid:
            return False, error

        return cls.validate_booking(data)

    @classmethod
    def validate_login(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return cls._login_validator.validate(data)

    @classmethod
    def validate_booking(cls, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return cls._booking_validator.validate(data)

``

---

## File: $relativePath

``python
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from models.slot import AppointmentSlot
from database import get_connection


# Strategy Pattern: Validation contract for booking attempts
class BookingValidationStrategy(ABC):
    @abstractmethod
    def validate(
        self, patient_id: Optional[int], slot: Optional[AppointmentSlot], db_connection=None
    ) -> Tuple[bool, Optional[str]]:
        pass


class StandardValidationStrategy(BookingValidationStrategy):
    def validate(
        self, patient_id: Optional[int], slot: Optional[AppointmentSlot], db_connection=None
    ) -> Tuple[bool, Optional[str]]:
        if not slot or not slot.is_available():
            return False, "This appointment slot is no longer available. Please select another slot."
        return True, None


class RegistrationBookingValidationStrategy:
    """Validates the database-dependent branches of the combined sign-up flow."""

    def validate(
        self, email_available: bool, slot: Optional[AppointmentSlot]
    ) -> Tuple[bool, Optional[str]]:
        if not email_available:
            return False, "This email is already registered."
        if not slot or not slot.is_available():
            return (
                False,
                "This appointment slot is no longer available. Please select another slot.",
            )
        return True, None


class StrictValidationStrategy(BookingValidationStrategy):
    def validate(
        self, patient_id: Optional[int], slot: Optional[AppointmentSlot], db_connection=None
    ) -> Tuple[bool, Optional[str]]:
        if not slot or not slot.is_available():
            return False, "This appointment slot is no longer available. Please select another slot."
        if patient_id is None:
            return False, "Patient information is required for booking validation."

        conn = db_connection or get_connection()
        if not conn:
            return False, "Database connection unavailable for validation."

        should_close = db_connection is None
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT appointment_id FROM appointments 
                WHERE user_id = %s AND status = 'Pending'
                """,
                (patient_id,),
            )
            existing_pending = cursor.fetchone()
            if existing_pending:
                return (
                    False,
                    "You already have a Pending appointment request. Please wait for staff review before requesting another.",
                )
            return True, None
        finally:
            cursor.close()
            if should_close:
                conn.close()

``

---

## File: $relativePath

``css
:root {
    --color-primary: #486B52;
    --color-primary-hover: #3F6047;
    --color-pale-sage: #E5EEE3;
    --color-bg: #FAF8F1;
    --color-surface: #FFFFFF;
    --color-text-heading: #34443A;
    --color-text-body: #46534A;
    --color-border: #D9E1D7;
    --color-input-border: #6F7F73;
    --status-pending-bg: #FFF1D6;
    --status-pending-text: #754A00;
    --status-confirmed-bg: #E8F0FE;
    --status-confirmed-text: #1A47A0;
    --status-completed-bg: #E2F2E7;
    --status-completed-text: #205C37;
    --status-cancelled-bg: #FCE8E6;
    --status-cancelled-text: #8B2C27;
    --font-main: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    --text-heading: 24px;
    --text-body: 16px;
    --text-caption: 14px;
    --radius-card: 12px;
    --radius-btn: 8px;
    --radius-input: 8px;
    --shadow-soft: 0 2px 8px rgba(52, 68, 58, 0.06);
}

* {
    box-sizing: border-box;
}

html {
    min-width: 320px;
    scroll-behavior: smooth;
}

body {
    min-height: 100vh;
    margin: 0;
    display: flex;
    flex-direction: column;
    background: var(--color-bg);
    color: var(--color-text-body);
    font-family: var(--font-main);
    font-size: var(--text-body);
    line-height: 1.6;
}

button,
input,
select,
textarea {
    font: inherit;
}

a {
    color: var(--color-primary);
    text-underline-offset: 0.18em;
}

a:hover {
    color: var(--color-primary-hover);
}

:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

h1,
h2,
h3,
h4 {
    margin: 0;
    color: var(--color-text-heading);
    line-height: 1.3;
}

h1,
h2 {
    font-size: var(--text-heading);
}

h3 {
    font-size: 20px;
}

p {
    margin: 0;
}

.container {
    width: min(100% - 40px, 1120px);
    margin-inline: auto;
}

.container-narrow {
    width: min(100% - 40px, 500px);
    margin-inline: auto;
}

.header {
    position: relative;
    z-index: 10;
    border-bottom: 1px solid var(--color-border);
    background: var(--color-surface);
}

.header-content {
    min-height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}

.brand {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    color: var(--color-text-heading);
    font-size: 19px;
    font-weight: 700;
    text-decoration: none;
}

.brand:hover {
    color: var(--color-text-heading);
}

.brand-icon {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    border-radius: var(--radius-btn);
    background: var(--color-primary);
    color: var(--color-surface);
    font-size: 16px;
}

.nav-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 12px;
}

.nav-user {
    color: var(--color-text-heading);
    font-weight: 600;
}

.main-content {
    flex: 1 0 auto;
    padding-block: 36px 48px;
}

.footer {
    padding-block: 20px;
    border-top: 1px solid var(--color-border);
    background: var(--color-surface);
    color: var(--color-text-body);
    font-size: var(--text-caption);
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px 24px;
}

@media (max-width: 600px) {
    .container,
    .container-narrow {
        width: min(100% - 28px, 1120px);
    }

    .main-content {
        padding-block: 24px 36px;
    }

    .header-content {
        min-height: 64px;
        gap: 12px;
    }

    .nav-actions {
        gap: 8px;
    }

    .nav-user {
        display: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }
}

``

---

## File: $relativePath

``css
.btn {
    min-height: 48px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 18px;
    border: 1px solid transparent;
    border-radius: var(--radius-btn);
    cursor: pointer;
    font-size: var(--text-body);
    font-weight: 650;
    line-height: 1.3;
    text-align: center;
    text-decoration: none;
    transition: background-color 120ms ease, border-color 120ms ease, color 120ms ease;
}

.btn:hover {
    text-decoration: none;
}

.btn:disabled {
    cursor: wait;
    opacity: 0.65;
}

.btn-primary {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: var(--color-surface);
}

.btn-primary:hover {
    border-color: var(--color-primary-hover);
    background: var(--color-primary-hover);
    color: var(--color-surface);
}

.btn-secondary {
    border-color: var(--color-border);
    background: var(--color-surface);
    color: var(--color-text-heading);
}

.btn-secondary:hover {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
    color: var(--color-text-heading);
}

.btn-danger {
    border-color: var(--status-cancelled-text);
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
}

.btn-danger:hover {
    background: #F7D9D6;
    color: var(--status-cancelled-text);
}

.btn-sm {
    min-height: 44px;
    padding: 8px 12px;
    font-size: var(--text-caption);
}

.btn-block {
    width: 100%;
}

.card {
    padding: 24px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
    box-shadow: var(--shadow-soft);
}

.card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--color-border);
}

.card-header p {
    margin-top: 6px;
}

.alert {
    padding: 12px 14px;
    margin-bottom: 18px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    font-size: var(--text-body);
}

.alert-error {
    border-color: var(--status-cancelled-text);
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
}

.alert-success {
    border-color: var(--status-completed-text);
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
}

.status-badge,
.badge-pending,
.badge-confirmed,
.badge-completed,
.badge-cancelled {
    min-height: 30px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: var(--text-caption);
    font-weight: 650;
    line-height: 1.35;
    white-space: nowrap;
}

.status-pending,
.badge-pending {
    background: var(--status-pending-bg);
    color: var(--status-pending-text);
}

.status-confirmed,
.badge-confirmed {
    background: var(--status-confirmed-bg);
    color: var(--status-confirmed-text);
}

.status-completed,
.badge-completed {
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
}

.status-cancelled,
.badge-cancelled {
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
}

.form-group {
    margin-bottom: 18px;
}

.form-label {
    display: block;
    margin-bottom: 6px;
    color: var(--color-text-heading);
    font-size: var(--text-body);
    font-weight: 650;
}

.form-input,
.form-textarea,
.form-select {
    width: 100%;
    min-height: 48px;
    padding: 10px 12px;
    border: 1px solid var(--color-input-border);
    border-radius: var(--radius-input);
    background: var(--color-surface);
    color: var(--color-text-heading);
    font-size: var(--text-body);
}

.form-textarea {
    min-height: 120px;
    resize: vertical;
}

.form-help {
    margin-top: 6px;
    color: var(--color-text-body);
    font-size: var(--text-caption);
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
    border-color: var(--color-primary);
}

.table-responsive {
    width: 100%;
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.data-table th {
    padding: 12px 14px;
    border-bottom: 2px solid var(--color-border);
    color: var(--color-text-heading);
    font-size: var(--text-body);
    font-weight: 700;
}

.data-table td {
    padding: 14px;
    border-bottom: 1px solid var(--color-border);
    vertical-align: middle;
}

.data-table tbody tr:hover {
    background: #F7F8F4;
}

.modal-backdrop {
    position: fixed;
    z-index: 1000;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(52, 68, 58, 0.48);
}

.modal-dialog {
    position: relative;
    width: min(100%, 500px);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
    box-shadow: var(--shadow-soft);
}

.modal-header {
    padding: 22px 24px 16px;
    border-bottom: 1px solid var(--color-border);
}

.modal-header p {
    margin-top: 6px;
}

.modal-body {
    padding: 20px 24px 24px;
}

.modal-close-btn {
    position: absolute;
    top: 12px;
    right: 14px;
    width: 44px;
    height: 44px;
    border: 1px solid transparent;
    border-radius: var(--radius-btn);
    background: transparent;
    color: var(--color-text-heading);
    cursor: pointer;
    font-size: 24px;
}

.modal-close-btn:hover {
    background: var(--color-pale-sage);
}

.hidden {
    display: none !important;
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

.toast {
    position: fixed;
    z-index: 1100;
    right: 16px;
    bottom: 16px;
    width: min(460px, calc(100% - 32px));
    padding: 14px 16px;
    border: 1px solid var(--status-completed-text);
    border-radius: var(--radius-btn);
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
    box-shadow: var(--shadow-soft);
    font-weight: 600;
}

.toast-error {
    border-color: var(--status-cancelled-text);
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
}

``

---

## File: $relativePath

``css
.test-panel {
    max-width: 820px;
}

.test-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding-bottom: 24px;
}

.test-heading p {
    margin-top: 6px;
}

.test-section {
    margin-bottom: 20px;
}

.test-section h2 {
    margin-bottom: 16px;
}

.test-response {
    min-height: 48px;
    padding: 12px;
    margin: 16px 0;
    overflow-x: auto;
    border-radius: var(--radius-btn);
    background: var(--color-bg);
    color: var(--color-text-heading);
    font: 14px/1.5 ui-monospace, SFMono-Regular, Consolas, monospace;
    white-space: pre-wrap;
}

.slot-table {
    margin-top: 16px;
}

@media (max-width: 640px) {
    .test-heading {
        align-items: flex-start;
        flex-direction: column;
    }
}

``

---

## File: $relativePath

``css
.auth-page {
    max-width: 1080px;
}

.auth-page-create {
    max-width: 1080px;
}

.auth-card {
    margin-block: 24px;
}

.auth-heading {
    margin-bottom: 22px;
}

.auth-heading p {
    margin-top: 8px;
}

.auth-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px;
    padding: 4px;
    margin-bottom: 22px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    background: var(--color-bg);
}

.auth-tab {
    min-height: 48px;
    padding: 8px 12px;
    border: 1px solid transparent;
    border-radius: 6px;
    background: transparent;
    color: var(--color-text-heading);
    cursor: pointer;
    font-weight: 650;
}

.auth-tab[aria-selected="true"] {
    border-color: var(--color-border);
    background: var(--color-surface);
}

.auth-page-login #sign-in-panel {
    max-width: 480px;
    margin-inline: auto;
}

.auth-page-login {
    max-width: 480px;
}

.auth-switch {
    margin-top: 20px;
    text-align: center;
}

.registration-layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(330px, 0.92fr);
    align-items: start;
    gap: 28px;
    margin-bottom: 22px;
}

.registration-fields {
    padding-top: 4px;
}

.registration-fields .form-group:last-child {
    margin-bottom: 0;
}

.availability-panel {
    min-width: 0;
    padding: 20px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
}

.availability-heading {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-bottom: 14px;
}

.availability-heading h2 {
    font-size: 20px;
}

.availability-heading p:not(.calendar-month) {
    margin-top: 4px;
    font-size: var(--text-caption);
}

.calendar-navigation {
    display: grid;
    grid-template-columns: 44px 1fr 44px;
    align-items: center;
    gap: 8px;
}

.calendar-nav-button {
    width: 44px;
    min-height: 44px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    background: var(--color-surface);
    color: var(--color-text-heading);
    cursor: pointer;
    font-size: 20px;
}

.calendar-nav-button:hover:not(:disabled) {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
}

.calendar-nav-button:disabled {
    cursor: not-allowed;
    opacity: 0.45;
}

.calendar-month {
    color: var(--color-text-heading);
    font-weight: 700;
    text-align: center;
}

.availability-calendar {
    display: grid;
    grid-template-columns: repeat(7, minmax(34px, 1fr));
    gap: 4px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--color-border);
}

.calendar-weekday,
.calendar-day,
.calendar-empty {
    display: grid;
    min-width: 0;
    min-height: 44px;
    place-items: center;
}

.calendar-weekday {
    color: var(--color-text-body);
    font-size: var(--text-caption);
    font-weight: 700;
}

.calendar-day {
    padding: 0;
    border: 1px solid transparent;
    border-radius: 6px;
    background: transparent;
    color: var(--color-text-heading);
    font-size: var(--text-caption);
}

.calendar-day--available {
    border-color: var(--color-border);
    background: var(--color-surface);
    cursor: pointer;
    font-weight: 650;
}

.calendar-day--available:hover {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
}

.calendar-day[aria-pressed="true"] {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: var(--color-surface);
}

.calendar-day:disabled {
    color: var(--color-text-body);
}

.available-times {
    padding-top: 14px;
}

.available-times h3 {
    font-size: 16px;
}

.available-times-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.available-time-button {
    min-height: 44px;
    padding: 8px 12px;
    border: 1px solid var(--color-border);
    border-radius: 6px;
    background: var(--color-surface);
    color: var(--color-text-heading);
    cursor: pointer;
    font-size: var(--text-caption);
    font-weight: 600;
}

.available-time-button:hover,
.available-time-button[aria-pressed="true"] {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
}

.available-time-button[aria-pressed="true"] {
    box-shadow: inset 0 0 0 1px var(--color-primary);
}

.availability-message {
    margin-bottom: 12px;
}

.calendar-feedback {
    margin: 12px 0 0;
}

@media (max-width: 760px) {
    .registration-layout {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .availability-panel {
        padding: 16px;
    }
}

@media (max-width: 480px) {
    .auth-card {
        padding: 18px;
    }

    .availability-calendar {
        gap: 2px;
    }

    .calendar-weekday,
    .calendar-day,
    .calendar-empty {
        min-height: 44px;
    }
}

``

---

## File: $relativePath

``css
.hero-section {
    max-width: 780px;
    margin-inline: auto;
    padding-block: 54px;
    text-align: center;
}

.hero-title {
    margin: 12px 0 16px;
    color: var(--color-text-heading);
    font-size: clamp(32px, 5vw, 44px);
    line-height: 1.2;
}

.hero-description {
    max-width: 660px;
    margin: 0 auto 24px;
    font-size: 18px;
}

.hero-actions {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
}

.section-block {
    padding-block: 48px;
    border-block: 1px solid var(--color-border);
    background: var(--color-surface);
}

.section-header {
    max-width: 720px;
    margin: 0 auto 28px;
    text-align: center;
}

.section-title {
    color: var(--color-text-heading);
    font-size: var(--text-heading);
}

.section-subtitle {
    margin-top: 8px;
}

.grid-3,
.grid-4 {
    display: grid;
    gap: 20px;
}

.grid-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}

.grid-4 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
}

.step-num {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    margin-bottom: 12px;
    border-radius: var(--radius-btn);
    background: var(--color-pale-sage);
    color: var(--color-text-heading);
    font-weight: 700;
}

.status-card {
    text-align: center;
}

.status-card p {
    margin-top: 8px;
}

@media (max-width: 800px) {
    .grid-3,
    .grid-4 {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 600px) {
    .hero-section {
        padding-block: 36px;
    }
}

``

---

## File: $relativePath

``css
.patient-dashboard {
    max-width: 1180px;
    padding-block: 8px 48px;
}

.patient-dashboard [hidden] {
    display: none !important;
}

.dashboard-welcome {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 32px;
    padding: 28px 32px;
    margin-bottom: 28px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
    box-shadow: var(--shadow-soft);
}

.dashboard-welcome h1 {
    margin: 4px 0 8px;
    font-size: clamp(28px, 3vw, 36px);
}

.dashboard-welcome p:not(.eyebrow) {
    font-size: 17px;
}

.eyebrow {
    color: var(--color-primary);
    font-size: 13px;
    font-weight: 750;
    letter-spacing: 0.1em;
}

.welcome-summary {
    display: flex;
    align-items: stretch;
    gap: 12px;
}

.summary-item {
    min-width: 108px;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    column-gap: 8px;
    padding: 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    background: var(--color-bg);
}

.summary-item > .material-symbols-outlined {
    grid-row: span 2;
    color: var(--color-primary);
    font-size: 24px;
}

.summary-count {
    color: var(--color-text-heading);
    font-size: 20px;
    font-weight: 750;
    line-height: 1.1;
}

.summary-label {
    font-size: 12px;
    line-height: 1.3;
}

.dashboard-tabs {
    display: flex;
    gap: 8px;
    padding: 6px;
    margin-bottom: 26px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: #F1F3EE;
}

.dashboard-tab {
    min-height: 54px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex: 1;
    padding: 10px 18px;
    border: 0;
    border-radius: 8px;
    background: transparent;
    color: var(--color-text-heading);
    cursor: pointer;
    font-size: 17px;
    font-weight: 700;
}

.dashboard-tab:hover {
    background: #E5EEE3;
}

.dashboard-tab.is-active {
    background: var(--color-primary);
    color: var(--color-surface);
    box-shadow: 0 2px 5px rgba(52, 68, 58, 0.16);
}

.dashboard-tab .material-symbols-outlined {
    font-size: 23px;
}

.panel-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 24px;
}

.panel-heading h2 {
    font-size: 27px;
}

.panel-heading p {
    margin-top: 5px;
    font-size: 16px;
}

.appointment-group {
    margin-bottom: 30px;
}

.group-heading {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}

.group-heading h3 {
    font-size: 21px;
}

.group-count {
    min-width: 30px;
    min-height: 30px;
    display: inline-grid;
    place-items: center;
    padding-inline: 8px;
    border-radius: 20px;
    background: var(--color-pale-sage);
    color: var(--color-text-heading);
    font-size: 14px;
    font-weight: 700;
}

.appointment-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
}

.appointment-card {
    min-width: 0;
    min-height: 124px;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    border-left: 5px solid var(--color-primary);
    background: var(--color-surface);
    color: var(--color-text-body);
    cursor: pointer;
    text-align: left;
    box-shadow: var(--shadow-soft);
    transition: border-color 140ms ease, box-shadow 140ms ease, transform 140ms ease;
}

.appointment-card:hover {
    border-color: var(--color-primary);
    box-shadow: 0 5px 16px rgba(52, 68, 58, 0.1);
    transform: translateY(-1px);
}

.appointment-card--past {
    border-left-color: #87948A;
}

.appointment-card__date-icon {
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    flex: 0 0 48px;
    border-radius: 50%;
    background: var(--color-pale-sage);
    color: var(--color-primary);
    font-size: 25px;
}

.appointment-card__main {
    min-width: 0;
    display: flex;
    flex: 1;
    flex-direction: column;
    gap: 2px;
}

.appointment-card__date {
    color: var(--color-text-heading);
    font-size: 16px;
    font-weight: 700;
}

.appointment-card__time {
    color: var(--color-text-heading);
    font-size: 19px;
    font-weight: 750;
}

.appointment-card__purpose {
    overflow: hidden;
    font-size: 14px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.appointment-card__open {
    flex: 0 0 auto;
    color: var(--color-text-body);
}

.status-badge {
    min-height: 34px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 5px 10px;
    border-radius: 7px;
    font-size: 14px;
    font-weight: 750;
    white-space: nowrap;
}

.status-badge .material-symbols-outlined {
    font-size: 19px;
}

.status-pending {
    background: var(--status-pending-bg);
    color: var(--status-pending-text);
}

.status-confirmed {
    background: var(--status-confirmed-bg);
    color: var(--status-confirmed-text);
}

.status-completed {
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
}

.status-cancelled {
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
}

.past-appointment-group {
    padding-top: 4px;
}

.empty-state,
.empty-history {
    padding: 30px;
    border: 1px dashed var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
    text-align: center;
}

.empty-state > .material-symbols-outlined {
    display: block;
    margin-bottom: 8px;
    color: var(--color-primary);
    font-size: 38px;
}

.empty-state h4,
.empty-state h3 {
    margin-bottom: 6px;
    color: var(--color-text-heading);
    font-size: 20px;
}

.empty-state p {
    margin-bottom: 18px;
}

.empty-history {
    color: var(--color-text-body);
    text-align: left;
}

.booking-stepper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    padding: 0;
    margin: 0 0 22px;
    list-style: none;
}

.booking-step {
    position: relative;
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
    padding: 10px 16px;
    color: #59665C;
}

.booking-step:not(:last-child)::after {
    position: absolute;
    top: 50%;
    right: -4px;
    width: 32px;
    height: 2px;
    background: var(--color-border);
    content: "";
}

.booking-step__number {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    flex: 0 0 40px;
    border: 2px solid #9AA69C;
    border-radius: 50%;
    background: var(--color-surface);
    color: var(--color-text-heading);
    font-size: 17px;
    font-weight: 750;
}

.booking-step > span:last-child {
    display: flex;
    flex-direction: column;
    line-height: 1.35;
}

.booking-step strong {
    color: var(--color-text-heading);
    font-size: 15px;
}

.booking-step small {
    margin-top: 2px;
    font-size: 13px;
}

.booking-step.is-current .booking-step__number,
.booking-step.is-complete .booking-step__number {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: var(--color-surface);
}

.booking-step.is-current strong,
.booking-step.is-complete strong {
    color: var(--color-primary);
}

.booking-selection-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.05fr) minmax(340px, 0.95fr);
    align-items: stretch;
    gap: 20px;
}

.booking-card {
    min-width: 0;
    padding: 24px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
    box-shadow: var(--shadow-soft);
}

.booking-card__heading {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-bottom: 22px;
}

.booking-card__heading > .material-symbols-outlined {
    color: var(--color-primary);
    font-size: 27px;
}

.booking-card__heading h3 {
    font-size: 21px;
}

.booking-card__heading p {
    margin-top: 4px;
    font-size: 14px;
}

.calendar-toolbar {
    display: grid;
    grid-template-columns: 48px 1fr 48px;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.calendar-toolbar h4 {
    font-size: 19px;
    text-align: center;
}

.calendar-nav-button {
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    background: var(--color-surface);
    color: var(--color-text-heading);
    cursor: pointer;
}

.calendar-nav-button:hover:not(:disabled) {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
}

.calendar-nav-button:disabled {
    cursor: not-allowed;
    opacity: 0.45;
}

.calendar-nav-button .material-symbols-outlined {
    font-size: 25px;
}

.availability-calendar {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 6px;
}

.calendar-weekday {
    display: grid;
    min-height: 38px;
    place-items: center;
    color: var(--color-text-body);
    font-size: 13px;
    font-weight: 750;
}

.calendar-empty,
.calendar-day {
    min-width: 0;
    min-height: 48px;
    display: grid;
    place-items: center;
}

.calendar-day {
    border: 1px solid transparent;
    border-radius: 8px;
    background: transparent;
    color: #7A857C;
    font-size: 16px;
    font-weight: 600;
}

.calendar-day:disabled {
    cursor: not-allowed;
    opacity: 0.55;
}

.calendar-day--available {
    border-color: var(--color-border);
    background: #F7FAF6;
    color: var(--color-text-heading);
    cursor: pointer;
}

.calendar-day--available:hover {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
}

.calendar-day--today {
    box-shadow: inset 0 0 0 2px #8CA392;
}

.calendar-day--selected,
.calendar-day--selected:hover {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: var(--color-surface);
}

.selection-hint {
    min-height: 26px;
    margin-top: 14px;
    color: var(--color-text-body);
    font-size: 14px;
}

.inline-feedback {
    padding: 12px 14px;
    margin-top: 14px;
    border: 1px solid var(--status-cancelled-text);
    border-radius: var(--radius-btn);
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
}

.available-times-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.time-slot-button {
    min-height: 54px;
    padding: 10px 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    background: var(--color-surface);
    color: var(--color-text-heading);
    cursor: pointer;
    font-size: 16px;
    font-weight: 700;
}

.time-slot-button:hover {
    border-color: var(--color-primary);
    background: var(--color-pale-sage);
}

.time-slot-button.is-selected {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: var(--color-surface);
}

.time-empty-state {
    min-height: 180px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: var(--color-text-body);
    text-align: center;
}

.time-empty-state .material-symbols-outlined {
    color: #6C7B70;
    font-size: 38px;
}

.wizard-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 24px;
}

.wizard-actions .btn {
    min-height: 52px;
}

.wizard-actions--selection {
    justify-content: flex-end;
}

.booking-details {
    max-width: 760px;
    margin-inline: auto;
}

.booking-summary {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    padding: 16px;
    margin-bottom: 24px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    background: var(--color-bg);
}

.booking-summary > div {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.summary-caption {
    color: var(--color-text-body);
    font-size: 13px;
    font-weight: 650;
}

.booking-summary strong {
    color: var(--color-text-heading);
    font-size: 17px;
}

.optional-label {
    color: var(--color-text-body);
    font-size: 14px;
    font-weight: 400;
}

.booking-details .form-textarea {
    min-height: 120px;
}

.booking-details .form-input,
.booking-details .form-textarea {
    min-height: 54px;
    font-size: 17px;
}

.booking-empty-state {
    margin-top: 20px;
}

.modal-backdrop {
    overflow-y: auto;
}

.appointment-details-modal {
    width: min(100%, 620px);
    max-height: calc(100vh - 40px);
    overflow-y: auto;
}

.appointment-details-modal .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding-right: 64px;
}

.appointment-details-modal .modal-header h2 {
    font-size: 23px;
}

.appointment-details-list {
    display: grid;
    gap: 0;
    margin: 0;
}

.appointment-details-list > div {
    display: grid;
    grid-template-columns: minmax(130px, 0.8fr) minmax(0, 1.2fr);
    gap: 16px;
    padding: 12px 0;
    border-bottom: 1px solid var(--color-border);
}

.appointment-details-list dt {
    color: var(--color-text-body);
    font-size: 14px;
    font-weight: 650;
}

.appointment-details-list dd {
    margin: 0;
    color: var(--color-text-heading);
    font-size: 15px;
    overflow-wrap: anywhere;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 20px;
}

@media (max-width: 900px) {
    .dashboard-welcome {
        align-items: flex-start;
        flex-direction: column;
    }

    .welcome-summary {
        width: 100%;
    }

    .summary-item {
        flex: 1;
    }

    .appointment-list {
        grid-template-columns: 1fr;
    }

    .booking-selection-grid {
        grid-template-columns: minmax(0, 1fr) minmax(300px, 0.9fr);
        gap: 14px;
    }

    .booking-card {
        padding: 20px;
    }
}

@media (max-width: 680px) {
    .patient-dashboard {
        padding-top: 0;
    }

    .dashboard-welcome {
        gap: 20px;
        padding: 22px;
    }

    .welcome-summary {
        gap: 8px;
    }

    .summary-item {
        min-width: 0;
        grid-template-columns: 1fr;
        justify-items: center;
        gap: 4px;
        padding: 10px 6px;
        text-align: center;
    }

    .summary-item > .material-symbols-outlined {
        grid-row: auto;
    }

    .summary-label {
        font-size: 11px;
    }

    .dashboard-tabs {
        position: sticky;
        top: 0;
        z-index: 5;
        margin-inline: -2px;
    }

    .dashboard-tab {
        min-height: 52px;
        gap: 6px;
        padding: 8px;
        font-size: 14px;
    }

    .dashboard-tab .material-symbols-outlined {
        font-size: 21px;
    }

    .panel-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .panel-heading .btn {
        width: 100%;
    }

    .appointment-card {
        gap: 11px;
        padding: 15px 12px;
    }

    .appointment-card__date-icon {
        width: 40px;
        height: 40px;
        flex-basis: 40px;
        font-size: 22px;
    }

    .appointment-card__date {
        font-size: 14px;
    }

    .appointment-card__time {
        font-size: 17px;
    }

    .appointment-card__purpose {
        max-width: 180px;
        font-size: 13px;
    }

    .appointment-card .status-badge {
        min-height: 30px;
        gap: 4px;
        padding: 4px 7px;
        font-size: 12px;
    }

    .appointment-card .status-badge .material-symbols-outlined {
        font-size: 17px;
    }

    .appointment-card__open {
        display: none;
    }

    .booking-stepper {
        margin-inline: -8px;
    }

    .booking-step {
        align-items: flex-start;
        flex-direction: column;
        gap: 7px;
        padding: 8px;
    }

    .booking-step:not(:last-child)::after {
        top: 28px;
        right: -6px;
        width: 18px;
    }

    .booking-step__number {
        width: 34px;
        height: 34px;
        flex-basis: 34px;
        font-size: 15px;
    }

    .booking-step strong {
        font-size: 12px;
    }

    .booking-step small {
        font-size: 11px;
    }

    .booking-selection-grid {
        grid-template-columns: 1fr;
    }

    .booking-card {
        padding: 18px;
    }

    .calendar-day {
        min-height: 44px;
    }

    .wizard-actions--selection {
        justify-content: stretch;
    }

    .wizard-actions--selection .btn {
        width: 100%;
    }

    .wizard-actions--details {
        align-items: stretch;
        flex-direction: column-reverse;
    }

    .wizard-actions--details .btn {
        width: 100%;
    }

    .booking-summary {
        padding: 12px;
    }

    .booking-summary strong {
        font-size: 15px;
    }

    .modal-backdrop {
        align-items: flex-start;
        padding: 12px;
    }

    .appointment-details-modal {
        max-height: calc(100vh - 24px);
    }

    .appointment-details-modal .modal-header {
        align-items: flex-start;
        flex-direction: column;
        padding-right: 48px;
    }

    .appointment-details-list > div {
        grid-template-columns: minmax(100px, 0.75fr) minmax(0, 1.25fr);
        gap: 10px;
    }

    .modal-actions {
        align-items: stretch;
        flex-direction: column-reverse;
    }
}

@media (prefers-reduced-motion: reduce) {
    .appointment-card {
        transition: none;
    }
}

``

---

## File: $relativePath

``css
/* Staff Dashboard - Desktop-First with Sidebar */

.staff-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 100vh;
    background: var(--color-bg);
}

/* Sidebar Styles */
.staff-sidebar {
    background: var(--color-surface);
    border-right: 1px solid var(--color-border);
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}

.sidebar-header {
    padding: 24px;
    border-bottom: 1px solid var(--color-border);
}

.sidebar-header .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.sidebar-header .brand-icon {
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    border-radius: var(--radius-btn);
    background: var(--color-primary);
    color: var(--color-surface);
    font-weight: 700;
    font-size: 16px;
}

.sidebar-header .brand-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--color-text-heading);
}

.user-info {
    font-size: 14px;
    color: var(--color-text-body);
    margin: 0;
}

.sidebar-nav {
    flex: 1;
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border: none;
    background: transparent;
    color: var(--color-text-body);
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    border-radius: var(--radius-btn);
    transition: all 150ms ease;
    text-align: left;
    width: 100%;
}

.nav-item:hover {
    background: var(--color-pale-sage);
    color: var(--color-text-heading);
}

.nav-item.active {
    background: var(--color-primary);
    color: var(--color-surface);
}

.nav-item .material-symbols-outlined {
    font-size: 20px;
}

.badge-count {
    margin-left: auto;
    background: var(--color-primary);
    color: var(--color-surface);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 700;
}

.nav-item.active .badge-count {
    background: var(--color-surface);
    color: var(--color-primary);
}

.sidebar-footer {
    padding: 16px;
    border-top: 1px solid var(--color-border);
}

.sidebar-footer .btn {
    width: 100%;
}

/* Main Content Area */
.staff-main {
    padding: 32px 40px;
    overflow-y: auto;
}

.content-section {
    display: none;
}

.content-section.active {
    display: block;
}

.section-header {
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 2px solid var(--color-border);
}

.section-header h1 {
    font-size: 28px;
    margin-bottom: 8px;
    color: var(--color-text-heading);
}

.section-header p {
    font-size: 16px;
    color: var(--color-text-body);
    margin: 0;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}

.stat-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 24px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    box-shadow: var(--shadow-soft);
    transition: transform 150ms ease;
}

.stat-card:hover {
    transform: translateY(-2px);
}

.stat-icon {
    width: 56px;
    height: 56px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: var(--color-pale-sage);
}

.stat-icon .material-symbols-outlined {
    font-size: 28px;
}

.stat-pending .stat-icon {
    background: var(--status-pending-bg);
    color: var(--status-pending-text);
}

.stat-confirmed .stat-icon {
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
}

.stat-slots .stat-icon {
    background: var(--color-pale-sage);
    color: var(--color-primary);
}

.stat-info {
    display: flex;
    flex-direction: column;
}

.stat-number {
    font-size: 32px;
    font-weight: 700;
    color: var(--color-text-heading);
    line-height: 1;
}

.stat-label {
    font-size: 14px;
    color: var(--color-text-body);
    margin-top: 6px;
}

/* Action Card */
.action-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    padding: 24px;
    margin-bottom: 24px;
}

.action-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.action-header h2 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 20px;
    margin: 0;
    color: var(--color-text-heading);
}

.action-header h2 .material-symbols-outlined {
    color: var(--status-pending-text);
}

.action-card p {
    margin: 0;
    color: var(--color-text-body);
}

/* Workflow Steps */
.workflow-steps {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 32px;
    padding: 20px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
}

.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.step-number {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: var(--color-border);
    color: var(--color-text-body);
    font-weight: 700;
    font-size: 16px;
}

.step.active .step-number {
    background: var(--color-primary);
    color: var(--color-surface);
}

.step.completed .step-number {
    background: var(--status-completed-text);
    color: var(--color-surface);
}

.step-label {
    font-size: 13px;
    color: var(--color-text-body);
    font-weight: 500;
}

.step.active .step-label {
    color: var(--color-primary);
    font-weight: 700;
}

.step-line {
    flex: 1;
    height: 2px;
    background: var(--color-border);
    max-width: 80px;
}

.step-line.completed {
    background: var(--status-completed-text);
}

/* Table Container */
.table-container {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    overflow: hidden;
    box-shadow: var(--shadow-soft);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    padding: 16px 20px;
    text-align: left;
    background: var(--color-bg);
    color: var(--color-text-heading);
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 2px solid var(--color-border);
}

.data-table td {
    padding: 16px 20px;
    border-bottom: 1px solid var(--color-border);
    vertical-align: middle;
    color: var(--color-text-heading);
    font-size: 15px;
}

.data-table tbody tr:hover {
    background: var(--color-pale-sage);
}

.data-table tbody tr:last-child td {
    border-bottom: none;
}

/* Patient Info */
.patient-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.patient-name {
    font-weight: 600;
    color: var(--color-text-heading);
}

.appointment-id {
    font-size: 13px;
    color: var(--color-text-body);
    font-family: ui-monospace, monospace;
}

/* Contact Info */
.contact-info {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: var(--color-text-body);
}

.contact-info .material-symbols-outlined {
    font-size: 16px;
}

/* DateTime Info */
.datetime-info {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: var(--color-text-body);
}

.datetime-info .material-symbols-outlined {
    font-size: 16px;
}

/* Action Buttons */
.action-buttons {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.btn-approve {
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
    border-color: var(--status-completed-text);
}

.btn-approve:hover {
    background: #d1e7dd;
}

.btn-reject {
    background: var(--status-cancelled-bg);
    color: var(--status-cancelled-text);
    border-color: var(--status-cancelled-text);
}

.btn-reject:hover {
    background: #f8d7da;
}

.btn-complete {
    background: var(--color-primary);
    color: var(--color-surface);
    border-color: var(--color-primary);
}

.btn-complete:hover {
    background: var(--color-primary-hover);
}

.btn-icon {
    min-height: 36px;
    min-width: 36px;
    padding: 8px;
    display: grid;
    place-items: center;
}

.btn-icon .material-symbols-outlined {
    font-size: 18px;
    margin: 0;
}

/* Management Grid */
.management-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    margin-bottom: 32px;
}

.management-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    padding: 24px;
    box-shadow: var(--shadow-soft);
}

.management-card h3 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 18px;
    margin-bottom: 12px;
    color: var(--color-text-heading);
}

.management-card h3 .material-symbols-outlined {
    color: var(--color-primary);
}

.management-card p {
    font-size: 14px;
    color: var(--color-text-body);
    margin-bottom: 20px;
}

.management-card .form-group {
    margin-bottom: 16px;
}

/* Slots Table Container */
.slots-table-container {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    padding: 24px;
    box-shadow: var(--shadow-soft);
}

.slots-table-container h3 {
    font-size: 18px;
    margin-bottom: 20px;
    color: var(--color-text-heading);
}

/* Report Card */
.report-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    padding: 24px;
    box-shadow: var(--shadow-soft);
}

.report-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.report-header h2 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 20px;
    margin: 0;
    color: var(--color-text-heading);
}

.report-content {
    padding: 16px;
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-btn);
    font-family: ui-monospace, monospace;
    font-size: 14px;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 48px 24px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
}

.empty-icon {
    font-size: 48px;
    color: var(--color-pale-sage);
    margin-bottom: 16px;
}

.empty-state h3 {
    font-size: 20px;
    margin-bottom: 8px;
    color: var(--color-text-heading);
}

.empty-state p {
    font-size: 15px;
    color: var(--color-text-body);
    margin: 0;
}

/* Modal Styles */
.modal-close-btn .material-symbols-outlined {
    font-size: 24px;
    margin: 0;
}

.modal-header h2 {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 20px;
    margin: 0;
    color: var(--color-text-heading);
}

.modal-header h2 .material-symbols-outlined {
    color: var(--color-primary);
}

/* Responsive */
@media (max-width: 1024px) {
    .staff-layout {
        grid-template-columns: 240px 1fr;
    }

    .staff-main {
        padding: 24px;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .management-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .staff-layout {
        grid-template-columns: 1fr;
    }

    .staff-sidebar {
        position: relative;
        height: auto;
    }

    .sidebar-nav {
        flex-direction: row;
        flex-wrap: wrap;
    }

    .nav-item {
        flex: 1;
        min-width: 140px;
    }

    .workflow-steps {
        flex-direction: column;
    }

    .step-line {
        width: 2px;
        height: 20px;
        max-width: none;
    }

    .action-buttons {
        flex-direction: column;
    }

    .btn {
        width: 100%;
    }
}

.section-header {
    margin-bottom: 20px;
}

.section-header > div {
    width: 100%;
}

.stats-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.stat-card,
.management-card,
.slots-table-container,
.report-card,
.action-card,
.dashboard-card {
    padding: 24px;
}

.stat-card {
    min-width: 0;
}

.stat-completed .stat-icon {
    background: var(--status-completed-bg);
    color: var(--status-completed-text);
}

.stat-trend {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    margin-top: 7px;
    color: var(--color-text-body);
    font-size: 12px;
}

.stat-trend--up {
    color: var(--status-cancelled-text);
}

.stat-trend--down {
    color: var(--status-completed-text);
}

.stat-trend .material-symbols-outlined {
    font-size: 16px;
}

.charts-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
    margin-bottom: 24px;
}

.dashboard-card {
    min-width: 0;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-card);
    background: var(--color-surface);
    box-shadow: var(--shadow-soft);
}

.dashboard-card__header {
    margin-bottom: 16px;
}

.dashboard-card__header h2 {
    font-size: 19px;
}

.dashboard-card__header p {
    margin-top: 4px;
    color: var(--color-text-body);
    font-size: 14px;
}

.chart-container {
    position: relative;
    height: 280px;
}

.chart-container--doughnut {
    max-width: 360px;
    height: 280px;
    margin-inline: auto;
}

.workflow-breadcrumb {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}

.workflow-pill {
    min-height: 28px;
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border: 1px solid var(--color-border);
    border-radius: 999px;
    background: var(--color-surface);
    color: var(--color-text-body);
    font-size: 12px;
    line-height: 1;
}

.workflow-pill.is-current {
    border-color: var(--color-primary);
    background: var(--color-primary);
    color: var(--color-surface);
    font-weight: 700;
}

.workflow-arrow {
    color: #68756B;
    font-size: 14px;
}

.data-table {
    table-layout: fixed;
    min-width: 920px;
}

.table-container {
    overflow-x: auto;
}

.data-table .column-patient { width: 16%; }
.data-table .column-contact { width: 23%; }
.data-table .column-datetime { width: 16%; }
.data-table .column-purpose { width: 18%; }
.data-table .column-status { width: 11%; }
.data-table .column-actions { width: 16%; }
.data-table .column-slot-date { width: 30%; }
.data-table .column-slot-time { width: 25%; }
.data-table .column-slot-status { width: 22%; }
.data-table .column-slot-actions { width: 23%; }

.data-table th,
.data-table td {
    overflow-wrap: anywhere;
}

.slots-table-heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 20px;
}

.slots-table-heading h3 {
    margin-bottom: 4px;
}

.slots-table-heading p {
    color: var(--color-text-body);
    font-size: 14px;
}

.slot-filters {
    display: flex;
    align-items: flex-end;
    gap: 12px;
}

.slot-filters .form-group {
    width: 160px;
    margin-bottom: 0;
}

.slot-filters .form-label {
    font-size: 13px;
}

.slot-filters .form-input {
    min-height: 44px;
    font-size: 14px;
}

.slot-filters .btn {
    min-height: 44px;
}

.slots-table-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-top: 16px;
}

.slot-results-count {
    color: var(--color-text-body);
    font-size: 14px;
}

.slot-filter-empty {
    padding: 18px;
    color: var(--color-text-body);
    text-align: center;
}

.slot-filter-empty[hidden],
#show-more-slots[hidden] {
    display: none;
}

.management-card,
.slots-table-container,
.report-card,
.action-card {
    margin-bottom: 24px;
}

@media (max-width: 1100px) {
    .stats-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .management-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 768px) {
    .staff-main {
        min-width: 0;
        padding: 20px 16px;
    }

    .charts-grid {
        grid-template-columns: 1fr;
    }

    .section-header {
        margin-bottom: 20px;
    }

    .workflow-breadcrumb {
        gap: 5px;
    }

    .workflow-pill {
        padding-inline: 8px;
        font-size: 11px;
    }

    .slots-table-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .slot-filters {
        width: 100%;
        flex-wrap: wrap;
    }

    .slot-filters .form-group {
        flex: 1;
        min-width: 130px;
    }

    .action-buttons {
        flex-direction: row;
    }

    .action-buttons .btn {
        width: auto;
    }
}

@media (max-width: 560px) {
    .stats-grid,
    .management-grid {
        grid-template-columns: 1fr;
    }

    .stat-card,
    .management-card,
    .slots-table-container,
    .report-card,
    .action-card,
    .dashboard-card {
        padding: 18px;
    }

    .chart-container {
        height: 250px;
    }

    .chart-container--doughnut {
        height: 240px;
    }

    .slots-table-footer,
    .report-header {
        align-items: stretch;
        flex-direction: column;
    }

    .slots-table-footer .btn,
    .report-header .btn {
        width: 100%;
    }
}

.slots-calendar {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 10px;
}

.calendar-day {
    min-width: 0;
    min-height: 190px;
    padding: 12px;
    border: 1px solid var(--color-border);
    border-radius: 12px;
    background: #fff;
}

.calendar-day[hidden] {
    display: none;
}

.calendar-day--today {
    border: 2px solid var(--color-primary);
    background: #f4f8f3;
}

.calendar-day__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 6px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--color-border);
}

.calendar-day__header > div {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.calendar-day__weekday {
    color: var(--color-text-body);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

.calendar-day__date {
    color: var(--color-text-heading);
    font-size: 21px;
    font-weight: 750;
    line-height: 1.1;
}

.calendar-day__date small {
    font-size: 13px;
    font-weight: 600;
}

.calendar-day__count {
    padding: 4px 7px;
    border: 1px solid #b6d5c2;
    border-radius: 999px;
    background: #edf7ef;
    color: #28623c;
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
}

.calendar-day__count--empty {
    border-color: var(--color-border);
    background: #f5f6f3;
    color: var(--color-text-body);
}

.calendar-day__slots {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 218px;
    overflow-y: auto;
    padding-top: 9px;
}

.calendar-slot {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    min-width: 0;
    padding: 6px;
    border: 1px solid var(--color-border);
    border-left-width: 3px;
    border-radius: 7px;
    background: #f8faf7;
}

.calendar-slot--available {
    border-left-color: #3b8052;
}

.calendar-slot--booked {
    border-color: #c5d5ea;
    border-left-color: #4f78b8;
    background: #f1f6fc;
}

.calendar-slot--disabled {
    border-left-color: #a0a8a0;
    background: #f2f3f1;
}

.calendar-slot__info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
}

.calendar-slot__time {
    color: var(--color-text-heading);
    font-size: 13px;
    font-weight: 700;
}

.calendar-slot__status {
    color: var(--color-text-body);
    font-size: 11px;
}

.calendar-slot__actions {
    display: flex;
    flex-shrink: 0;
    gap: 3px;
}

.calendar-slot__actions .btn-icon {
    width: 30px;
    height: 30px;
    min-height: 30px;
    padding: 4px;
}

.calendar-slot__actions .material-symbols-outlined {
    font-size: 17px;
}

.calendar-day__empty {
    margin: auto 0;
    padding-top: 18px;
    color: #69756c;
    font-size: 12px;
    text-align: center;
}

@media (max-width: 1600px) {
    .slots-calendar {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
}

@media (max-width: 768px) {
    .slots-calendar {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .calendar-day {
        min-height: 170px;
    }
}

@media (max-width: 560px) {
    .slots-calendar {
        grid-template-columns: 1fr;
    }

    .calendar-day {
        min-height: 0;
    }

    .calendar-day__slots {
        max-height: 260px;
    }
}
``

---

## File: $relativePath

``javascript
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

``

---

## File: $relativePath

``javascript
(() => {
    const signInForm = document.getElementById("sign-in-form");
    const createAccountForm = document.getElementById("create-account-form");
    const authPage = document.querySelector(".auth-page");
    const signInTab = document.getElementById("sign-in-tab");
    const createAccountTab = document.getElementById("create-account-tab");
    const signInPanel = document.getElementById("sign-in-panel");
    const createAccountPanel = document.getElementById("create-account-panel");

    function setFeedback(id, message, success = false) {
        const feedback = document.getElementById(id);
        if (!feedback) return;
        feedback.textContent = message;
        feedback.classList.toggle("alert-success", success);
        feedback.classList.toggle("alert-error", !success);
        feedback.setAttribute("role", success ? "status" : "alert");
        feedback.hidden = false;
    }

    function clearFeedback(id) {
        const feedback = document.getElementById(id);
        if (!feedback) return;
        feedback.textContent = "";
        feedback.classList.remove("alert-success");
        feedback.classList.add("alert-error");
        feedback.setAttribute("role", "alert");
        feedback.hidden = true;
    }

    if (authPage && signInTab && createAccountTab && signInPanel && createAccountPanel) {
        const tabs = [
            { button: signInTab, panel: signInPanel },
            { button: createAccountTab, panel: createAccountPanel }
        ];

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

        tabs.forEach((tab, index) => {
            tab.button.addEventListener("click", () => activateTab(index));
            tab.button.addEventListener("keydown", (event) => {
                if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
                event.preventDefault();
                const nextIndex = (index + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
                activateTab(nextIndex, true);
            });
        });
    }

    const slotInput = document.getElementById("initial-slot-id");
    const calendar = document.getElementById("availability-calendar");
    const calendarFeedback = document.getElementById("calendar-feedback");
    let setCalendarFeedback = () => {};

    if (slotInput && calendar) {
        const availableTimes = document.getElementById("available-times-list");
        const calendarInstructions = document.getElementById("calendar-instructions");
        const monthLabel = document.getElementById("calendar-month");
        const previousMonthButton = document.getElementById("calendar-previous");
        const nextMonthButton = document.getElementById("calendar-next");

        slotInput.name = "slot_id";

        const slotsByDate = new Map();
        document.querySelectorAll("[data-slot-option]").forEach((option) => {
            const slotDate = option.dataset.slotDate;
            if (!slotDate) return;
            if (!slotsByDate.has(slotDate)) slotsByDate.set(slotDate, []);
            slotsByDate.get(slotDate).push({
                id: option.dataset.slotId,
                time: option.dataset.slotTime
            });
        });

        const availableDates = [...slotsByDate.keys()].sort();
        const monthKeys = [...new Set(availableDates.map((date) => date.slice(0, 7)))];

        function monthKeyFromDate(date) {
            return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
        }

        function monthDate(monthKey) {
            const [year, month] = monthKey.split("-").map(Number);
            return new Date(year, month - 1, 1, 12);
        }

        function parseLocalDate(isoDate) {
            const [year, month, day] = isoDate.split("-").map(Number);
            return new Date(year, month - 1, day, 12);
        }

        let displayedMonth = monthKeys[0] || monthKeyFromDate(new Date());
        let selectedDate = null;
        let selectedSlotId = slotInput.value;

        setCalendarFeedback = (message) => {
            if (!calendarFeedback) return;
            calendarFeedback.textContent = message;
            calendarFeedback.hidden = !message;
            if (message) {
                calendar.setAttribute("aria-invalid", "true");
            } else {
                calendar.removeAttribute("aria-invalid");
            }
        };

        function renderAvailableTimes() {
            if (!availableTimes || !calendarInstructions) return;
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

        function renderCalendar() {
            const currentMonth = monthDate(displayedMonth);
            const year = currentMonth.getFullYear();
            const month = currentMonth.getMonth();
            if (monthLabel) {
                monthLabel.textContent = currentMonth.toLocaleDateString(undefined, {
                    month: "long",
                    year: "numeric"
                });
            }
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
                    button.addEventListener("click", () => {
                        selectedDate = isoDate;
                        selectedSlotId = "";
                        slotInput.value = "";
                        setCalendarFeedback("");
                        renderCalendar();
                        renderAvailableTimes();
                    });
                }
                calendar.append(button);
            }
        }

        previousMonthButton?.addEventListener("click", () => {
            const date = monthDate(displayedMonth);
            date.setMonth(date.getMonth() - 1);
            displayedMonth = monthKeyFromDate(date);
            renderCalendar();
        });

        nextMonthButton?.addEventListener("click", () => {
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
    }

    if (signInForm) {
        signInForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            clearFeedback("sign-in-feedback");
            const submitButton = signInForm.querySelector('[type="submit"]');
            if (submitButton) submitButton.disabled = true;

            try {
                await window.ClinicEase.request(signInForm.dataset.apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(Object.fromEntries(new FormData(signInForm)))
                });
                window.location.assign(signInForm.dataset.dashboardUrl);
            } catch (error) {
                setFeedback("sign-in-feedback", error.message);
                if (submitButton) submitButton.disabled = false;
            }
        });
    }

    if (createAccountForm) {
        createAccountForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            if (slotInput && !slotInput.value) {
                setCalendarFeedback("Choose an available date and time before continuing.");
                calendar?.focus();
                return;
            }
            if (!window.confirm(createAccountForm.dataset.confirmMessage)) return;

            clearFeedback("create-account-feedback");
            const submitButton = createAccountForm.querySelector('[type="submit"]');
            if (submitButton) submitButton.disabled = true;

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
                setFeedback("create-account-feedback", error.message);
                if (submitButton) submitButton.disabled = false;
            }
        });
    }
})();

``

---

## File: $relativePath

``javascript
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

``

---

## File: $relativePath

``javascript
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

``

---

## File: $relativePath

``javascript
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

``

---

## File: $relativePath

``html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#FAF8F1">
    <title>{% block title %}ClinicEase{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
    {% block page_css %}{% endblock %}
</head>
<body>
    <header class="header">
        <div class="container header-content">
            <a class="brand" href="{{ url_for('home') }}" aria-label="ClinicEase home">
                <span class="brand-icon" aria-hidden="true">CE</span>
                <span class="brand-title">ClinicEase</span>
            </a>

            <nav class="nav-actions" aria-label="Account navigation">
                {% if session.get('role') %}
                    <span class="nav-user">{{ session.get('name', 'Account') }}</span>
                    <a class="btn btn-secondary btn-sm" href="{{ url_for('logout') }}">Log Out</a>
                {% else %}
                    <a class="btn btn-secondary btn-sm" href="{{ url_for('login_page') }}">Sign In</a>
                    <a class="btn btn-primary btn-sm" href="{{ url_for('register_page') }}">Create Account</a>
                {% endif %}
            </nav>
        </div>
    </header>

    <main class="main-content">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="container" aria-live="polite">
                    {% for category, message in messages %}
                        <div class="alert {% if category in ['error', 'danger'] %}alert-error{% else %}alert-success{% endif %}"
                             role="{% if category in ['error', 'danger'] %}alert{% else %}status{% endif %}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="container footer-content">
            <span><strong>ClinicEase</strong> · Appointment care made easier.</span>
            <span>&copy; 2026 ClinicEase</span>
        </div>
    </footer>

    <div id="app-toast" class="toast" role="status" aria-live="polite" aria-atomic="true" hidden></div>
    <script src="{{ url_for('static', filename='js/base.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>

``

---

## File: $relativePath

``html
{% extends "base.html" %}
{% block title %}Staff Dashboard - ClinicEase{% endblock %}
{% block page_css %}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/staff-dashboard.css') }}">
{% endblock %}
{% block content %}
<div class="staff-layout">
    <!-- Left Sidebar Navigation -->
    <aside class="staff-sidebar">
        <div class="sidebar-header">
            <div class="brand">
                <span class="brand-icon">CE</span>
                <span class="brand-title">ClinicEase</span>
            </div>
            <p class="user-info">{{ user.name }}</p>
        </div>

        <nav class="sidebar-nav">
            <button class="nav-item active" data-section="dashboard" type="button">
                <span class="material-symbols-outlined">dashboard</span>
                <span>Dashboard</span>
            </button>
            <button class="nav-item" data-section="pending" type="button">
                <span class="material-symbols-outlined">schedule</span>
                <span>Pending Requests</span>
                {% if pending_appointments|length > 0 %}
                <span class="badge-count">{{ pending_appointments|length }}</span>
                {% endif %}
            </button>
            <button class="nav-item" data-section="confirmed" type="button">
                <span class="material-symbols-outlined">event_available</span>
                <span>Confirmed</span>
                {% if confirmed_appointments|length > 0 %}
                <span class="badge-count">{{ confirmed_appointments|length }}</span>
                {% endif %}
            </button>
            <button class="nav-item" data-section="slots" type="button">
                <span class="material-symbols-outlined">calendar_month</span>
                <span>Appointment Times</span>
            </button>
            <button class="nav-item" data-section="reports" type="button">
                <span class="material-symbols-outlined">assessment</span>
                <span>Reports</span>
            </button>
        </nav>

        <div class="sidebar-footer">
            <a href="{{ url_for('logout') }}" class="btn btn-secondary btn-sm">
                <span class="material-symbols-outlined">logout</span>
                Log Out
            </a>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="staff-main">
        <!-- Dashboard Overview -->
        <section id="dashboard-section" class="content-section active"
                 data-stats-url="{{ url_for('get_staff_dashboard_stats') }}">
            <header class="section-header">
                <div>
                    <h1>Dashboard Overview</h1>
                    <p>Welcome back, {{ user.name }}. Here's what needs your attention.</p>
                </div>
            </header>

            <div class="stats-grid">
                <div class="stat-card stat-pending">
                    <div class="stat-icon">
                        <span class="material-symbols-outlined">schedule</span>
                    </div>
                    <div class="stat-info">
                        <span id="stat-pending-count" class="stat-number">{{ pending_appointments|length }}</span>
                        <span class="stat-label">Pending Requests</span>
                        <span id="pending-trend" class="stat-trend" aria-live="polite">Loading trend…</span>
                    </div>
                </div>
                <div class="stat-card stat-confirmed">
                    <div class="stat-icon">
                        <span class="material-symbols-outlined">event_available</span>
                    </div>
                    <div class="stat-info">
                        <span id="stat-confirmed-count" class="stat-number">—</span>
                        <span class="stat-label">Confirmed This Week</span>
                    </div>
                </div>
                <div class="stat-card stat-completed">
                    <div class="stat-icon">
                        <span class="material-symbols-outlined">task_alt</span>
                    </div>
                    <div class="stat-info">
                        <span id="stat-completed-count" class="stat-number">—</span>
                        <span class="stat-label">Completed This Month</span>
                    </div>
                </div>
                <div class="stat-card stat-slots">
                    <div class="stat-icon">
                        <span class="material-symbols-outlined">calendar_month</span>
                    </div>
                    <div class="stat-info">
                        <span id="stat-available-slots" class="stat-number">—</span>
                        <span class="stat-label">Available Slots · 7 Days</span>
                    </div>
                </div>
            </div>

            <div class="charts-grid">
                <article class="dashboard-card chart-card">
                    <header class="dashboard-card__header">
                        <div>
                            <h2>Appointment Status</h2>
                            <p>All appointments by current status</p>
                        </div>
                    </header>
                    <div class="chart-container chart-container--doughnut">
                        <canvas id="appointment-status-chart" aria-label="Appointments by status chart" role="img"></canvas>
                    </div>
                </article>
                <article class="dashboard-card chart-card">
                    <header class="dashboard-card__header">
                        <div>
                            <h2>Bookings This Week</h2>
                            <p>Daily appointments for the next seven days</p>
                        </div>
                    </header>
                    <div class="chart-container">
                        <canvas id="weekly-bookings-chart" aria-label="Bookings per day for the next seven days" role="img"></canvas>
                    </div>
                </article>
            </div>

            {% if pending_appointments %}
            <div class="action-card">
                <div class="action-header">
                    <h2><span class="material-symbols-outlined">schedule</span> Pending Requests</h2>
                    <button class="btn btn-primary" data-nav="pending">Review Now</button>
                </div>
                <p>{{ pending_appointments|length }} appointment{{ 's' if pending_appointments|length != 1 }} waiting for your approval.</p>
            </div>
            {% endif %}
        </section>

        <!-- Pending Requests Section -->
        <section id="pending-section" class="content-section">
            <header class="section-header">
                <div>
                    <h1>Pending Requests</h1>
                    <p>Review and approve or reject new appointment requests.</p>
                    <nav class="workflow-breadcrumb" aria-label="Appointment workflow">
                        <span class="workflow-pill is-current">Review</span>
                        <span class="workflow-arrow" aria-hidden="true">→</span>
                        <span class="workflow-pill">Approve / Reject</span>
                        <span class="workflow-arrow" aria-hidden="true">→</span>
                        <span class="workflow-pill">Complete</span>
                    </nav>
                </div>
            </header>

            {% if pending_appointments %}
            <div class="table-container">
                <table class="data-table">
                <colgroup>
                    <col class="column-patient">
                    <col class="column-contact">
                    <col class="column-datetime">
                    <col class="column-purpose">
                    <col class="column-status">
                    <col class="column-actions">
                </colgroup>
                    <thead>
                    <tr>
                        <th>Patient</th>
                            <th>Contact</th>
                            <th>Date & Time</th>
                            <th>Purpose</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for appt in pending_appointments %}
                        <tr>
                            <td>
                                <div class="patient-info">
                                    <span class="patient-name">{{ appt.patient_name }}</span>
                                    <span class="appointment-id">#{{ appt.appointment_id }}</span>
                                </div>
                            </td>
                            <td>
                                <div class="contact-info">
                                    <span class="material-symbols-outlined">email</span>
                                    {{ appt.email }}
                                </div>
                                {% if appt.contact_number %}
                                <div class="contact-info">
                                    <span class="material-symbols-outlined">phone</span>
                                    {{ appt.contact_number }}
                                </div>
                                {% endif %}
                            </td>
                            <td>
                                <div class="datetime-info">
                                    <span class="material-symbols-outlined">calendar_today</span>
                                    {{ appt.slot_date }}
                                </div>
                                <div class="datetime-info">
                                    <span class="material-symbols-outlined">schedule</span>
                                    {{ appt.time }}
                                </div>
                            </td>
                            <td>{{ appt.purpose }}</td>
                            <td><span class="status-badge status-pending">Pending</span></td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-approve" type="button"
                                            data-appointment-action="confirm"
                                            data-appointment-id="{{ appt.appointment_id }}"
                                            data-endpoint="{{ url_for('staff_appointment_action', appt_id=appt.appointment_id) }}">
                                        <span class="material-symbols-outlined">check_circle</span>
                                        Approve
                                    </button>
                                    <button class="btn btn-reject" type="button"
                                            data-appointment-action="cancel"
                                            data-appointment-id="{{ appt.appointment_id }}"
                                            data-endpoint="{{ url_for('staff_appointment_action', appt_id=appt.appointment_id) }}">
                                        <span class="material-symbols-outlined">cancel</span>
                                        Reject
                                    </button>
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state">
                <span class="material-symbols-outlined empty-icon">check_circle</span>
                <h3>All caught up!</h3>
                <p>No pending appointment requests at this time.</p>
            </div>
            {% endif %}
        </section>

        <!-- Confirmed Appointments Section -->
        <section id="confirmed-section" class="content-section">
            <header class="section-header">
                <div>
                    <h1>Confirmed Appointments</h1>
                    <p>Mark visits as completed after the patient has been seen.</p>
                </div>
            </header>

            {% if confirmed_appointments %}
            <div class="table-container">
                <table class="data-table">
                        <colgroup>
                            <col class="column-patient">
                            <col class="column-contact">
                            <col class="column-datetime">
                            <col class="column-purpose">
                            <col class="column-status">
                            <col class="column-actions">
                        </colgroup>
                        <thead>
                        <tr>
                            <th>Patient</th>
                            <th>Contact</th>
                            <th>Date & Time</th>
                            <th>Purpose</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for appt in confirmed_appointments %}
                        <tr>
                            <td>
                                <div class="patient-info">
                                    <span class="patient-name">{{ appt.patient_name }}</span>
                                    <span class="appointment-id">#{{ appt.appointment_id }}</span>
                                </div>
                            </td>
                            <td>
                                <div class="contact-info">
                                    <span class="material-symbols-outlined">email</span>
                                    {{ appt.email }}
                                </div>
                                {% if appt.contact_number %}
                                <div class="contact-info">
                                    <span class="material-symbols-outlined">phone</span>
                                    {{ appt.contact_number }}
                                </div>
                                {% endif %}
                            </td>
                            <td>
                                <div class="datetime-info">
                                    <span class="material-symbols-outlined">calendar_today</span>
                                    {{ appt.slot_date }}
                                </div>
                                <div class="datetime-info">
                                    <span class="material-symbols-outlined">schedule</span>
                                    {{ appt.time }}
                                </div>
                            </td>
                            <td>{{ appt.purpose }}</td>
                            <td>
                                <span class="status-badge status-confirmed">Confirmed</span>
                            </td>
                            <td>
                                <button class="btn btn-complete" type="button"
                                        data-appointment-action="complete"
                                        data-appointment-id="{{ appt.appointment_id }}"
                                        data-endpoint="{{ url_for('staff_appointment_action', appt_id=appt.appointment_id) }}">
                                    <span class="material-symbols-outlined">task_alt</span>
                                    Mark Completed
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% else %}
            <div class="empty-state">
                <span class="material-symbols-outlined empty-icon">event_busy</span>
                <h3>No confirmed appointments</h3>
                <p>Confirmed appointments will appear here.</p>
            </div>
            {% endif %}
        </section>

        <!-- Appointment Times Section -->
        <section id="slots-section" class="content-section">
            <header class="section-header">
                <div>
                    <h1>Manage Appointment Times</h1>
                    <p>Generate slots, block dates, or manage existing times.</p>
                </div>
            </header>

            <div class="management-grid">
                <!-- Generate Slots Card -->
                <div class="management-card">
                    <h3><span class="material-symbols-outlined">add_circle</span> Generate Monthly Slots</h3>
                    <p>Create available appointment times for the selected month.</p>
                    <form id="generate-slots-form" action="{{ url_for('generate_monthly_slots') }}">
                        <div class="form-group">
                            <label class="form-label" for="slot-month">Select Month</label>
                            <input class="form-input" id="slot-month" name="month" type="month"
                                   value="{{ today.strftime('%Y-%m') }}"
                                   min="{{ today.strftime('%Y-%m') }}" required>
                        </div>
                        <button class="btn btn-primary btn-block" type="submit">
                            Generate Slots
                        </button>
                    </form>
                </div>

                <!-- Block Date Card -->
                <div class="management-card">
                    <h3><span class="material-symbols-outlined">block</span> Block a Date</h3>
                    <p>Mark a date as closed (holiday, vacation, etc.).</p>
                    <form id="blocked-date-form" action="{{ url_for('create_blocked_date') }}">
                        <div class="form-group">
                            <label class="form-label" for="blocked-date">Date</label>
                            <input class="form-input" id="blocked-date" name="blocked_date" type="date"
                                   min="{{ today.isoformat() }}" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="blocked-date-reason">Reason</label>
                            <input class="form-input" id="blocked-date-reason" name="reason" type="text"
                                   placeholder="e.g., Christmas Day" maxlength="255" required>
                        </div>
                        <button class="btn btn-secondary btn-block" type="submit">
                            <span class="material-symbols-outlined">block</span>
                            Block Date
                        </button>
                    </form>
                </div>
            </div>

            <!-- Appointment Times Calendar -->
            <div class="slots-table-container">
                <div class="slots-table-heading">
                    <div>
                        <h3>Appointment Times Calendar</h3>
                        <p>Review availability from today through 14 days ahead.</p>
                    </div>
                    <div class="slot-filters" role="group" aria-label="Filter appointment times by date">
                        <div class="form-group">
                            <label class="form-label" for="slot-from-date">From</label>
                            <input class="form-input" id="slot-from-date" type="date"
                                   min="{{ today.isoformat() }}" aria-label="Filter from date">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="slot-to-date">To</label>
                            <input class="form-input" id="slot-to-date" type="date"
                                   min="{{ today.isoformat() }}" aria-label="Filter to date">
                        </div>
                        <button id="clear-slot-filters" class="btn btn-secondary" type="button">Clear</button>
                    </div>
                </div>
                <div class="slots-calendar" aria-label="Appointment times by date">
                    {% for day in calendar_days %}
                    {% set day_slots = slots|selectattr('slot_date_input', 'equalto', day.isoformat())|list %}
                    {% set open_count = day_slots|selectattr('status', 'equalto', 'Available')|list|length %}
                    <article class="calendar-day{% if day == today %} calendar-day--today{% endif %}"
                             data-calendar-day data-slot-date="{{ day.isoformat() }}"
                             data-day-index="{{ loop.index0 }}">
                        <header class="calendar-day__header">
                            <div>
                                <span class="calendar-day__weekday">{{ day.strftime('%a') }}</span>
                                <span class="calendar-day__date">
                                    {{ day.day }} <small>{{ day.strftime('%b') }}</small>
                                </span>
                            </div>
                            <span class="calendar-day__count{% if open_count == 0 %} calendar-day__count--empty{% endif %}">
                                {{ open_count }} open
                            </span>
                        </header>
                        <div class="calendar-day__slots">
                            {% for slot in day_slots %}
                            <div class="calendar-slot{% if slot.status == 'Available' %} calendar-slot--available{% elif slot.status == 'Booked' %} calendar-slot--booked{% else %} calendar-slot--disabled{% endif %}">
                                <div class="calendar-slot__info">
                                    <span class="calendar-slot__time">{{ slot.time }}</span>
                                    <span class="calendar-slot__status">{{ slot.status }}</span>
                                </div>
                                {% if slot.status in ['Available', 'Unavailable', 'Disabled'] %}
                                <div class="calendar-slot__actions">
                                    {% if not slot.has_appointments %}
                                    <button class="btn btn-secondary btn-icon" type="button"
                                            data-edit-slot
                                            data-slot-id="{{ slot.slot_id }}"
                                            data-slot-date="{{ slot.slot_date_input }}"
                                            data-slot-time="{{ slot.time_input }}"
                                            data-endpoint="{{ url_for('manage_staff_slot', slot_id=slot.slot_id) }}"
                                            aria-label="Edit {{ slot.time }} on {{ day.strftime('%b %d') }}"
                                            title="Edit">
                                        <span class="material-symbols-outlined">edit</span>
                                    </button>
                                    {% endif %}
                                    {% if slot.status == 'Available' %}
                                    <button class="btn btn-secondary btn-icon" type="button"
                                            data-slot-action="disable" data-slot-id="{{ slot.slot_id }}"
                                            data-endpoint="{{ url_for('manage_staff_slot', slot_id=slot.slot_id) }}"
                                            aria-label="Disable {{ slot.time }} on {{ day.strftime('%b %d') }}"
                                            title="Disable">
                                        <span class="material-symbols-outlined">block</span>
                                    </button>
                                    {% else %}
                                    <button class="btn btn-secondary btn-icon" type="button"
                                            data-slot-action="enable" data-slot-id="{{ slot.slot_id }}"
                                            data-endpoint="{{ url_for('manage_staff_slot', slot_id=slot.slot_id) }}"
                                            aria-label="Enable {{ slot.time }} on {{ day.strftime('%b %d') }}"
                                            title="Enable">
                                        <span class="material-symbols-outlined">check_circle</span>
                                    </button>
                                    {% endif %}
                                    {% if not slot.has_appointments %}
                                    <button class="btn btn-danger btn-icon" type="button"
                                            data-slot-action="delete" data-slot-id="{{ slot.slot_id }}"
                                            data-endpoint="{{ url_for('manage_staff_slot', slot_id=slot.slot_id) }}"
                                            aria-label="Delete {{ slot.time }} on {{ day.strftime('%b %d') }}"
                                            title="Delete">
                                        <span class="material-symbols-outlined">delete</span>
                                    </button>
                                    {% endif %}
                                </div>
                                {% endif %}
                            </div>
                            {% else %}
                            <p class="calendar-day__empty">No times scheduled</p>
                            {% endfor %}
                        </div>
                    </article>
                    {% endfor %}
                </div>
                <p id="slot-filter-empty" class="slot-filter-empty" role="status" hidden>
                    No appointment times match these dates.
                </p>
                <div class="slots-table-footer">
                    <p id="slot-results-count" class="slot-results-count" aria-live="polite"></p>
                    <button id="show-more-slots" class="btn btn-secondary" type="button" hidden>
                        Show more dates
                    </button>
                </div>
            </div>
        </section>

        <!-- Reports Section -->
        <section id="reports-section" class="content-section">
            <header class="section-header">
                <div>
                    <h1>Appointment Reports</h1>
                    <p>Generate and view appointment summaries.</p>
                </div>
            </header>

            <div class="report-card">
                <div class="report-header">
                    <h2><span class="material-symbols-outlined">description</span> Appointment Summary Report</h2>
                    <button class="btn btn-primary" id="generate-report-btn" type="button"
                            data-endpoint="{{ url_for('get_staff_appointment_report') }}">
                        <span class="material-symbols-outlined">generate</span>
                        Generate Report
                    </button>
                </div>
                <pre id="report-content" class="report-content hidden"></pre>
            </div>
        </section>
    </main>
</div>

<!-- Edit Slot Modal -->
<div id="edit-slot-modal" class="modal-backdrop hidden" aria-hidden="true">
    <section class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="edit-slot-title">
        <button class="modal-close-btn" type="button" aria-label="Close" data-close-edit-slot>
            <span class="material-symbols-outlined">close</span>
        </button>
        <header class="modal-header">
            <h2 id="edit-slot-title">
                <span class="material-symbols-outlined">edit_calendar</span>
                Edit Appointment Time
            </h2>
        </header>
        <form class="modal-body" id="edit-slot-form" method="post">
            <div class="form-group">
                <label class="form-label" for="edit-slot-date">Date</label>
                <input class="form-input" id="edit-slot-date" name="slot_date" type="date"
                       min="{{ today.isoformat() }}" required>
            </div>
            <div class="form-group">
                <label class="form-label" for="edit-slot-time">Time</label>
                <input class="form-input" id="edit-slot-time" name="time" type="time" required>
            </div>
            <button class="btn btn-primary btn-block" type="submit">
                <span class="material-symbols-outlined">save</span>
                Save Changes
            </button>
        </form>
    </section>
</div>
{% endblock %}
{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{{ url_for('static', filename='js/staff-dashboard.js') }}"></script>
{% endblock %}
``

---

## File: $relativePath

``html
{% extends "base.html" %}

{% block title %}API Test Panel - ClinicEase{% endblock %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/api-test.css') }}">
{% endblock %}

{% block content %}
<div class="container test-panel">
    <header class="test-heading">
        <div>
            <h1>ClinicEase API Test Panel</h1>
            <p>Developer utility for checking the signed-in session and appointment endpoints.</p>
        </div>
        <a href="{{ url_for('home') }}" class="btn btn-secondary">Back to home</a>
    </header>

    <section class="card test-section" aria-labelledby="test-login-title">
        <h2 id="test-login-title">Sign in test</h2>
        <form id="test-login-form" data-endpoint="{{ url_for('api_login') }}">
            <div class="form-group">
                <label class="form-label" for="test-email">Email address</label>
                <input class="form-input" id="test-email" name="email" type="email" required>
            </div>
            <div class="form-group">
                <label class="form-label" for="test-password">Password</label>
                <input class="form-input" id="test-password" name="password" type="password" required>
            </div>
            <button class="btn btn-primary" type="submit">Test Sign In</button>
        </form>
        <pre id="login-response" class="test-response" aria-live="polite">Response will appear here.</pre>
        <p>Active role: <strong id="active-role">Not signed in</strong></p>
    </section>

    <section class="card test-section" aria-labelledby="test-slots-title">
        <h2 id="test-slots-title">Available time test</h2>
        <button class="btn btn-secondary" id="load-slots"
                data-endpoint="{{ url_for('get_dashboard_slots') }}" type="button">
            Load appointment times
        </button>
        <pre id="slots-response" class="test-response" aria-live="polite">Response will appear here.</pre>
        <div class="table-responsive">
            <table class="data-table">
                <caption class="visually-hidden">Appointment slot data returned by the API</caption>
                <thead>
                    <tr>
                        <th scope="col">Slot</th>
                        <th scope="col">Date</th>
                        <th scope="col">Time</th>
                        <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody id="slots-table-body">
                    <tr><td colspan="4">Load appointment times to view results.</td></tr>
                </tbody>
            </table>
        </div>
    </section>

    <section class="card test-section" aria-labelledby="test-booking-title">
        <h2 id="test-booking-title">Appointment request test</h2>
        <form id="test-booking-form" data-endpoint="{{ url_for('book_appointment_slot') }}">
            <div class="form-group">
                <label class="form-label" for="test-slot-id">Available slot ID</label>
                <input class="form-input" id="test-slot-id" name="slot_id" type="number" min="1" required>
            </div>
            <div class="form-group">
                <label class="form-label" for="test-contact-number">Contact number (optional)</label>
                <input class="form-input" id="test-contact-number" name="contact_number" type="tel">
            </div>
            <div class="form-group">
                <label class="form-label" for="test-purpose">Purpose of visit</label>
                <input class="form-input" id="test-purpose" name="purpose" type="text" maxlength="255" required>
            </div>
            <button class="btn btn-primary" type="submit">Submit Test Request</button>
        </form>
        <pre id="booking-response" class="test-response" aria-live="polite">Response will appear here.</pre>
    </section>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/api-test.js') }}"></script>
{% endblock %}

``

---

## File: $relativePath

``html
{% extends "base.html" %}
{% block title %}ClinicEase - Healthcare Appointment System{% endblock %}
{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/landing.css') }}">
{% endblock %}

{% block content %}
<div class="container">
    <!-- Hero Section -->
    <section class="hero-section">
        <span class="badge-pill">Centralized Clinic Scheduling</span>
        <h1 class="hero-title">Simple, transparent clinic appointments for everyone.</h1>
        <p class="hero-description">
            Choose an available time, request a clinic visit, and follow its status as staff review it.
        </p>
        <div class="hero-actions">
            <a href="{{ url_for('register_page') }}" class="btn btn-primary">Book an Appointment</a>
            <a href="{{ url_for('login_page') }}" class="btn btn-secondary">Sign In</a>
        </div>
    </section>
</div>

<!-- How it Works Section -->
<section class="section-block">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">How ClinicEase Works</h2>
            <p class="section-subtitle">A clear process for patients and clinic staff.</p>
        </div>
        <div class="grid-3">
            <article class="card">
                <div class="step-num">1</div>
                <h3>Browse Available Slots</h3>
                <p>Choose from appointment times made available by clinic staff.</p>
            </article>
            <article class="card">
                <div class="step-num">2</div>
                <h3>Submit Booking Request</h3>
                <p>Tell us the reason for your visit. A contact number is optional.</p>
            </article>
            <article class="card">
                <div class="step-num">3</div>
                <h3>Track Status Updates</h3>
                <p>See when staff confirm your request and when your visit is complete.</p>
            </article>
        </div>
    </div>
</section>

<!-- Status Lifecycle Section -->
<div class="container">
    <section class="status-section">
        <div class="section-header">
            <h2 class="section-title">Appointment Status Lifecycle</h2>
            <p class="section-subtitle">Each status is shown with a label and a distinct color.</p>
        </div>
        <div class="grid-4">
            <article class="card status-card">
                <span class="badge-pending">Pending</span>
                <p>Awaiting staff review</p>
            </article>
            <article class="card status-card">
                <span class="badge-confirmed">Confirmed</span>
                <p>Approved by clinic staff</p>
            </article>
            <article class="card status-card">
                <span class="badge-completed">Completed</span>
                <p>Clinic visit completed</p>
            </article>
            <article class="card status-card">
                <span class="badge-cancelled">Cancelled</span>
                <p>Request was not approved</p>
            </article>
        </div>
    </section>
</div>
{% endblock %}
``

---

## File: $relativePath

``html
{% extends "base.html" %}

{% block title %}Sign In - ClinicEase{% endblock %}

{% block page_css %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/auth.css') }}">
{% endblock %}

{% block content %}
<div class="container auth-page auth-page-login">
    <section class="card auth-card" aria-labelledby="auth-title">
        <header class="auth-heading">
            <h1 id="auth-title">Welcome back to ClinicEase</h1>
            <p>Sign in to manage your appointments.</p>
        </header>

        {% if error %}
            <div class="alert alert-error" role="alert">{{ error }}</div>
        {% endif %}
        {% if message %}
            <div class="alert alert-success" role="status">{{ message }}</div>
        {% endif %}
        <div id="sign-in-feedback" class="alert alert-error" role="alert" hidden></div>

        <form id="sign-in-form" action="{{ url_for('login_page') }}" data-api-url="{{ url_for('api_login') }}"
              data-dashboard-url="{{ url_for('dashboard') }}" method="post">
            <div class="form-group">
                <label class="form-label" for="sign-in-email">Email address</label>
                <input class="form-input" id="sign-in-email" name="email" type="email"
                       autocomplete="email" required>
            </div>
            <div class="form-group">
                <label class="form-label" for="sign-in-password">Password</label>
                <input class="form-input" id="sign-in-password" name="password" type="password"
                       autocomplete="current-password" required>
            </div>
            <button class="btn btn-primary btn-block" type="submit">Sign In</button>
        </form>
        <p class="auth-switch">New to ClinicEase? <a href="{{ url_for('register_page') }}">Create an account</a></p>
    </section>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/auth.js') }}"></script>
{% endblock %}

``

---

## File: $relativePath

``html
{% extends "base.html" %}
{% block title %}Patient Dashboard - ClinicEase{% endblock %}
{% block page_css %}
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static', filename='css/pages/patient-dashboard.css') }}">
{% endblock %}
{% block content %}
<div class="container patient-dashboard">
    <header class="dashboard-welcome">
        <div>
            <p class="eyebrow">PATIENT DASHBOARD</p>
            <h1>Welcome, {{ user.name }}</h1>
            <p>Manage your appointments or find a time that works for you.</p>
        </div>
        <div class="welcome-summary" aria-label="Appointment summary">
            <div class="summary-item">
                <span class="material-symbols-outlined" aria-hidden="true">schedule</span>
                <span class="summary-count">{{ upcoming_appointments|selectattr('status', 'equalto', 'Pending')|list|length }}</span>
                <span class="summary-label">Pending</span>
            </div>
            <div class="summary-item">
                <span class="material-symbols-outlined" aria-hidden="true">check_circle</span>
                <span class="summary-count">{{ upcoming_appointments|selectattr('status', 'equalto', 'Confirmed')|list|length }}</span>
                <span class="summary-label">Confirmed</span>
            </div>
            <div class="summary-item">
                <span class="material-symbols-outlined" aria-hidden="true">history</span>
                <span class="summary-count">{{ past_appointments|length }}</span>
                <span class="summary-label">Past visits</span>
            </div>
        </div>
    </header>

    <div class="dashboard-tabs" role="tablist" aria-label="Patient dashboard sections">
        <button id="appointments-tab" class="dashboard-tab is-active" type="button" role="tab"
                aria-selected="true" aria-controls="appointments-panel" data-dashboard-tab="appointments-panel">
            <span class="material-symbols-outlined" aria-hidden="true">event_note</span>
            My Appointments
        </button>
        <button id="booking-tab" class="dashboard-tab" type="button" role="tab"
                aria-selected="false" aria-controls="booking-panel" data-dashboard-tab="booking-panel" tabindex="-1">
            <span class="material-symbols-outlined" aria-hidden="true">add_circle</span>
            Book Appointment
        </button>
    </div>

    <section id="appointments-panel" class="dashboard-tab-panel" role="tabpanel"
             aria-labelledby="appointments-tab">
        <div class="panel-heading">
            <div>
                <h2>My Appointments</h2>
                <p>Choose an appointment to see its details.</p>
            </div>
            <button class="btn btn-primary" type="button" data-open-tab="booking-panel">
                <span class="material-symbols-outlined" aria-hidden="true">add_circle</span>
                Book an appointment
            </button>
        </div>

        <section class="appointment-group" aria-labelledby="upcoming-title">
            <div class="group-heading">
                <h3 id="upcoming-title">Upcoming</h3>
                <span class="group-count">{{ upcoming_appointments|length }}</span>
            </div>
            {% if upcoming_appointments %}
                <div class="appointment-list">
                    {% for appt in upcoming_appointments %}
                        <button class="appointment-card" type="button"
                                data-appointment-details
                                data-appt-id="{{ appt.appointment_id }}"
                                data-appt-date="{{ appt.slot_date }}"
                                data-appt-time="{{ appt.time }}"
                                data-appt-purpose="{{ appt.purpose }}"
                                data-appt-status="{{ appt.status }}"
                                data-appt-contact="{{ appt.contact_number or 'Not provided' }}"
                                data-appt-created="{{ appt.created_at }}"
                                aria-label="View {{ appt.status|lower }} appointment on {{ appt.slot_date }} at {{ appt.time }}">
                            <span class="appointment-card__date-icon material-symbols-outlined" aria-hidden="true">calendar_month</span>
                            <span class="appointment-card__main">
                                <span class="appointment-card__date">{{ appt.slot_date }}</span>
                                <span class="appointment-card__time">{{ appt.time }}</span>
                                <span class="appointment-card__purpose">{{ appt.purpose }}</span>
                            </span>
                            <span class="status-badge status-{{ appt.status|lower }}">
                                <span class="material-symbols-outlined" aria-hidden="true">
                                    {% if appt.status == 'Pending' %}schedule
                                    {% elif appt.status == 'Confirmed' %}check_circle
                                    {% elif appt.status == 'Completed' %}task_alt
                                    {% elif appt.status == 'Cancelled' %}cancel
                                    {% else %}event
                                    {% endif %}
                                </span>
                                {{ appt.status }}
                            </span>
                            <span class="material-symbols-outlined appointment-card__open" aria-hidden="true">chevron_right</span>
                        </button>
                    {% endfor %}
                </div>
            {% else %}
                <div class="empty-state">
                    <span class="material-symbols-outlined" aria-hidden="true">event_available</span>
                    <h4>No upcoming appointments</h4>
                    <p>When you request an appointment, it will appear here.</p>
                    <button class="btn btn-secondary" type="button" data-open-tab="booking-panel">
                        Find an appointment time
                    </button>
                </div>
            {% endif %}
        </section>

        <section class="appointment-group past-appointment-group" aria-labelledby="past-title">
            <div class="group-heading">
                <h3 id="past-title">Past appointments</h3>
                <span class="group-count">{{ past_appointments|length }}</span>
            </div>
            {% if past_appointments %}
                <div class="appointment-list">
                    {% for appt in past_appointments %}
                        <button class="appointment-card appointment-card--past" type="button"
                                data-appointment-details
                                data-appt-id="{{ appt.appointment_id }}"
                                data-appt-date="{{ appt.slot_date }}"
                                data-appt-time="{{ appt.time }}"
                                data-appt-purpose="{{ appt.purpose }}"
                                data-appt-status="{{ appt.status }}"
                                data-appt-contact="{{ appt.contact_number or 'Not provided' }}"
                                data-appt-created="{{ appt.created_at }}"
                                aria-label="View {{ appt.status|lower }} appointment on {{ appt.slot_date }} at {{ appt.time }}">
                            <span class="appointment-card__date-icon material-symbols-outlined" aria-hidden="true">history</span>
                            <span class="appointment-card__main">
                                <span class="appointment-card__date">{{ appt.slot_date }}</span>
                                <span class="appointment-card__time">{{ appt.time }}</span>
                                <span class="appointment-card__purpose">{{ appt.purpose }}</span>
                            </span>
                            <span class="status-badge status-{{ appt.status|lower }}">
                                <span class="material-symbols-outlined" aria-hidden="true">
                                    {% if appt.status == 'Pending' %}schedule
                                    {% elif appt.status == 'Confirmed' %}check_circle
                                    {% elif appt.status == 'Completed' %}task_alt
                                    {% elif appt.status == 'Cancelled' %}cancel
                                    {% else %}event
                                    {% endif %}
                                </span>
                                {{ appt.status }}
                            </span>
                            <span class="material-symbols-outlined appointment-card__open" aria-hidden="true">chevron_right</span>
                        </button>
                    {% endfor %}
                </div>
            {% else %}
                <p class="empty-history">Your past appointments will appear here.</p>
            {% endif %}
        </section>
    </section>

    <section id="booking-panel" class="dashboard-tab-panel" role="tabpanel"
             aria-labelledby="booking-tab" hidden>
        <div class="panel-heading">
            <div>
                <h2>Book an appointment</h2>
                <p>Choose an available date and time, then tell us what you need.</p>
            </div>
        </div>

        <ol class="booking-stepper" aria-label="Booking progress">
            <li class="booking-step is-current" data-step-indicator="1" aria-current="step">
                <span class="booking-step__number">1</span>
                <span><strong>Choose a date</strong><small>Pick a day</small></span>
            </li>
            <li class="booking-step" data-step-indicator="2">
                <span class="booking-step__number">2</span>
                <span><strong>Choose a time</strong><small>Select a slot</small></span>
            </li>
            <li class="booking-step" data-step-indicator="3">
                <span class="booking-step__number">3</span>
                <span><strong>Your details</strong><small>Review and send</small></span>
            </li>
        </ol>

        <div id="booking-selection" class="booking-selection-grid" data-step-panel="selection">
            <section class="booking-card calendar-card" aria-labelledby="calendar-title">
                <div class="booking-card__heading">
                    <span class="material-symbols-outlined" aria-hidden="true">calendar_month</span>
                    <div>
                        <h3 id="calendar-title">Choose a date</h3>
                        <p>Available days are highlighted.</p>
                    </div>
                </div>
                <div class="calendar-toolbar">
                    <button id="calendar-previous" class="calendar-nav-button" type="button"
                            aria-label="Show previous month" disabled>
                        <span class="material-symbols-outlined" aria-hidden="true">chevron_left</span>
                    </button>
                    <h4 id="calendar-month" aria-live="polite"></h4>
                    <button id="calendar-next" class="calendar-nav-button" type="button"
                            aria-label="Show next month" disabled>
                        <span class="material-symbols-outlined" aria-hidden="true">chevron_right</span>
                    </button>
                </div>
                <div id="availability-calendar" class="availability-calendar"
                     role="group" aria-label="Available appointment dates"></div>
                <p id="calendar-feedback" class="inline-feedback" role="alert" hidden></p>
                <p id="selected-date-label" class="selection-hint" aria-live="polite">
                    Select a highlighted date to see available times.
                </p>
            </section>

            <section class="booking-card time-card" aria-labelledby="time-title">
                <div class="booking-card__heading">
                    <span class="material-symbols-outlined" aria-hidden="true">schedule</span>
                    <div>
                        <h3 id="time-title">Choose a time</h3>
                        <p id="time-panel-description">Select a date first to see available times.</p>
                    </div>
                </div>
                <div id="available-times-list" class="available-times-list"
                     aria-label="Available times for selected date" aria-live="polite"></div>
                <div id="time-empty-state" class="time-empty-state">
                    <span class="material-symbols-outlined" aria-hidden="true">event</span>
                    <p>Your available appointment times will appear here.</p>
                </div>
                <div class="wizard-actions wizard-actions--selection">
                    <button id="details-step-button" class="btn btn-primary" type="button" disabled>
                        Continue to your details
                        <span class="material-symbols-outlined" aria-hidden="true">arrow_forward</span>
                    </button>
                </div>
            </section>
        </div>

        <section id="booking-details" class="booking-card booking-details" data-step-panel="details" hidden>
            <div class="booking-card__heading">
                <span class="material-symbols-outlined" aria-hidden="true">assignment</span>
                <div>
                    <h3>Appointment details</h3>
                    <p>Check your selection and tell us about your visit.</p>
                </div>
            </div>
            <div class="booking-summary" aria-live="polite">
                <div>
                    <span class="summary-caption">Date</span>
                    <strong id="booking-summary-date">Not selected</strong>
                </div>
                <div>
                    <span class="summary-caption">Time</span>
                    <strong id="booking-summary-time">Not selected</strong>
                </div>
            </div>
            <form id="booking-form" action="{{ url_for('book_appointment_slot') }}" method="post">
                <input id="selected-slot-id" name="slot_id" type="hidden">
                <div class="form-group">
                    <label class="form-label" for="booking-purpose">Purpose of visit</label>
                    <textarea class="form-textarea" id="booking-purpose" name="purpose"
                              maxlength="255" rows="4" required
                              aria-describedby="purpose-help"></textarea>
                    <p id="purpose-help" class="form-help">Briefly describe the reason for your appointment.</p>
                </div>
                <div class="form-group">
                    <label class="form-label" for="booking-contact">Contact number <span class="optional-label">(optional)</span></label>
                    <input class="form-input" id="booking-contact" name="contact_number" type="tel"
                           autocomplete="tel" inputmode="tel" maxlength="20"
                           value="{{ user.contact_number or '' }}">
                    <p class="form-help">We may use this number if the clinic needs to contact you.</p>
                </div>
                <div id="booking-feedback" class="inline-feedback" role="alert" hidden></div>
                <div class="wizard-actions wizard-actions--details">
                    <button id="back-to-times" class="btn btn-secondary" type="button">
                        <span class="material-symbols-outlined" aria-hidden="true">arrow_back</span>
                        Back to times
                    </button>
                    <button id="submit-booking" class="btn btn-primary" type="submit">
                        <span class="material-symbols-outlined" aria-hidden="true">send</span>
                        Submit appointment request
                    </button>
                </div>
            </form>
        </section>

        {% if slots %}
            <div id="available-slot-data" class="visually-hidden" aria-hidden="true">
                {% for slot in slots %}
                    <span data-slot-option data-slot-id="{{ slot.slot_id }}"
                          data-slot-date="{{ slot.slot_date }}"
                          data-slot-time="{{ slot.time }}"></span>
                {% endfor %}
            </div>
        {% endif %}
        <div id="no-slots-message" class="empty-state booking-empty-state" {% if slots %}hidden{% endif %}>
            <span class="material-symbols-outlined" aria-hidden="true">event_busy</span>
            <h3>No available times right now</h3>
            <p>Please check back later or contact the clinic for assistance.</p>
        </div>
    </section>
</div>

<div id="appointment-modal" class="modal-backdrop hidden" aria-hidden="true" hidden>
    <section class="modal-dialog appointment-details-modal" role="dialog" aria-modal="true"
             aria-labelledby="appointment-modal-title" tabindex="-1">
        <button class="modal-close-btn" type="button" aria-label="Close appointment details"
                data-close-appointment-modal>
            <span class="material-symbols-outlined" aria-hidden="true">close</span>
        </button>
        <header class="modal-header">
            <h2 id="appointment-modal-title">Appointment details</h2>
            <span id="modal-status-badge" class="status-badge"></span>
        </header>
        <div class="modal-body">
            <dl class="appointment-details-list">
                <div><dt>Date</dt><dd id="modal-date"></dd></div>
                <div><dt>Time</dt><dd id="modal-time"></dd></div>
                <div><dt>Purpose</dt><dd id="modal-purpose"></dd></div>
                <div><dt>Status</dt><dd id="modal-status"></dd></div>
                <div><dt>Contact number</dt><dd id="modal-contact"></dd></div>
                <div><dt>Appointment ID</dt><dd id="modal-id"></dd></div>
                <div><dt>Request submitted</dt><dd id="modal-created"></dd></div>
            </dl>
            <div id="modal-feedback" class="inline-feedback" role="alert" hidden></div>
            <div class="modal-actions">
                <button class="btn btn-secondary" type="button" data-close-appointment-modal>Close</button>
                <button id="cancel-appointment-button" class="btn btn-danger" type="button" hidden>
                    <span class="material-symbols-outlined" aria-hidden="true">cancel</span>
                    Cancel appointment
                </button>
            </div>
        </div>
    </section>
</div>
{% endblock %}
{% block scripts %}
<script src="{{ url_for('static', filename='js/patient-dashboard.js') }}"></script>
{% endblock %}

``

---

