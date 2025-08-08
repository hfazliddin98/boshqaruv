$(document).ready(function () {
    // Sidebar toggle functionality
    $('#sidebarToggle').click(function () {
        $('#sidebar').toggleClass('collapsed');
        $('#mainContent').toggleClass('expanded');

        // For mobile view
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

    // Card hover effects
    $('.card').hover(
        function() {
            $(this).addClass('shadow-lg');
        }, 
        function() {
            $(this).removeClass('shadow-lg');
        }
    );

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Initialize tooltips if any
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
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

// Sidebar boshqaruvi
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

    // Form field class additions for better styling
    $('.form-control, .form-select').addClass('form-control');
});

// File management functionality
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('files');
    const fileDropArea = document.getElementById('fileDropArea');
    const fileList = document.getElementById('fileList');
    let allFiles = [];

    if (!fileInput || !fileDropArea || !fileList) return;

    // File selection handler
    fileInput.addEventListener('change', function (e) {
        handleFiles(this.files);
    });

    // Drag and drop functionality
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

    function handleFiles(files) {
        Array.from(files).forEach(file => {
            // File size validation (10MB)
            if (file.size > 10 * 1024 * 1024) {
                showAlert(`Fayl hajmi juda katta: ${file.name} (Maksimum 10MB)`, 'danger');
                return;
            }

            // File type validation
            const validTypes = [
                'image/jpeg', 
                'image/png', 
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            ];
            
            if (!validTypes.includes(file.type)) {
                showAlert(`Fayl formati qo'llab-quvvatlanmaydi: ${file.name}`, 'warning');
                return;
            }

            // Prevent duplicate files
            if (!allFiles.some(f => f.name === file.name && f.size === file.size)) {
                allFiles.push(file);
                showAlert(`Fayl qo'shildi: ${file.name}`, 'success');
            } else {
                showAlert(`Fayl allaqachon mavjud: ${file.name}`, 'info');
            }
        });
        renderFileList();
    }

    function renderFileList() {
        fileList.innerHTML = '';

        if (allFiles.length > 0) {
            const listGroup = document.createElement('div');
            listGroup.className = 'list-group';

            allFiles.forEach((file, index) => {
                const item = document.createElement('div');
                item.className = 'list-group-item d-flex justify-content-between align-items-center';

                // File type icon
                let fileIcon = getFileIcon(file.type);

                item.innerHTML = `
                    <div class="d-flex align-items-center flex-grow-1">
                        <i class="fas ${fileIcon} me-3 fs-4"></i>
                        <div class="text-truncate me-3">
                            <div class="fw-bold text-truncate">${file.name}</div>
                            <small class="text-muted">${formatSize(file.size)} • ${getFileTypeDisplay(file.type)}</small>
                        </div>
                    </div>
                    <button type="button" 
                            class="btn btn-sm btn-outline-danger" 
                            onclick="removeFile(${index})"
                            title="Faylni o'chirish">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                `;
                listGroup.appendChild(item);
            });

            fileList.appendChild(listGroup);
            updateFileInput();

            // Show file count info
            const infoDiv = document.createElement('div');
            infoDiv.className = 'alert alert-info mt-2';
            infoDiv.innerHTML = `
                <i class="fas fa-info-circle me-2"></i>
                Jami ${allFiles.length} ta fayl tanlandi
            `;
            fileList.appendChild(infoDiv);
        }
    }

    function getFileIcon(fileType) {
        if (fileType.startsWith('image/')) return 'fa-file-image text-info';
        if (fileType === 'application/pdf') return 'fa-file-pdf text-danger';
        if (fileType.includes('wordprocessingml')) return 'fa-file-word text-primary';
        if (fileType.includes('spreadsheetml')) return 'fa-file-excel text-success';
        return 'fa-file text-secondary';
    }

    function getFileTypeDisplay(fileType) {
        const typeMap = {
            'image/jpeg': 'JPEG rasm',
            'image/png': 'PNG rasm',
            'application/pdf': 'PDF hujjat',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word hujjat',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Excel jadval'
        };
        return typeMap[fileType] || 'Noma\'lum format';
    }

    window.removeFile = function (index) {
        const removedFile = allFiles[index];
        allFiles.splice(index, 1);
        renderFileList();
        showAlert(`Fayl o'chirildi: ${removedFile.name}`, 'warning');
    };

    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        allFiles.forEach(file => dataTransfer.items.add(file));
        fileInput.files = dataTransfer.files;
    }

    function formatSize(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Byte';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
    }

    function showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => {
            if (alert.classList.contains(`alert-${type}`)) {
                alert.remove();
            }
        });

        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show mt-2`;
        alert.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        fileList.prepend(alert);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    }
});

// Form validation
(function () {
    'use strict';

    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Show validation error alert
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger alert-dismissible fade show';
                alert.innerHTML = `
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Iltimos, barcha majburiy maydonlarni to'ldiring!
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                form.prepend(alert);
                
                // Scroll to first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        }, false);

        // Real-time validation
        form.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('input', function () {
                if (input.checkValidity()) {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                } else {
                    input.classList.remove('is-valid');
                    input.classList.add('is-invalid');
                }
            });
        });

        // Form reset handler
        form.addEventListener('reset', function () {
            // Clear file list
            if (window.allFiles) {
                window.allFiles = [];
                const fileList = document.getElementById('fileList');
                if (fileList) fileList.innerHTML = '';
            }
            
            // Remove validation classes
            form.classList.remove('was-validated');
            form.querySelectorAll('.is-valid, .is-invalid').forEach(field => {
                field.classList.remove('is-valid', 'is-invalid');
            });
            
            // Remove alerts
            form.querySelectorAll('.alert').forEach(alert => alert.remove());
        });
    });
})();

