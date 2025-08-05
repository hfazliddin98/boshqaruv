$(document).ready(function () {
    // Sidebar toggle functionality
    $('#sidebarToggle').click(function () {
        $('#sidebar').toggleClass('collapsed');
        $('#mainContent').toggleClass('expanded');
        if ($(window).width() < 992) {
            $('#sidebar').toggleClass('show');
        }
    });

    // Close sidebar when clicking outside on mobile
    $(document).click(function (e) {
        if ($(window).width() < 992) {
            if (!$(e.target).closest('#sidebar').length && !$(e.target).is('#sidebarToggle')) {
                $('#sidebar').removeClass('show');
            }
        }
    });

    // Prevent closing when clicking inside sidebar
    $('#sidebar').click(function (e) {
        e.stopPropagation();
    });

    // Active menu item highlight
    $('.sidebar-menu a').click(function () {
        $('.sidebar-menu a').removeClass('active');
        $(this).addClass('active');
    });

    // Qidiruv funksiyasi (dekanlar va boshliqlar uchun universal)
    $('#searchButton').click(function() {
        const searchText = $('#searchInput').val().toLowerCase();
        $('#dataTable tbody tr').each(function() {
            const rowText = $(this).text().toLowerCase();
            $(this).toggle(rowText.includes(searchText));
        });
    });
    $('#searchInput').keypress(function(e) {
        if (e.which === 13) {
            $('#searchButton').click();
        }
    });

    // Parol ko'rsatish/berkitish funksiyasi
    $('.toggle-password').click(function () {
        let input = $(this).siblings('input');
        let icon = $(this).find('i');
        if (input.attr('type') === 'password') {
            input.attr('type', 'text');
            icon.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            input.attr('type', 'password');
            icon.removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });
});