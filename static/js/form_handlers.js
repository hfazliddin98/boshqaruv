// HTML formasidagi tanlangan qiymatlarni olish

// 1. Select field dan qiymat olish
function getSelectedRole() {
    const roleSelect = document.getElementById('id_role');
    const selectedValue = roleSelect.value;
    const selectedText = roleSelect.options[roleSelect.selectedIndex].text;
    
    console.log('Tanlangan rol qiymati:', selectedValue);
    console.log('Tanlangan rol matni:', selectedText);
    return selectedValue;
}

// 2. Checkbox holatini tekshirish
function isActiveChecked() {
    const checkbox = document.getElementById('id_is_active');
    return checkbox.checked;
}

// 3. Barcha form ma'lumotlarini olish
function getAllFormData() {
    const form = document.getElementById('user-form'); // form ID si
    const formData = new FormData(form);
    
    // FormData dan oddiy object ga o'tkazish
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    console.log('Barcha form ma\'lumotlari:', data);
    return data;
}

// 4. Select o'zgarishini kuzatish
document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('id_role');
    if (roleSelect) {
        roleSelect.addEventListener('change', function() {
            const selectedRole = this.value;
            console.log('Yangi rol tanlandi:', selectedRole);
            
            // Strukturani avtomatik yangilash
            updateStrukturaOptions(selectedRole);
        });
    }
});

// 5. Struktura variantlarini yangilash
function updateStrukturaOptions(selectedRole) {
    const strukturaSelect = document.getElementById('id_struktura');
    
    // AJAX orqali yangi variantlarni olish
    fetch(`/get_struktura_by_role/${selectedRole}/`)
        .then(response => response.json())
        .then(data => {
            // Eski variantlarni tozalash
            strukturaSelect.innerHTML = '<option value="">---------</option>';
            
            // Yangi variantlarni qo'shish
            data.strukturalar.forEach(struktura => {
                const option = new Option(struktura.name, struktura.id);
                strukturaSelect.add(option);
            });
        })
        .catch(error => {
            console.error('Xatolik:', error);
        });
}

// 6. Form yuborishdan oldin validatsiya
function validateForm() {
    const role = document.getElementById('id_role').value;
    const username = document.getElementById('id_username').value;
    
    if (!role) {
        alert('Iltimos, rol tanlang!');
        return false;
    }
    
    if (!username.trim()) {
        alert('Iltimos, foydalanuvchi nomini kiriting!');
        return false;
    }
    
    return true;
}

// 7. Multiple select uchun
function getSelectedMultipleValues(selectId) {
    const select = document.getElementById(selectId);
    const selectedValues = [];
    
    for (let option of select.options) {
        if (option.selected) {
            selectedValues.push(option.value);
        }
    }
    
    return selectedValues;
}
