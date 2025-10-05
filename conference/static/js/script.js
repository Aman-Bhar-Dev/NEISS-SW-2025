document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  // Theme toggle
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    themeToggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
  });

  // Mobile menu toggle
  menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
  });

  // New target date → 21st November 2025 00:00:00
  const targetDate = new Date("November 21, 2025 00:00:00").getTime();

  // Countdown function
  const countdown = () => {
    const now = new Date().getTime();
    const gap = targetDate - now;

    if (gap <= 0) {
      // When time is up, just show 00:00:00
      document.getElementById("days").innerText = "00";
      document.getElementById("hours").innerText = "00";
      document.getElementById("minutes").innerText = "00";
      return;
    }

    const day = 1000 * 60 * 60 * 24;
    const hour = 1000 * 60 * 60;
    const minute = 1000 * 60;

    document.getElementById("days").innerText = String(Math.floor(gap / day)).padStart(2, '0');
    document.getElementById("hours").innerText = String(Math.floor((gap % day) / hour)).padStart(2, '0');
    document.getElementById("minutes").innerText = String(Math.floor((gap % hour) / minute)).padStart(2, '0');
  };

  // Run immediately, then every second
  countdown();
  setInterval(countdown, 1000);
});
