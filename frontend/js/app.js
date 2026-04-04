import { login, logout, getToken, getAuthHeaders } from './api/auth.js';
import { initRouter } from './router.js';
import { renderOrdersTable } from './components/orders_ui.js';
import { showToast } from './utils/toast.js';

// Элементы DOM
const loginOverlay = document.getElementById('login-overlay');
const crmApp = document.getElementById('crm-app');
const loginForm = document.getElementById('login-form');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');

/**
 * Проверка состояния авторизации при загрузке
 */
function checkAuth() {
    const token = getToken();

    if (!token) {
        // Нет токена -> Показываем вход
        loginOverlay.style.display = 'flex';
        crmApp.style.display = 'none';
    } else {
        // Токен есть -> Показываем приложение
        loginOverlay.style.display = 'none';
        crmApp.style.display = 'grid'; // Возвращаем grid layout
        
        // Инициализация приложения
        initApp();
    }
}

/**
 * Инициализация основного функционала CRM
 */
function initApp() {
    console.log("🚀 CRM App Initialized");
    
    // Запуск роутера (вкладки)
    initRouter();
    
    // Первоначальная загрузка данных (можно добавить загрузку дашборда здесь)
    // renderDashboard(); 
    
    showToast("Добро пожаловать в систему!", "success");
}

// Обработчик формы входа
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Сброс ошибок
    loginError.style.display = 'none';
    loginError.textContent = '';
    
    try {
        await login(username, password);
        checkAuth(); // Перепроверка и переключение интерфейса
    } catch (err) {
        loginError.textContent = err.message;
        loginError.style.display = 'block';
        showToast("Ошибка входа", "error");
    }
});

// Обработчик выхода
logoutBtn.addEventListener('click', () => {
    if(confirm("Вы уверены, что хотите выйти?")) {
        logout();
    }
});

// Запуск проверки при загрузке страницы
document.addEventListener('DOMContentLoaded', checkAuth);
