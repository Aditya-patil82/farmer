// ============================================================
// script.js — Main JavaScript File
// Local Farmer Information System
// ============================================================
// This file handles:
//   1. Mobile navigation toggle
//   2. Crop search filtering (live, client-side)
//   3. Market price filtering
//   4. Weather form interactions
//   5. Smooth scroll & general UI helpers
// ============================================================

// -------------------------------------------------------
// Wait for the page to fully load before running code
// -------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {

    // Call all setup functions when the page is ready
    setupMobileNav();
    setupCropSearch();
    setupMarketFilter();
    setupWeatherForm();
    markActiveNavLink();
    setupTipsCategoryBtns();

});


// ============================================================
// 1. MOBILE NAVIGATION TOGGLE
// ============================================================
/**
 * Shows/hides the nav menu on small screens.
 * The hamburger button has id="nav-toggle".
 * The nav links container has id="nav-links".
 */
function setupMobileNav() {
    var toggleBtn = document.getElementById('nav-toggle');
    var navLinks  = document.getElementById('nav-links');

    if (!toggleBtn || !navLinks) return; // Not on this page

    // Toggle the menu when hamburger is clicked
    toggleBtn.addEventListener('click', function () {
        // Switch the 'open' class on the button (controls ☰ → ✕ animation)
        toggleBtn.classList.toggle('open');
        // Switch the 'open' class on the links (shows/hides them)
        navLinks.classList.toggle('open');
    });

    // Close the menu when the user clicks any nav link
    navLinks.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            toggleBtn.classList.remove('open');
            navLinks.classList.remove('open');
        });
    });

    // Close the menu if the user clicks outside the nav area
    document.addEventListener('click', function (event) {
        var navbar = document.querySelector('.navbar');
        if (navbar && !navbar.contains(event.target)) {
            toggleBtn.classList.remove('open');
            navLinks.classList.remove('open');
        }
    });
}


// ============================================================
// 2. MARK ACTIVE NAV LINK
// ============================================================
/**
 * Adds the 'active' CSS class to the nav link that matches the
 * current page URL. This highlights the current page in the nav.
 */
