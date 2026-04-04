import { getSettings, updateSettings } from '../api/system.js';
import { showToast } from '../utils/toast.js';

/**
 * Проверка режима отпуска и отображение предупреждения на дашборде
 */
export async function checkVacationMode() {
    const alertBox = document.getElementById("vacation-alert-box");
    if (!alertBox) return;

    try {
        const settings = await getSettings();
        
        if (settings.is_vacation_mode) {
            alertBox.style.display = 'block';
            let text = "⚠️ ВНИМАНИЕ: Включен режим отпуска!";
            if (settings.vacation_end_date) {
                text += ` (до ${settings.vacation_end_date})`;
            }
            alertBox.textContent = text;
        } else {
            alertBox.style.display = 'none';
        }
    } catch (error) {
        console.error("Не удалось проверить режим отпуска", error);
    }
}

/**
 * Рендеринг формы настроек отпуска (для модального окна или секции настроек)
 * @param {string} containerId - ID элемента, куда рендерить форму
 */
export function renderVacationSettings(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="card">
            <h3>🌴 Режим отпуска</h3>
            <p class="text-sm text-gray-500 mb-4">Включите этот режим, чтобы VK-бот автоматически отвечал клиентам.</p>
            
            <form id="vacation-form">
                <div class="form-group">
                    <label class="flex items-center space-x-3 cursor-pointer">
                        <input type="checkbox" id="vacation-toggle" class="w-5 h-5 text-blue-600 rounded">
                        <span class="font-medium text-lg">Я в отпуске</span>
                    </label>
                </div>

                <div class="form-group">
                    <label for="vacation-date">Дата возвращения</label>
                    <input type="text" id="vacation-date" placeholder="Например: 25.08.2024">
                </div>

                <div class="form-group">
                    <label for="vacation-msg">Текст автоответа</label>
                    <textarea id="vacation-msg" rows="4" placeholder="Сообщение, которое увидят клиенты в ВК..."></textarea>
                </div>

                <button type="submit" class="btn btn-primary">Сохранить настройки</button>
            </form>
        </div>
    `;

    // Загрузка текущих значений
    loadSettingsIntoForm();

    // Обработчик сохранения
    document.getElementById('vacation-form').addEventListener('submit', handleSaveSettings);
}

async function loadSettingsIntoForm() {
    try {
        const settings = await getSettings();
        
        const toggle = document.getElementById('vacation-toggle');
        const dateInput = document.getElementById('vacation-date');
        const msgInput = document.getElementById('vacation-msg');

        if (toggle) toggle.checked = settings.is_vacation_mode;
        if (dateInput) dateInput.value = settings.vacation_end_date || '';
        if (msgInput) msgInput.value = settings.vacation_message || '';
        
    } catch (error) {
        console.error("Ошибка загрузки настроек", error);
    }
}

async function handleSaveSettings(e) {
    e.preventDefault();
    
    const data = {
        is_vacation_mode: document.getElementById('vacation-toggle').checked,
        vacation_end_date: document.getElementById('vacation-date').value,
        vacation_message: document.getElementById('vacation-msg').value
    };

    try {
        await updateSettings(data);
        showToast("Настройки отпуска сохранены!", "success");
        checkVacationMode(); // Обновить плашку на дашборде
    } catch (err) {
        showToast(err.message, "error");
    }
}
