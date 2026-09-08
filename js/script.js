/**
 * FOHOW Landing Page - JavaScript
 * Все скрипты для лендинга FOHOW
 * Включает: маску телефона, аккордеон FAQ, плавную прокрутку, мобильное меню
 */

// ============================================
// ДОЖИДАЕМСЯ ЗАГРУЗКИ DOM
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // МАСКА ДЛЯ ТЕЛЕФОНА
    // Формат: +7 (999) 999-99-99
    // ============================================
    const phoneInput = document.getElementById('phone');
    
    if (phoneInput) {
        // Функция форматирования телефона
        function formatPhone(value) {
            // Удаляем все нецифровые символы
            let digits = value.replace(/\D/g, '');
            
            // Если начинается с 8, заменяем на 7
            if (digits.startsWith('8')) {
                digits = '7' + digits.slice(1);
            }
            
            // Если не начинается с 7, добавляем 7
            if (!digits.startsWith('7')) {
                digits = '7' + digits;
            }
            
            // Ограничиваем длину (11 цифр для российского номера)
            if (digits.length > 11) {
                digits = digits.slice(0, 11);
            }
            
            // Форматируем: +7 (XXX) XXX-XX-XX
            let formatted = '+7';
            if (digits.length > 1) {
                formatted += ' (' + digits.slice(1, 4);
            }
            if (digits.length > 4) {
                formatted += ') ' + digits.slice(4, 7);
            }
            if (digits.length > 7) {
                formatted += '-' + digits.slice(7, 9);
            }
            if (digits.length > 9) {
                formatted += '-' + digits.slice(9, 11);
            }
            
            return formatted;
        }
        
        // Обработчик ввода
        phoneInput.addEventListener('input', function(e) {
            const formatted = formatPhone(e.target.value);
            e.target.value = formatted;
        });
        
        // Обработчик фокуса - показываем полную маску
        phoneInput.addEventListener('focus', function(e) {
            if (e.target.value === '') {
                e.target.value = '+7 (';
            }
        });
        
        // Обработчик потери фокуса - убираем неполные значения
        phoneInput.addEventListener('blur', function(e) {
            if (e.target.value === '+7 (' || e.target.value === '+7') {
                e.target.value = '';
            }
        });
    }
    
    // ============================================
    // АККОРДЕОН ДЛЯ FAQ
    // Раскрывается только один вопрос за раз
    // ============================================
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(function(item) {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', function() {
            const isActive = item.classList.contains('active');
            
            // Закрываем все остальные вопросы
            faqItems.forEach(function(otherItem) {
                otherItem.classList.remove('active');
            });
            
            // Если этот вопрос не был активен, открываем его
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
    
    // ============================================
    // ПЛАВНАЯ ПРОКРУТКА ДЛЯ ЯКОРНЫХ ССЫЛОК
    // ============================================
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Игнорируем ссылки без id или просто "#"
            if (href === '#' || href.length < 2) {
                return;
            }
            
            const targetId = href.substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                // Учитываем высоту фиксированной шапки (70px)
                const headerOffset = 70;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Закрываем мобильное меню после клика
                const navMenu = document.querySelector('.nav-menu');
                const hamburger = document.querySelector('.hamburger');
                
                if (navMenu && navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    hamburger.classList.remove('active');
                }
            }
        });
    });
    
    // ============================================
    // МОБИЛЬНОЕ МЕНЮ (ГАМБУРГЕР)
    // ============================================
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Закрываем меню при клике вне его области
        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
    
    // ============================================
    // ОБРАБОТЧИК ОТПРАВКИ ФОРМЫ
    // ============================================
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            const phoneInput = document.getElementById('phone');
            const agreementCheckbox = document.getElementById('agreement');
            
            // Простая валидация
            let isValid = true;
            
            // Проверка имени
            if (!nameInput || nameInput.value.trim() === '') {
                alert('Пожалуйста, введите ваше имя');
                isValid = false;
            }
            
            // Проверка телефона (минимум 10 символов для +7 (XXX) XXX)
            if (!phoneInput || phoneInput.value.replace(/\D/g, '').length < 10) {
                alert('Пожалуйста, введите корректный номер телефона');
                isValid = false;
            }
            
            // Проверка согласия
            if (!agreementCheckbox || !agreementCheckbox.checked) {
                alert('Необходимо согласие с политикой конфиденциальности');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // ============================================
    // ВИДЕО-ЗАГУШКИ (ОПЦИОНАЛЬНО)
    // Можно добавить обработку кликов по видео-заглушкам
    // для открытия модального окна с видео
    // ============================================
    const videoPlaceholders = document.querySelectorAll('.video-placeholder');
    
    videoPlaceholders.forEach(function(video) {
        video.addEventListener('click', function() {
            // Здесь можно добавить логику открытия модального окна
            // или перехода на страницу с видео
            console.log('Клик по видео-заглушке. Замените на реальное видео.');
            
            // Пример: открыть видео в модальном окне
            // const videoSrc = this.getAttribute('data-video-src');
            // openVideoModal(videoSrc);
        });
    });
    
});

// ============================================
// ФУНКЦИЯ ДЛЯ ОТКРЫТИЯ ВИДЕО В МОДАЛЬНОМ ОКНЕ
// (Опционально, если нужно)
// ============================================
function openVideoModal(videoSrc) {
    // Создаём модальное окно
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2000;
    `;
    
    const videoContainer = document.createElement('div');
    videoContainer.style.cssText = `
        position: relative;
        width: 80%;
        max-width: 900px;
        aspect-ratio: 16/9;
    `;
    
    const iframe = document.createElement('iframe');
    iframe.src = videoSrc;
    iframe.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    `;
    iframe.setAttribute('allowfullscreen', '');
    
    videoContainer.appendChild(iframe);
    modal.appendChild(videoContainer);
    document.body.appendChild(modal);
    
    // Закрытие по клику вне видео
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    // Закрытие по Esc
    document.addEventListener('keydown', function closeOnEsc(e) {
        if (e.key === 'Escape') {
            modal.remove();
            document.removeEventListener('keydown', closeOnEsc);
        }
    });
}
