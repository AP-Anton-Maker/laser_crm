/**
 * Утилита для показа всплывающих уведомлений (Toasts).
 * @param {string} message - Текст сообщения
 * @param {string} type - Тип: 'success', 'error', 'info', 'warning'
 */
export function showToast(message, type = "success") {
    const toast = document.createElement("div");
    
    // Базовые стили контейнера уведомления
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.padding = "12px 24px";
    toast.style.borderRadius = "8px";
    toast.style.color = "#fff";
    toast.style.fontWeight = "500";
    toast.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
    toast.style.zIndex = "9999";
    toast.style.transition = "opacity 0.3s ease, transform 0.3s ease";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(20px)";
    toast.style.fontSize = "14px";
    toast.style.fontFamily = "sans-serif";
    toast.textContent = message;

    // Цвета в зависимости от типа
    switch (type) {
        case "success":
            toast.style.backgroundColor = "#10b981"; // Зеленый
            break;
        case "error":
            toast.style.backgroundColor = "#ef4444"; // Красный
            break;
        case "info":
            toast.style.backgroundColor = "#3b82f6"; // Синий
            break;
        case "warning":
            toast.style.backgroundColor = "#f59e0b"; // Оранжевый
            break;
        default:
            toast.style.backgroundColor = "#6b7280"; // Серый
    }

    document.body.appendChild(toast);

    // Анимация появления (небольшая задержка для применения стилей)
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });

    // Автоматическое удаление через 3 секунды
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}
