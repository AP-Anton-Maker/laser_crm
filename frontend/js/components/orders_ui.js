import { getOrders, updateOrderStatus } from '../api/orders.js';
import { showToast } from '../utils/toast.js';

/**
 * Отрисовка таблицы заказов
 */
export async function renderOrdersTable() {
    const tbody = document.getElementById("orders-body");
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Загрузка...</td></tr>';

    try {
        const orders = await getOrders();
        
        if (orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Заказов пока нет</td></tr>';
            return;
        }

        tbody.innerHTML = ""; // Очищаем лоадер

        orders.forEach(order => {
            const tr = document.createElement("tr");
            
            // Форматирование даты
            const date = new Date(order.created_at).toLocaleDateString("ru-RU");
            
            // Определение цвета статуса
            let statusClass = "";
            if (order.status === "NEW") statusClass = "bg-blue-100 text-blue-800";
            else if (order.status === "PROCESSING") statusClass = "bg-yellow-100 text-yellow-800";
            else if (order.status === "COMPLETED") statusClass = "bg-green-100 text-green-800";
            else statusClass = "bg-gray-100 text-gray-800";

            tr.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#${order.id}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${order.client_name || 'Клиент #' + order.client_id}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${order.service_name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${order.total_price} ₽</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}">
                        ${order.status}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${date}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    ${order.status === 'NEW' ? `<button class="text-indigo-600 hover:text-indigo-900 mr-3 btn-start-order" data-id="${order.id}">В работу</button>` : ''}
                    ${order.status === 'PROCESSING' ? `<button class="text-green-600 hover:text-green-900 mr-3 btn-complete-order" data-id="${order.id}">Готов</button>` : ''}
                </td>
            `;

            tbody.appendChild(tr);
        });

        // Навешиваем обработчики событий на кнопки
        attachOrderEvents();

    } catch (error) {
        console.error(error);
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:red;">Ошибка: ${error.message}</td></tr>`;
        showToast("Не удалось загрузить заказы", "error");
    }
}

/**
 * Навешивает обработчики кликов на кнопки действий
 */
function attachOrderEvents() {
    // Кнопка "В работу"
    document.querySelectorAll(".btn-start-order").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const id = e.target.getAttribute("data-id");
            if (confirm("Перевести заказ в работу?")) {
                try {
                    await updateOrderStatus(id, "PROCESSING");
                    showToast("Статус обновлен", "success");
                    renderOrdersTable();
                } catch (err) {
                    showToast(err.message, "error");
                }
            }
        });
    });

    // Кнопка "Готов"
    document.querySelectorAll(".btn-complete-order").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const id = e.target.getAttribute("data-id");
            if (confirm("Подтвердить выполнение заказа?")) {
                try {
                    await updateOrderStatus(id, "COMPLETED");
                    showToast("Заказ выполнен!", "success");
                    renderOrdersTable();
                } catch (err) {
                    showToast(err.message, "error");
                }
            }
        });
    });
}

// Делаем функцию доступной глобально для вызова из router.js
window.renderOrdersTable = renderOrdersTable;
