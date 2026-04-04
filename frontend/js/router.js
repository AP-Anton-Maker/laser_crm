import { renderOrdersTable } from './components/orders_ui.js';
// Можно импортировать другие рендеры, если они вынесены в отдельные файлы

export function initRouter() {
    const tabs = document.querySelectorAll(".tab");
    const sections = document.querySelectorAll(".content-section");
    const pageTitle = document.getElementById("page-title");

    tabs.forEach(tab => {
        tab.addEventListener("click", (e) => {
            e.preventDefault();
            
            const targetId = tab.getAttribute("data-tab");
            if (!targetId) return;

            // Переключение классов
            tabs.forEach(t => t.classList.remove("active"));
            sections.forEach(s => s.classList.remove("active"));

            tab.classList.add("active");
            
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add("active");
                
                // Обновление заголовка
                pageTitle.textContent = tab.textContent.trim().split('\n')[1] || tab.textContent.trim();

                // Логика подгрузки данных при переключении
                if (targetId === "orders-section") {
                    if (typeof window.renderOrdersTable === 'function') {
                        window.renderOrdersTable();
                    }
                }
                // Здесь можно добавить логику для других вкладок (clients, inventory и т.д.)
            }

            // На мобильных закрывать меню после клика
            const sidebar = document.querySelector('.sidebar');
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('open');
            }
        });
    });

    // Мобильное меню
    const menuBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
}
