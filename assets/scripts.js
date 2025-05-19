document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileSubmenus = document.querySelectorAll('.mobile-submenu');
    
    mobileMenuButton.addEventListener('click', function() {
        mobileMenuButton.classList.toggle('open');
        mobileMenu.classList.toggle('is-active');
    });
    
    mobileSubmenus.forEach(submenu => {
        const toggle = submenu.querySelector('div');
        const menu = submenu.querySelector('div:last-child');
        
        toggle.addEventListener('click', function() {
            menu.classList.toggle('hidden');
            const icon = toggle.querySelector('svg');
            if (menu.classList.contains('hidden')) {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>';
            } else {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>';
            }
        });
    });
    
    // Theme Toggle - Fixed version
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        html.classList.remove('light');
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
        html.classList.add('light');
    }
    
    themeToggle.addEventListener('click', function() {
        if (html.classList.contains('dark')) {
            html.classList.remove('dark');
            html.classList.add('light');
            localStorage.setItem('theme', 'light');
        } else {
            html.classList.remove('light');
            html.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        }
    });

    // Sticky Header
    const header = document.querySelector('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('bg-cyan-900', 'dark:bg-gray-900');
            header.classList.remove('bg-opacity-90', 'dark:bg-opacity-90');
        } else {
            header.classList.add('bg-opacity-90', 'dark:bg-opacity-90');
        }
    });
});
