document.addEventListener("DOMContentLoaded", function() {
    // 1. Спочатку просто шукаємо елементи на сторінці
    const typeSelect = document.getElementById("id_employer_type");
    const companyBlock = document.getElementById("company-name-block");
    const companyInput = document.getElementById("id_name_company");

    // 2. ГОЛОВНИЙ ЗАХИСТ: Якщо хоча б одного з цих елементів немає на сторінці,
    // ми просто зупиняємо виконання скрипту. Помилок у консолі більше не буде!
    if (!typeSelect || !companyBlock || !companyInput) {
        return; 
    }

    // 3. Логіка перемикання полів (твій початковий правильний код)
    function toggleCompanyField() {
        if (typeSelect.value === "company") {
            companyBlock.style.style.display = "block";
        } else {
            companyBlock.style.style.display = "none";
            companyInput.value = ""; // Очищаємо інпут, якщо це приватна особа
        }
    }

    // 4. Перевірка відразу при завантаженні сторінки (щоб зберегти стан форми)
    toggleCompanyField();

    // 5. Подія на зміну вибору користувача
    typeSelect.addEventListener("change", toggleCompanyField);
});