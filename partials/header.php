<!-- 
    НАЧАЛО ФАЙЛА HEADER (ШАПКА)
    Логотип, контактный телефон, навигация
    Для мобильных устройств - гамбургер-меню
-->
<header class="header">
    <div class="container header-container">
        <!-- ЛОГОТИП: Замените SVG на реальное изображение при необходимости -->
        <!-- ССЫЛКА НА ИЗОБРАЖЕНИЕ: img/logo.svg или используйте текст -->
        <a href="#" class="logo">
            <!-- SVG-заглушка логотипа - круг с буквой F -->
            <svg class="logo-svg" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="20" cy="20" r="20" fill="#f5a623"/>
                <text x="20" y="27" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#1a3a5f" text-anchor="middle">F</text>
            </svg>
            <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ: Название компании -->
            FOHOW
        </a>
        
        <!-- Контактный телефон в шапке -->
        <!-- ТЕЛЕФОН ДЛЯ РЕДАКТИРОВАНИЯ -->
        <a href="tel:+79126802227" class="header-phone">+7 912 680-22-27</a>
        
        <!-- Гамбургер-меню для мобильных устройств -->
        <button class="hamburger" aria-label="Меню">
            <span></span>
            <span></span>
            <span></span>
        </button>
        
        <!-- Навигация (якорные ссылки на секции) -->
        <nav>
            <ul class="nav-menu">
                <!-- ЯКОРНЫЕ ССЫЛКИ: ведут на соответствующие секции по id -->
                <li><a href="#about" class="nav-link">О компании</a></li>
                <li><a href="#advantages" class="nav-link">Преимущества</a></li>
                <li><a href="#earnings" class="nav-link">Способы заработка</a></li>
                <li><a href="#testimonials" class="nav-link">Отзывы</a></li>
                <li><a href="#steps" class="nav-link">Как начать</a></li>
                <li><a href="#faq" class="nav-link">FAQ</a></li>
                <li><a href="#form" class="nav-link">Контакты</a></li>
            </ul>
        </nav>
    </div>
</header>
<!-- КОНЕЦ ФАЙЛА HEADER -->
