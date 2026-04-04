/**
 * Единый клиент для API запросов.
 * Автоматически подставляет JWT токен и обрабатывает ошибки авторизации.
 */

const API_BASE_URL = "http://localhost:8000/api";

/**
 * Получение токена из localStorage
 */
function getToken() {
    return localStorage.getItem('crm_token');
}

/**
 * Базовая функция fetch с обработкой токена и ошибок
 * @param {string} endpoint - Эндпоинт (например, '/orders/')
 * @param {Object} options - Опции fetch (method, body и т.д.)
 */
async function request(endpoint, options = {}) {
    const token = getToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

        // Если токен протух или неверен (401)
        if (response.status === 401) {
            localStorage.removeItem('crm_token');
            window.location.reload();
            throw new Error('Unauthorized');
        }

        // Обработка ошибок сервера
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Ошибка HTTP: ${response.status}`);
        }

        // Если ответ пустой (например, 204 No Content)
        if (response.status === 204) {
            return null;
        }

        return await response.json();

    } catch (error) {
        console.error(`API Request Error (${endpoint}):`, error);
        throw error;
    }
}

// --- Auth Methods ---
export async function login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
    });

    if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Неверный логин или пароль");
    }

    const data = await response.json();
    localStorage.setItem('crm_token', data.access_token);
    return data;
}

export function logout() {
    localStorage.removeItem('crm_token');
    window.location.reload();
}

// --- Orders Methods ---
export async function getOrders(statusFilter = null) {
    let url = '/orders/';
    if (statusFilter) url += `?status=${statusFilter}`;
    return request(url);
}

export async function createOrder(orderData) {
    return request('/order/create', {
        method: 'POST',
        body: JSON.stringify(orderData)
    });
}

export async function updateOrderStatus(orderId, status) {
    return request('/order/status', {
        method: 'POST',
        body: JSON.stringify({ order_id: orderId, status })
    });
}

// --- System & Settings Methods ---
export async function getSystemSettings() {
    return request('/system/settings');
}

export async function updateSystemSettings(data) {
    return request('/system/settings', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

// --- Clients Methods ---
export async function getClients(segment = null) {
    let url = '/clients';
    if (segment) url += `?segment=${segment}`;
    return request(url);
}

export async function getCashbackHistory(clientId) {
    return request(`/cashback/history/${clientId}`);
}

// --- Inventory Methods ---
export async function getInventory() {
    return request('/inventory/');
}

export async function getLowStock() {
    return request('/inventory/low-stock');
}

// --- Analytics Methods ---
export async function getAnalyticsSummary() {
    return request('/analytics/summary');
}

export async function getAnalyticsServices() {
    return request('/analytics/services');
}

export async function getAnalyticsSegments() {
    return request('/analytics/segments');
}

export async function getAiPredictions() {
    return request('/ai/predictions');
}

// --- Chat Methods ---
export async function getChatHistory(vkId) {
    return request(`/chat/history?vk_id=${vkId}`);
}

export async function sendChatMessage(vkId, message) {
    return request('/chat/send', {
        method: 'POST',
        body: JSON.stringify({ vk_id: vkId, message })
    });
}
