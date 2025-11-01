// home.js

// Handle subscription form
/* REMOVED: Old 'subscribeForm' listener as the form is gone.
  If you add a new subscription form, you can wire it up here.
*/

// Smooth scroll for anchor links
document.querySelectorAll('a.smooth-scroll').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

