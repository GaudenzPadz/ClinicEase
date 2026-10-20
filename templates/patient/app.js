const toast = document.getElementById('toast');
function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(window.toastTimer);
    window.toastTimer = setTimeout(() => toast.classList.remove('show'), 3200);
}

document.querySelectorAll('[data-toast]').forEach(el => el.addEventListener('click', e => { e.preventDefault(); showToast(el.dataset.toast) }));
const login = document.getElementById('loginForm'); if (login) login.addEventListener('submit', e => { e.preventDefault(); location.href = 'patient-dashboard.html' });
const signup = document.getElementById('signupForm'); if (signup) signup.addEventListener('submit', e => { e.preventDefault(); showToast('Demo only: account creation needs a backend/database.'); setTimeout(() => location.href = 'index.html', 1800) });
document.querySelectorAll('.slot[data-time]').forEach(btn => btn.addEventListener('click', () => { document.querySelectorAll('.slot[data-time]').forEach(b => b.classList.remove('selected')); btn.classList.add('selected'); const input = document.getElementById('selectedTime'); if (input) input.value = btn.dataset.time }));
const booking = document.getElementById('bookingForm'); if (booking) booking.addEventListener('submit', e => { e.preventDefault(); showToast('Demo request submitted. In the full system, this would be saved as Pending.'); });
const tabs = document.querySelectorAll('[data-filter]'); const rows = [...document.querySelectorAll('#appointmentRows tr')]; const search = document.getElementById('search'); let filter = 'All';
function filterRows() { let count = 0; const q = (search?.value || '').toLowerCase(); rows.forEach(row => { const okFilter = filter === 'All' || row.dataset.kind === filter; const okSearch = row.innerText.toLowerCase().includes(q); row.style.display = okFilter && okSearch ? '' : 'none'; if (okFilter && okSearch) count++ }); document.getElementById('empty')?.classList.toggle('hidden', count !== 0) }
tabs.forEach(tab => tab.addEventListener('click', () => { tabs.forEach(t => t.classList.remove('active')); tab.classList.add('active'); filter = tab.dataset.filter; filterRows() })); if (search) search.addEventListener('input', filterRows);
