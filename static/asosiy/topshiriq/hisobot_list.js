/*
 * Hisobot List sahifasi uchun JavaScript
 * Author: System  
 * Date: 2025-08-20
 */

$(document).ready(function() {
    'use strict';

    // ===== SIDEBAR FUNCTIONALITY =====
    function initSidebar() {
        // Sidebar toggle click handler
        $(document).on('click', '.sidebar-toggle', function(e) {
            e.preventDefault();
            $('body').toggleClass('sidebar-toggled');
            $('.main-content').toggleClass('sidebar-collapsed');
            
            // LocalStorage ga saqlash
            const isToggled = $('body').hasClass('sidebar-toggled');
            localStorage.setItem('sidebarToggled', isToggled);
        });

        // LocalStorage dan oldingi holatni yuklash
        const savedState = localStorage.getItem('sidebarToggled');
        if (savedState === 'true') {
            $('body').addClass('sidebar-toggled');
            $('.main-content').addClass('sidebar-collapsed');
        }
    }

    // ===== RESPONSIVE HANDLING =====
    function handleResponsive() {
        function checkScreenSize() {
            const windowWidth = $(window).width();
            
            if (windowWidth < 992) {
                $('.main-content').removeClass('sidebar-collapsed');
                $('body').removeClass('sidebar-toggled');
            } else {
                // Desktop holatida localStorage dan yuklash
                const savedState = localStorage.getItem('sidebarToggled');
                if (savedState === 'true') {
                    $('body').addClass('sidebar-toggled');
                    $('.main-content').addClass('sidebar-collapsed');
                }
            }
        }

        // Window resize event
        $(window).resize(function() {
            clearTimeout(window.resizeTimer);
            window.resizeTimer = setTimeout(checkScreenSize, 250);
        });

        // Initial check
        checkScreenSize();
    }

    // ===== MOBILE SIDEBAR =====
    function initMobileSidebar() {
        // Mobile sidebar close when clicking outside
        $(document).on('click', function(e) {
            if ($(window).width() < 992) {
                if (!$(e.target).closest('.sidebar, .sidebar-toggle').length) {
                    $('.sidebar').removeClass('show');
                    $('.navbar-toggler').removeClass('active');
                }
            }
        });

        // Navbar toggler click
        $(document).on('click', '.navbar-toggler', function(e) {
            e.preventDefault();
            $(this).toggleClass('active');
            $('.sidebar').toggleClass('show');
        });
    }

    // ===== TABLE ENHANCEMENTS =====
    function initTableFeatures() {
        // Table row click enhancement
        $('.table tbody tr').on('click', function(e) {
            // Agar button yoki link bosilgan bo'lsa, boshqa ishni qilmaslik
            if ($(e.target).closest('a, button').length) {
                return;
            }
            
            // Row selection effect
            $(this).addClass('table-active').siblings().removeClass('table-active');
        });

        // Tooltip initialization for action buttons
        $('[data-bs-toggle="tooltip"]').each(function() {
            new bootstrap.Tooltip(this);
        });
    }

    // ===== STATS CARDS ANIMATION =====
    function initStatsCards() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        });

        $('.stats-card').each(function() {
            observer.observe(this);
        });
    }

    // ===== SEARCH FUNCTIONALITY =====
    function initSearch() {
        let searchTimeout;
        
        $(document).on('input', '#searchInput', function() {
            const searchTerm = $(this).val().toLowerCase();
            
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterTable(searchTerm);
            }, 300);
        });

        function filterTable(searchTerm) {
            $('.table tbody tr').each(function() {
                const rowText = $(this).text().toLowerCase();
                const isVisible = rowText.includes(searchTerm);
                
                $(this).toggle(isVisible);
            });

            // Update empty state
            const visibleRows = $('.table tbody tr:visible').length;
            if (visibleRows === 0 && searchTerm !== '') {
                showEmptyState('Qidiruv natijasi topilmadi');
            } else {
                hideEmptyState();
            }
        }
    }

    // ===== EMPTY STATE =====
    function showEmptyState(message) {
        if ($('.empty-state').length === 0) {
            const emptyState = `
                <tr class="empty-state">
                    <td colspan="7" class="text-center py-5">
                        <div class="text-muted">
                            <i class="fas fa-search fa-3x mb-3 text-gray-300"></i>
                            <h5 class="text-gray-600">${message}</h5>
                        </div>
                    </td>
                </tr>
            `;
            $('.table tbody').append(emptyState);
        }
    }

    function hideEmptyState() {
        $('.empty-state').remove();
    }

    // ===== CONFIRMATION DIALOGS =====
    function initConfirmations() {
        // Confirm buttons with custom messages
        $('.btn-success[onclick*="confirm"]').on('click', function(e) {
            e.preventDefault();
            
            const result = confirm('Hisobotni tasdiqlashni xohlaysizmi?\n\nTasdiqlangandan so\'ng bu amalni bekor qila olmaysiz.');
            if (result) {
                window.location.href = $(this).attr('href');
            }
        });

        $('.btn-danger[onclick*="confirm"]').on('click', function(e) {
            e.preventDefault();
            
            const result = confirm('Hisobotni rad etishni xohlaysizmi?\n\nRad etilgan hisobot qayta ko\'rib chiqilishi mumkin.');
            if (result) {
                window.location.href = $(this).attr('href');
            }
        });
    }

    // ===== LOADING STATES =====
    function initLoadingStates() {
        // Download buttons loading state
        $('.btn[href*="download"]').on('click', function() {
            const $btn = $(this);
            const originalHtml = $btn.html();
            
            $btn.html('<i class="fas fa-spinner fa-spin"></i>').prop('disabled', true);
            
            setTimeout(() => {
                $btn.html(originalHtml).prop('disabled', false);
            }, 3000);
        });
    }

    // ===== PERFORMANCE OPTIMIZATION =====
    function initPerformance() {
        // Debounce resize events
        let resizeTimeout;
        $(window).on('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                $(window).trigger('debouncedResize');
            }, 150);
        });

        // Lazy loading for images if any
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            $('.lazy').each(function() {
                imageObserver.observe(this);
            });
        }
    }

    // ===== ERROR HANDLING =====
    function initErrorHandling() {
        // Global error handler
        window.addEventListener('error', function(e) {
            console.error('JavaScript Error:', e.error);
            // Optional: Send error to logging service
        });

        // Unhandled promise rejections
        window.addEventListener('unhandledrejection', function(e) {
            console.error('Unhandled Promise Rejection:', e.reason);
            // Optional: Send error to logging service
        });
    }

    // ===== ACCESSIBILITY =====
    function initAccessibility() {
        // Keyboard navigation for custom elements
        $('.dropdown-toggle').on('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                $(this).click();
            }
        });

        // Focus management for modals
        $(document).on('shown.bs.modal', '.modal', function() {
            $(this).find('[autofocus]').focus();
        });
    }

    // ===== INITIALIZATION =====
    function init() {
        try {
            initSidebar();
            handleResponsive();
            initMobileSidebar();
            initTableFeatures();
            initStatsCards();
            initSearch();
            initConfirmations();
            initLoadingStates();
            initPerformance();
            initErrorHandling();
            initAccessibility();
            
            console.log('Hisobot List: All modules initialized successfully');
        } catch (error) {
            console.error('Hisobot List: Initialization error:', error);
        }
    }

    // Start the application
    init();

    // ===== PUBLIC API =====
    window.HisobotList = {
        refreshTable: function() {
            location.reload();
        },
        
        exportData: function() {
            // Custom export functionality
            console.log('Export functionality not implemented yet');
        },
        
        updateStats: function() {
            // Update statistics cards
            console.log('Stats update functionality not implemented yet');
        }
    };
});
