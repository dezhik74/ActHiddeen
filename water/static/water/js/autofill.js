function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = (hash << 5) - hash + char;
        hash = hash & hash; // Преобразуем в 32-битное целое
    }
    return Math.abs(hash);
}

function generate5DigitHash(...args) {
    const input = args.join('').toLowerCase();
    const hash = simpleHash(input);
    return String(hash % 100000).padStart(5, '0');
}

function generate4DigitHash(...args) {
    const input = args.join('').toLowerCase();
    const hash = simpleHash(input);
    return String(hash % 10000).padStart(4, '0');
}

const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

// Вычисление даты минус N рабочих дней (пропускаем субботу и воскресенье)
function subtractWorkingDays(dateStr, days) {
    // dateStr в формате "дд.мм.гггг" → преобразуем в объект Date
    const parts = dateStr.split('.');
    if (parts.length !== 3) {
        return dateStr; // если формат неверный — возвращаем как есть
    }
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1; // месяцы в JS с 0
    const year = parseInt(parts[2], 10);

    const result = new Date(year, month, day);
    if (isNaN(result.getTime())) {
        return dateStr; // некорректная дата
    }

    let subtracted = 0;
    while (subtracted < days) {
        result.setDate(result.getDate() - 1);
        const dayOfWeek = result.getDay();
        if (dayOfWeek !== 0 && dayOfWeek !== 6) { // не воскресенье и не суббота
            subtracted++;
        }
    }

    // Форматируем обратно в дд.мм.гггг
    const dd = String(result.getDate()).padStart(2, '0');
    const mm = String(result.getMonth() + 1).padStart(2, '0');
    const yyyy = result.getFullYear();

    return `${dd}.${mm}.${yyyy}`;
}

