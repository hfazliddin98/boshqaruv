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

// Fayllarni boshqarish va drag-drop
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('files');
    const fileDropArea = document.getElementById('fileDropArea');
    const fileList = document.getElementById('fileList');
    let allFiles = [];

    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            handleFiles(this.files);
        });
    }

    if (fileDropArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, unhighlight, false);
        });

        function highlight() {
            fileDropArea.classList.add('border-primary', 'bg-light');
        }

        function unhighlight() {
            fileDropArea.classList.remove('border-primary', 'bg-light');
        }

        fileDropArea.addEventListener('drop', function (e) {
            const dt = e.dataTransfer;
            handleFiles(dt.files);
        });
    }

    function handleFiles(files) {
        Array.from(files).forEach(file => {
            // File size validation (10MB)
            if (file.size > 10 * 1024 * 1024) {
                showAlert(`Fayl hajmi juda katta: ${file.name} (Maksimum 10MB)`, 'danger');
                return;
            }
            // File type validation
            const validTypes = [
                'image/jpeg', 'image/png', 'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ];
            if (!validTypes.includes(file.type)) {
                showAlert(`Fayl formati qo'llab-quvvatlanmaydi: ${file.name}`, 'warning');
                return;
            }
            if (!allFiles.some(f => f.name === file.name && f.size === file.size)) {
                allFiles.push(file);
            }
        });
        renderFileList();
    }

    function renderFileList() {
        if (!fileList) return;
        fileList.innerHTML = '';
        if (allFiles.length > 0) {
            const listGroup = document.createElement('div');
            listGroup.className = 'list-group';
            allFiles.forEach((file, index) => {
                const item = document.createElement('div');
                item.className = 'list-group-item d-flex justify-content-between align-items-center';
                // File type icon
                let fileIcon = 'fa-file';
                if (file.type.startsWith('image/')) fileIcon = 'fa-file-image text-info';
                else if (file.type === 'application/pdf') fileIcon = 'fa-file-pdf text-danger';
                else if (file.type.includes('wordprocessingml')) fileIcon = 'fa-file-word text-primary';
                else if (file.type.includes('spreadsheetml')) fileIcon = 'fa-file-excel text-success';
                item.innerHTML = `
                    <div class="d-flex align-items-center flex-grow-1">
                        <i class="fas ${fileIcon} me-3 fs-4"></i>
                        <div class="text-truncate me-3">
                            <div class="fw-bold text-truncate">${file.name}</div>
                            <small class="text-muted">${formatSize(file.size)} • ${file.type}</small>
                        </div>
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeFile(${index})">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                `;
                listGroup.appendChild(item);
            });
            fileList.appendChild(listGroup);
            updateFileInput();
        }
    }

    window.removeFile = function (index) {
        allFiles.splice(index, 1);
        renderFileList();
        showAlert('Fayl o\'chirildi', 'success');
    };

    function updateFileInput() {
        if (!fileInput) return;
        const dataTransfer = new DataTransfer();
        allFiles.forEach(file => dataTransfer.items.add(file));
        fileInput.files = dataTransfer.files;
    }

    function formatSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Byte';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    }

    function showAlert(message, type) {
        if (!fileList) return;
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        fileList.prepend(alert);
        setTimeout(() => alert.remove(), 5000);
    }
});

// Sidebar boshqaruvi va form validation
$(document).ready(function () {
    $('#sidebarToggle').click(function () {
        $('#sidebar').toggleClass('collapsed');
        $('#mainContent').toggleClass('expanded');
        if ($(window).width() < 992) {
            $('#sidebar').toggleClass('show');
        }
    });

    $(document).click(function (e) {
        if ($(window).width() < 992 && !$(e.target).closest('#sidebar, #sidebarToggle').length) {
            $('#sidebar').removeClass('show');
        }
    });

    // Bootstrap form validation
    (function () {
        'use strict'
        const forms = document.querySelectorAll('.needs-validation')
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
            // Real-time validation
            form.querySelectorAll('input, textarea, select').forEach(input => {
                input.addEventListener('input', function () {
                    if (input.checkValidity()) {
                        input.classList.remove('is-invalid')
                        input.classList.add('is-valid')
                    } else {
                        input.classList.remove('is-valid')
                        input.classList.add('is-invalid')
                    }
                })
            })
        })
    })()
});