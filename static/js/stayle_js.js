    document.addEventListener("DOMContentLoaded", function() {
        const typeSelect = document.getElementById("id_employer_type");
        const companyBlock = document.getElementById("company-name-block");
        const companyInput = document.getElementById("id_name_company");

        function toggleCompanyField() {
            if (typeSelect.value === "company") {
                companyBlock.style.display = "block";
            } else {
                companyBlock.style.display = "none";
                companyInput.value = ""; // Очищаємо інпут, якщо це приватна особа
            }
        }

        // Перевірка при завантаженні сторінки
        toggleCompanyField();

        // Подія на зміну вибору користувача
        typeSelect.addEventListener("change", toggleCompanyField);
    });