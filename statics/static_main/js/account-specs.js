document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('accountSpecsForm');
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    const addAddressBtn = document.querySelector('.btn-add-address');

    // Fetch provinces from API
    async function fetchProvinces() {
        try {
            const response = await fetch('https://iranplacesapi.liara.run/api/provinces');
            const provinces = await response.json();
            
            // Clear existing options except the first one
            provinceSelect.innerHTML = '<option value="">انتخاب استان</option>';
            
            // Add provinces to select
            provinces.forEach(province => {
                const option = document.createElement('option');
                option.value = province.id;
                option.textContent = province.name;
                provinceSelect.appendChild(option);
            });
        } catch (error) {
            showError('خطا در دریافت لیست استان‌ها');
            console.error('Error fetching provinces:', error);
        }
    }

    // Fetch cities for a province
    async function fetchCities(provinceId) {
        try {
            const response = await fetch(`https://iranplacesapi.liara.run/api/provinces/id/${provinceId}/cities`);
            const cities = await response.json();
            
            // Clear existing options except the first one
            citySelect.innerHTML = '<option value="">انتخاب شهر</option>';
            
            // Add cities to select
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.id;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        } catch (error) {
            showError('خطا در دریافت لیست شهرها');
            console.error('Error fetching cities:', error);
        }
    }

    // Handle province change
    provinceSelect.addEventListener('change', function() {
        const selectedProvince = this.value;
        if (selectedProvince) {
            fetchCities(selectedProvince);
        } else {
            citySelect.innerHTML = '<option value="">انتخاب شهر</option>';
        }
    });

    // Add new address
    addAddressBtn.addEventListener('click', function() {
        const addressCard = document.querySelector('.address-card').cloneNode(true);
        const addressHeader = addressCard.querySelector('.address-header h4');
        addressHeader.textContent = `آدرس ${document.querySelectorAll('.address-card').length + 1}`;
        
        // Clear form fields
        addressCard.querySelectorAll('input, select, textarea').forEach(field => {
            field.value = '';
        });

        // Reattach event listeners for the new province select
        const newProvinceSelect = addressCard.querySelector('#province');
        newProvinceSelect.addEventListener('change', function() {
            const selectedProvince = this.value;
            const newCitySelect = addressCard.querySelector('#city');
            if (selectedProvince) {
                fetchCities(selectedProvince);
            } else {
                newCitySelect.innerHTML = '<option value="">انتخاب شهر</option>';
            }
        });

        this.parentNode.insertBefore(addressCard, this);
    });

    // Form validation
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate national code
        const nationalCode = document.getElementById('nationalCode').value;
        if (!validateNationalCode(nationalCode)) {
            showError('کد ملی نامعتبر است');
            return;
        }

        // Validate mobile number
        const mobile = document.getElementById('mobile').value;
        if (!validateMobile(mobile)) {
            showError('شماره موبایل نامعتبر است');
            return;
        }

        // Validate postal code
        const postalCode = document.getElementById('postalCode').value;
        if (!validatePostalCode(postalCode)) {
            showError('کد پستی نامعتبر است');
            return;
        }

        // Validate password change
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (newPassword && !currentPassword) {
            showError('برای تغییر رمز عبور، رمز فعلی را وارد کنید');
            return;
        }

        if (newPassword && newPassword !== confirmPassword) {
            showError('رمز عبور جدید و تکرار آن مطابقت ندارند');
            return;
        }

        // If all validations pass, submit the form
        submitForm();
    });

    // Validation functions
    function validateNationalCode(code) {
        if (code.length !== 10) return false;
        const digits = code.split('').map(Number);
        const lastDigit = digits.pop();
        const sum = digits.reduce((acc, digit, index) => acc + digit * (10 - index), 0);
        const remainder = sum % 11;
        return remainder < 2 ? lastDigit === remainder : lastDigit === 11 - remainder;
    }

    function validateMobile(mobile) {
        return /^09[0-9]{9}$/.test(mobile);
    }

    function validatePostalCode(code) {
        return /^[0-9]{10}$/.test(code);
    }

    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#ff4757';
        errorDiv.style.padding = '1rem';
        errorDiv.style.marginTop = '1rem';
        errorDiv.style.backgroundColor = '#fff3f3';
        errorDiv.style.borderRadius = '8px';
        
        const existingError = form.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        form.insertBefore(errorDiv, form.firstChild);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    // Submit form
    function submitForm() {
        const formData = new FormData(form);
        const submitButton = form.querySelector('.btn-save');
        
        // Show loading state
        submitButton.disabled = true;
        submitButton.textContent = 'در حال ذخیره...';
        
        // Simulate API call
        setTimeout(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'ذخیره تغییرات';
            
            // Show success message
            const successDiv = document.createElement('div');
            successDiv.className = 'success-message';
            successDiv.textContent = 'اطلاعات با موفقیت ذخیره شد';
            successDiv.style.color = '#2ed573';
            successDiv.style.padding = '1rem';
            successDiv.style.marginTop = '1rem';
            successDiv.style.backgroundColor = '#f0fff4';
            successDiv.style.borderRadius = '8px';
            
            form.insertBefore(successDiv, form.firstChild);
            
            setTimeout(() => {
                successDiv.remove();
            }, 5000);
        }, 2000);
    }

    // Initialize provinces on page load
    fetchProvinces();
}); 