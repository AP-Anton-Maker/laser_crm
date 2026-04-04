import { getSystemSettings, updateSystemSettings } from '../api/api_client.js';
import { showToast } from '../utils/toast.js';

/**
 * Проверка режима отпуска и отображение алерта
 */
export async function checkVacationMode() {
    const alertBox = document.getElementById("vacation-alert-box");
    if (!alertBox) return;

    try {
        const settings = await getSystemSettings();
        
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
        console.error("Ошибка проверки режима отпуска", error);
    }
}

/**
 * Рендеринг формы настроек отпуска
 */
export function renderVacationSettings(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <div class="card">
            <h3>🌴 Режим отпуска</h3>
            <p class="text-muted mb-4">Включите этот режим, чтобы VK-бот автоматически отвечал клиентам.</p>
            
            <form id="vacation-form">
                <div class="form-group">
                    <label class="flex items-center space-x-3" style="display:flex; align-items:center; gap:10px; cursor:pointer;">
                        <input type="checkbox" id="vacation-toggle" style="width:auto;">
                        <span style="font-weight:600; font-size:1.1rem;">Я в отпуске</span>
                    </label>
                </div>

                <div class="form-group">
                    <label for="vacation-date">Дата возвращения</label>
                    <input type="text" id="vacation-date" placeholder="Например: 25.08.2024">
                </div>

                <div class="form-group">
                    <label for="vacation-msg">Текст автоответа</label>
                    <textarea id="vacation-msg" rows="4" placeholder="Сообщение для клиентов..."></textarea>
                </div>

                <button type="submit" class="btn btn-primary">Сохранить настройки</button>
            </form>
        </div>
    `;

    loadSettingsIntoForm();
    document.getElementById('vacation-form').addEventListener('submit', handleSaveSettings);
}

async function loadSettingsIntoForm() {
    try {
        const settings = await getSystemSettings();
        
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
        await updateSystemSettings(data);
        showToast("Настройки сохранены!", "success");
        checkVacationMode();
    } catch (err) {
        showToast(err.message, "error");
    }
}
