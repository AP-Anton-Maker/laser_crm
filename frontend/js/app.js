import { initRouter } from './router.js';
import { renderOrdersTable } from './components/orders_ui.js';
import { showToast } from './utils/toast.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 Laser CRM App started");
    
    // Инициализация роутера (вкладки)
    initRouter();
    
    // Первоначальная загрузка заказов (если мы на вкладке заказов)
    // Но лучше загружать динамически при переключении, что уже сделано в router.js
    
    showToast("Система готова к работе", "info");
});
