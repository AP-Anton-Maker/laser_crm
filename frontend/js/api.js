/**
 * Глобальный объект API для взаимодействия с бэкендом.
 * Автоматически подставляет JWT токен и обрабатывает 401 ошибки.
 */
window.API = (function() {
    const BASE_URL = '/api';

    // Функция для выполнения запросов
    async function request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        
        const headers = {
            ...options.headers
        };

        // Если это не FormData (как при логине), ставим application/json
        if (!(options.body instanceof URLSearchParams) && !(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
            if (options.body && typeof options.body === 'object') {
                options.body = JSON.stringify(options.body);
            }
        }

        // Подставляем токен авторизации
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method: options.method || 'GET',
            headers,
            body: options.body
        };

        try {
            const response = await fetch(`${BASE_URL}${endpoint}`, config);

            // Перехват 401 Unauthorized (токен истек или недействителен)
            if (response.status === 401) {
                console.error("Ошибка авторизации. Выполняем выход.");
                localStorage.removeItem('token');
                window.location.reload(); // Перезагрузка вызовет показ экрана логина
                throw new Error('Unauthorized');
            }

            // Обработка Blob (для скачивания ZIP архива бэкапа)
            if (options.isBlob) {
                if (!response.ok) throw new Error('Ошибка при скачивании файла');
                return await response.blob();
            }

            // Обработка обычного JSON
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Произошла ошибка при запросе');
            }

            return data;

        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    return {
        // Auth
        login: (username, password) => {
            const params = new URLSearchParams();
            params.append('username', username);
            params.append('password', password);
            return request('/auth/login', { method: 'POST', body: params });
        },
        getMe: () => request('/auth/me'),

        // Dashboard & Analytics
        getForecast: () => request('/forecast/'),

        // Orders
        getOrders: () => request('/orders/'),
        changeOrderStatus: (id, status) => request(`/orders/${id}/action/status?new_status=${status}`, { method: 'POST' }),

        // Clients
        getClients: () => request('/clients/'),

        // Chat
        getChatHistory: (clientId) => request(`/chat/${clientId}`),
        sendChatMessage: (clientId, text) => request(`/chat/${clientId}/send`, { method: 'POST', body: { text } }),

        // Calculator
        calculate: (params) => request('/calculator/calculate', { method: 'POST', body: params }),

        // Backup
        downloadBackup: () => request('/backup/download', { method: 'GET', isBlob: true })
    };
})();
