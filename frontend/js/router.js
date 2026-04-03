/**
 * Инициализирует навигацию по вкладкам
 */
export function initRouter() {
    const tabs = document.querySelectorAll(".tab");
    const sections = document.querySelectorAll(".content-section");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            const targetId = tab.getAttribute("data-tab");

            // Убираем активный класс у всех вкладок и секций
            tabs.forEach(t => t.classList.remove("active"));
            sections.forEach(s => s.classList.remove("active"));

            // Добавляем активный класс текущей вкладке и секции
            tab.classList.add("active");
            
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add("active");
                
                // Если переключились на заказы - обновляем таблицу
                if (targetId === "orders-section" && typeof window.renderOrdersTable === 'function') {
                    window.renderOrdersTable();
                }
            }
        });
    });
}
