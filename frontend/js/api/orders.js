const API_BASE_URL = "http://localhost:8000/api";

/**
 * Получение списка заказов
 * @param {string} statusFilter - Фильтр по статусу ('all' или конкретный статус)
 * @returns {Promise<Array>}
 */
export async function getOrders(statusFilter = 'all') {
    let url = `${API_BASE_URL}/orders/`;
    if (statusFilter !== 'all') {
        url += `?status=${statusFilter}`;
    }

    const response = await fetch(url, {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });

    if (!response.ok) {
        throw new Error("Ошибка при получении заказов");
    }

    return await response.json();
}

/**
 * Создание нового заказа
 * @param {Object} orderData - Данные заказа
 * @returns {Promise<Object>}
 */
export async function createOrder(orderData) {
    const response = await fetch(`${API_BASE_URL}/order/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderData)
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Ошибка при создании заказа");
    }

    return data;
}

/**
 * Обновление статуса заказа
 * @param {number} orderId - ID заказа
 * @param {string} status - Новый статус
 * @returns {Promise<Object>}
 */
export async function updateOrderStatus(orderId, status) {
    const response = await fetch(`${API_BASE_URL}/order/status`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: orderId, status })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Ошибка при обновлении статуса");
    }

    return data;
}