document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus on cancel button for better UX
    const cancelButton = document.querySelector('.btn-cancel');
    if (cancelButton) {
        cancelButton.focus();
    }

    // Add confirmation dialog for delete action
    const deleteButton = document.querySelector('.btn-delete');
    if (deleteButton) {
        deleteButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show confirmation modal or use browser confirm
            const confirmDelete = confirm('Bu amalni qaytarib bo\'lmaydi. Haqiqatan ham o\'chirmoqchimisiz?');
            
            if (confirmDelete) {
                // Add loading state
                this.classList.add('loading');
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> O\'chirilmoqda...';
                
                // Proceed with deletion
                window.location.href = this.href;
            }
        });
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // ESC key cancels the action
            window.location.href = cancelButton.href;
        } else if (e.key === 'Enter' && e.target.classList.contains('btn-cancel')) {
            // Enter on cancel button
            window.location.href = e.target.href;
        }
    });

    // Add smooth animations on load
    const container = document.querySelector('.confirmation-container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            container.style.transition = 'all 0.6s ease-out';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);
    }

    // Auto-redirect timer (optional - can be removed)
    let autoRedirectTimer;
    const startAutoRedirect = () => {
        let seconds = 30;
        const timerElement = document.createElement('div');
        timerElement.className = 'text-center mt-3 text-muted small';
        timerElement.innerHTML = `Bu sahifa ${seconds} soniyadan so'ng avtomatik yopiladi`;
        
        const actionButtons = document.querySelector('.action-buttons');
        if (actionButtons) {
            actionButtons.parentNode.insertBefore(timerElement, actionButtons.nextSibling);
        }

        autoRedirectTimer = setInterval(() => {
            seconds--;
            if (seconds <= 0) {
                window.location.href = cancelButton.href;
            } else {
                timerElement.innerHTML = `Bu sahifa ${seconds} soniyadan so'ng avtomatik yopiladi`;
            }
        }, 1000);
    };

    // Start auto-redirect timer after 5 seconds of inactivity
    let activityTimer = setTimeout(startAutoRedirect, 5000);

    // Clear timers on user activity
    ['click', 'keydown', 'mousemove'].forEach(event => {
        document.addEventListener(event, () => {
            if (activityTimer) {
                clearTimeout(activityTimer);
                activityTimer = null;
            }
            if (autoRedirectTimer) {
                clearInterval(autoRedirectTimer);
                const timerElement = document.querySelector('.text-center.mt-3.text-muted.small');
                if (timerElement) {
                    timerElement.remove();
                }
            }
        }, { once: true });
    });
});

// Add smooth page transitions
window.addEventListener('beforeunload', function() {
    document.body.style.opacity = '0.5';
    document.body.style.transition = 'opacity 0.3s ease-out';
});

// Handle back button
window.addEventListener('popstate', function() {
    window.location.href = document.querySelector('.btn-cancel').href;
});