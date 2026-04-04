import { getOrders, updateOrderStatus } from '../api/orders.js';
import { showToast } from '../utils/toast.js';

/**
 * Отрисовка таблицы заказов.
 * Находит tbody с id="orders-body" и заполняет его данными.
 */
export async function renderOrdersTable() {
    const tbody = document.getElementById("orders-body");
    if (!tbody) {
        console.warn("Элемент #orders-body не найден. Пропускаем рендер.");
        return;
    }

    // Индикатор загрузки
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 20px;">Загрузка данных...</td></tr>';

    try {
        const orders = await getOrders();
        
        if (orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 20px; color: #666;">Заказов пока нет</td></tr>';
            return;
        }

        tbody.innerHTML = ""; // Очищаем лоадер

        orders.forEach(order => {
            const tr = document.createElement("tr");
            
            // Форматирование даты
            const dateObj = new Date(order.created_at);
            const dateStr = dateObj.toLocaleDateString("ru-RU", { day: '2-digit', month: '2-digit', year: 'numeric' });
            
            // Стилизация статуса
            let statusClass = "bg-gray-100 text-gray-800";
            const statusUpper = order.status.toUpperCase();
            
            if (statusUpper === "NEW") statusClass = "bg-blue-100 text-blue-800";
            else if (statusUpper === "PROCESSING") statusClass = "bg-yellow-100 text-yellow-800";
            else if (statusUpper === "DONE" || statusUpper === "COMPLETED") statusClass = "bg-green-100 text-green-800";
            else if (statusUpper === "CANCELLED") statusClass = "bg-red-100 text-red-800";

            // Формирование кнопок действий
            let actionsHtml = '';
            if (statusUpper === "NEW") {
                actionsHtml = `<button class="text-indigo-600 hover:text-indigo-900 font-medium btn-start-order" data-id="${order.id}">В работу</button>`;
            } else if (statusUpper === "PROCESSING") {
                actionsHtml = `<button class="text-green-600 hover:text-green-900 font-medium btn-complete-order" data-id="${order.id}">Готов</button>`;
            } else {
                actionsHtml = '<span class="text-gray-400">-</span>';
            }

            tr.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">#${order.id}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${order.client_name || `Клиент #${order.client_id}`}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${order.service_name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">${order.total_price} ₽</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}">
                        ${statusUpper}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${dateStr}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    ${actionsHtml}
                </td>
            `;

            tbody.appendChild(tr);
        });

        // Навешиваем обработчики событий на новые кнопки
        attachOrderEvents();

    } catch (error) {
        console.error(error);
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:red; padding: 20px;">Ошибка загрузки: ${error.message}</td></tr>`;
        showToast("Не удалось загрузить заказы", "error");
    }
}

/**
 * Навешивает обработчики кликов на кнопки управления заказами внутри таблицы.
 */
function attachOrderEvents() {
    // Кнопка "В работу"
    document.querySelectorAll(".btn-start-order").forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const id = e.target.getAttribute("data-id");
            if (confirm("Перевести этот заказ в работу?")) {
                try {
                    await updateOrderStatus(id, "PROCESSING");
                    showToast("Статус изменен на 'В работе'", "success");
                    renderOrdersTable(); // Перерисовка
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
            if (confirm("Подтвердить выполнение заказа? Будет начислен кэшбэк.")) {
                try {
                    await updateOrderStatus(id, "DONE");
                    showToast("Заказ выполнен! Кэшбэк начислен.", "success");
                    renderOrdersTable(); // Перерисовка
                } catch (err) {
                    showToast(err.message, "error");
                }
            }
        });
    });
}

// Делаем функцию доступной глобально для вызова из других модулей (например, router)
window.renderOrdersTable = renderOrdersTable;