document.addEventListener('DOMContentLoaded', function () {
    const autofillBtn = document.getElementById('autofill-btn');
    if (!autofillBtn) return;

    autofillBtn.addEventListener('click', function (e) {
        e.preventDefault();

        // Получаем обязательные поля
        const conclusionDateInput = document.querySelector('input[name="conclusion_date"]');
        const customerInput = document.querySelector('input[name="customer"]');
        const addressInput = document.querySelector('input[name="address"]');

        if (!conclusionDateInput || !customerInput || !addressInput) {
            alert('Ошибка: не найдены обязательные поля формы');
            return;
        }

        const conclusionDate = conclusionDateInput.value.trim();
        const customer = customerInput.value.trim();
        const address = addressInput.value.trim();

        if (!conclusionDate || !customer || !address) {
            // Создаём сообщение в стиле Django messages
            const messagesContainer = document.getElementById('messages-container') ||
                document.querySelector('.container.mt-3');

            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show';
            alertDiv.role = 'alert';
            alertDiv.innerHTML = `
                <i class="fas fa-exclamation-triangle me-2"></i>
                Для автозаполнения обязательно заполните: Дата заключения, Заказчик и Адрес
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            // Вставляем в начало контейнера сообщений или в начало формы
            const container = messagesContainer || document.querySelector('.container.py-4') || document.body;
            container.prepend(alertDiv);

            // Автоудаление через 3 сек
            setTimeout(() => {
                if (alertDiv.isConnected) {
                    alertDiv.classList.remove('show');
                    setTimeout(() => alertDiv.remove(), 300);
                }
            }, 3000);

            return;
        }

        // Генерируем базовый хэш
        const baseHash5 = generate5DigitHash(customer, conclusionDate, address);
        const baseHash4 = generate4DigitHash(conclusionDate, customer, address);

        // Даты

        const actDate = subtractWorkingDays(conclusionDate, 15);
        const chemistryDate = subtractWorkingDays(conclusionDate, 4);
        const bioDate = subtractWorkingDays(conclusionDate, 3);
        const bioBeginDate = subtractWorkingDays(conclusionDate, 10);
        const bioEndDate = subtractWorkingDays(conclusionDate, 8);

        // Константы показателей
        const phArray = ["6,4  ±  0,2", "7,1  ±  0,2", "7,0  ±  0,2", "6,7  ±  0,2", "6,9  ±  0,2",
                                "7,4  ±  0,2", "7,5  ±  0,2", "7,7  ±  0,2", "6,5  ±  0,2", "7,2  ±  0,2",
                                "6,6  ±  0,2", "6,9  ±  0,2", "7,6  ±  0,2", "6,8  ±  0,2"]
        const feArray = ["0,14  ±  0,02", "0,13  ±  0,02", "0,12  ±  0,02", "0,16  ±  0,03",
                                "0,18  ±  0,04", "0,20  ±  0,04", "0,27  ±  0,05", "0,26  ±  0,04",
                                "0,09  ±  0,02", "0,12  ±  0,02", "0,11  ±  0,02", "0,17  ±  0,03",
                                "0,24  ±  0,05", "0,19  ±  0,03", "0,07  ±  0,01"]
        const turbArray = ["2,0  ±  0,4", "2,2  ±  0,4", "2,5  ±  0,4", "2,5  ±  0,5", "2,4  ±  0,5",
                                "2,6  ±  0,5", "1,4  ±  0,3", "2,3  ±  0,5", "2,2  ±  0,4", "2,1  ±  0,4",
                                "1,6  ±  0,3", "1,9  ±  0,4"]
        const chromaArray = ["5  ±  2", "15  ±  3", "4  ±  2", "6  ±  2", "3  ±  1", "7  ±  3", "17  ±  3",
                                "16  ±  3", "14  ±  3", "13  ±  3", "10  ±  2", "9  ±  4"]
        const rigArray = ["1,1  ±  0,2", "3,2  ±  0,5", "1,5  ±  0,2", "1,6  ±  0,2", "2,0  ±  0,3",
                                "1,7  ±  0,3", "3,3  ±  0,5", "2,2  ±  0,3", "2,4  ±  0,4", "3,6  ±  0,5",
                                "2,6  ±  0,4", "2,3  ±  0,3", "1,0  ±  0,2", "0,9  ±  0,1"]
        const oxArray = ["1,7  ±  0,3", "0,8  ±  0,2", "1,4  ±  0,3", "1,3  ±  0,3", "1,8  ±  0,4", "2,2  ±  0,2",
                                "1,6  ±  0,3", "1,9  ±  0,4", "2,4  ±  0,2", "1,0  ± 0,2",  "2,7  ±  0,3", "2,6  ±  0,3"]

        // Заполняем поля (даже если они не пустые)
        const setValueIfEmpty = (selector, value) => {
            const el = document.querySelector(selector);
            // if (el && !el.value.trim()) {
                el.value = value;
            // }
        };

        // Акт
        setValueIfEmpty('input[name="act_number"]', `${baseHash5}-3`);
        setValueIfEmpty('input[name="act_date"]', actDate);
        setValueIfEmpty('input[name="hvs_probe_number"]', `${baseHash5}.12-3-1`);
        setValueIfEmpty('input[name="gvs_probe_number"]', `${baseHash5}.12-3-2`);
        setValueIfEmpty('input[name="probe_date"]', actDate);

        // Химия
        setValueIfEmpty('input[name="chemistry_number"]', `${baseHash5}.12-3`);
        setValueIfEmpty('input[name="chemistry_date"]', chemistryDate);
        setValueIfEmpty('input[name="chemistry_order_number"]', `${baseHash5}-3`);
        setValueIfEmpty('input[name="chemistry_order_date"]', actDate);

        // Биология
        setValueIfEmpty('input[name="bio_number"]', `${generate4DigitHash(address, customer, actDate)}.2026`);
        setValueIfEmpty('input[name="bio_date"]', bioDate);
        setValueIfEmpty('input[name="hvs_bio_code"]', baseHash4);
        setValueIfEmpty('input[name="gvs_bio_code"]', String(parseInt(baseHash4) + 1).padStart(4, '0'));
        setValueIfEmpty('input[name="hvs_bio_referral"]', `${baseHash5}-3`);
        setValueIfEmpty('input[name="gvs_bio_referral"]', `${baseHash5}-3`);
        setValueIfEmpty('input[name="bio_begin_date"]', bioBeginDate);
        setValueIfEmpty('input[name="bio_end_date"]', bioEndDate);

        // Показатели хим анализа
        setValueIfEmpty('input[name="hvs_ph"]', getRandomElement(phArray));
        setValueIfEmpty('input[name="hvs_fe"]', getRandomElement(feArray));
        setValueIfEmpty('input[name="hvs_turb"]', getRandomElement(turbArray));
        setValueIfEmpty('input[name="hvs_chroma"]', getRandomElement(chromaArray));
        setValueIfEmpty('input[name="hvs_rig"]', getRandomElement(rigArray));
        setValueIfEmpty('input[name="hvs_ox"]', getRandomElement(oxArray));
        setValueIfEmpty('input[name="gvs_ph"]', getRandomElement(phArray));
        setValueIfEmpty('input[name="gvs_fe"]', getRandomElement(feArray));
        setValueIfEmpty('input[name="gvs_turb"]', getRandomElement(turbArray));
        setValueIfEmpty('input[name="gvs_chroma"]', getRandomElement(chromaArray));
        setValueIfEmpty('input[name="gvs_rig"]', getRandomElement(rigArray));
        setValueIfEmpty('input[name="gvs_ox"]', getRandomElement(oxArray));

        // Успешное сообщение
        const successAlert = document.createElement('div');
        successAlert.className = 'alert alert-success alert-dismissible fade show';
        successAlert.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            Форма успешно автозаполнена!
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        const container = document.querySelector('.container.py-4') || document.body;
        container.prepend(successAlert);

        setTimeout(() => {
            if (successAlert.isConnected) {
                successAlert.classList.remove('show');
                setTimeout(() => successAlert.remove(), 300);
            }
        }, 4000);
    });
});