function markActiveNavLink() {
    var currentPath = window.location.pathname;
    var links = document.querySelectorAll('.nav-links a');

    links.forEach(function (link) {
        var linkPath = link.getAttribute('href');
        // Exact match, or the path starts with the link path (for sub-pages)
        if (linkPath === currentPath ||
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
}


// ============================================================
// 3. LIVE CROP SEARCH (Client-side filtering)
// ============================================================
/**
 * Filters the crop cards as the user types in the search box.
 * This is a client-side filter — it doesn't make a server request.
 * Element IDs used:
 *   - crop-search-input (the text input)
 *   - crop-cards-container (wrapper around all crop cards)
 *   - no-results-msg (message shown when nothing matches)
 */
function setupCropSearch() {
    var searchInput = document.getElementById('crop-search-input');
    if (!searchInput) return; // Not on the crops page

    searchInput.addEventListener('input', function () {
        var query = this.value.toLowerCase().trim();

        // Select all individual crop cards
        var cards = document.querySelectorAll('.crop-card');
        var visibleCount = 0;

        cards.forEach(function (card) {
            // Each card has a data-name attribute with the crop name
            var name = card.getAttribute('data-name') || '';
            if (name.toLowerCase().includes(query)) {
                card.style.display = '';    // Show card
                visibleCount++;
            } else {
                card.style.display = 'none'; // Hide card
            }
        });

        // Show "No results" message if nothing matches
        var noResults = document.getElementById('no-results-msg');
        if (noResults) {
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    });
}


// ============================================================
// 4. MARKET PRICE FILTER
// ============================================================
/**
 * Filters market price table rows when the user selects a crop
 * from the dropdown on the market prices page.
 * Element IDs:
 *   - market-filter-select (the <select> dropdown)
 *   - market-table-body   (the <tbody> of the price table)
 */
function setupMarketFilter() {
    var filterSelect = document.getElementById('market-filter-select');
    if (!filterSelect) return;

    filterSelect.addEventListener('change', function () {
        var selectedCrop = this.value.toLowerCase();
        var rows = document.querySelectorAll('#market-table-body tr');

        rows.forEach(function (row) {
            var cropCell = row.querySelector('[data-crop]');
            if (!cropCell) return;

            var cropName = cropCell.getAttribute('data-crop').toLowerCase();

            if (selectedCrop === '' || cropName.includes(selectedCrop)) {
                row.style.display = '';      // Show row
            } else {
                row.style.display = 'none';  // Hide row
            }
        });
    });
}


// ============================================================
// 5. WEATHER FORM VALIDATION
// ============================================================
/**
 * Prevents empty location search on the weather page.
 * Element IDs:
 *   - weather-form          (the <form>)
 *   - weather-location-input (the text input)
 *   - weather-input-error   (error message span)
 */
function setupWeatherForm() {
    var weatherForm = document.getElementById('weather-form');
    if (!weatherForm) return;

    weatherForm.addEventListener('submit', function (event) {
        var input = document.getElementById('weather-location-input');
        var errorMsg = document.getElementById('weather-input-error');

        if (!input || input.value.trim() === '') {
            event.preventDefault(); // Stop the form from submitting
            if (errorMsg) {
                errorMsg.textContent = '⚠️ Please enter a location name first.';
                errorMsg.style.display = 'block';
            }
            if (input) {
                input.focus();
                input.style.borderColor = '#ef4444'; // Red border
            }
        } else {
            // Clear any previous error
            if (errorMsg) { errorMsg.style.display = 'none'; }
            if (input)    { input.style.borderColor = ''; }
        }
    });
}


// ============================================================
// 6. FARMING TIPS — Category Filter Buttons
// ============================================================
/**
 * Highlights the active category button on the tips page.
 * The active state is handled by CSS (.active class),
 * and the Flask route handles the actual filtering server-side.
 * This function just ensures the button appearance stays in sync.
 */
function setupTipsCategoryBtns() {
    var btns = document.querySelectorAll('.category-btn');
    if (btns.length === 0) return;

    // Read the current category from URL params
    var params = new URLSearchParams(window.location.search);
    var activeCategory = params.get('category') || '';

    btns.forEach(function (btn) {
        var btnCategory = btn.getAttribute('data-category') || '';
        if (btnCategory === activeCategory) {
            btn.classList.add('active');
        }
    });
}


// ============================================================
// 7. UTILITY — Smooth scroll to section (optional helper)
// ============================================================
/**
 * Smoothly scrolls to any element by its ID.
 * Usage: scrollToSection('features')
 */
function scrollToSection(sectionId) {
    var el = document.getElementById(sectionId);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}


// ============================================================
// 8. UTILITY — Show a temporary toast notification
// ============================================================
/**
 * Shows a brief notification message at the bottom of the screen.
 * Useful for confirming actions (e.g., "Copied!").
 * @param {string} message - The text to display
 * @param {number} duration - How long to show it in milliseconds
 */
function showToast(message, duration) {
    duration = duration || 3000; // Default 3 seconds

    // Create toast element
    var toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = [
        'position: fixed',
        'bottom: 24px',
        'left: 50%',
        'transform: translateX(-50%)',
        'background: #1e4d35',
        'color: white',
        'padding: 12px 24px',
        'border-radius: 9999px',
        'font-size: 0.9rem',
        'font-weight: 500',
        'z-index: 9999',
        'box-shadow: 0 4px 20px rgba(0,0,0,0.2)',
        'animation: fadeIn 0.3s ease',
        'pointer-events: none'
    ].join(';');

    document.body.appendChild(toast);

    // Remove after duration
    setTimeout(function () {
        toast.remove();
    }, duration);
}
