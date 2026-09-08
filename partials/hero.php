<!-- 
    НАЧАЛО СЕКЦИИ HERO (ГЕРОЙ)
    Главный экран с заголовком, подзаголовком, кнопками и видео
-->
<section class="hero" id="hero">
    <div class="container hero-container">
        <!-- Левая часть: текст и кнопки -->
        <div class="hero-content">
            <!-- ЗАГОЛОВОК ГЕРОЯ: Часть выделена жёлтым цветом -->
            <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
            <h1>Пришло время сделать выбор — <span>твой путь к успеху</span></h1>
            
            <!-- ПОДЗАГОЛОВОК: Описание FOHOW -->
            <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
            <p class="hero-subtitle">
                FOHOW — это международная компания, предлагающая уникальные высокотехнологичные продукты 
                для здоровья и благополучия. Присоединяйся к команде успешных людей и начни зарабатывать, 
                помогая другим становиться здоровее!
            </p>
            
            <!-- КНОПКИ ПРИЗЫВА К ДЕЙСТВИЮ -->
            <div class="hero-buttons">
                <!-- Основная кнопка: ведёт к форме -->
                <a href="#form" class="btn btn-primary">Узнать условия бизнеса</a>
                <!-- Второстепенная кнопка: открывает видео или скроллит к видео -->
                <a href="#hero-video" class="btn btn-secondary">Смотреть приветствие</a>
            </div>
        </div>
        
        <!-- Правая часть: видео-обложка -->
        <div class="hero-video-wrapper" id="hero-video">
            <!-- ВИДЕО-ЗАГЛУШКА: Замените на реальное видео -->
            <!-- ЗДЕСЬ ВСТАВЬТЕ СВОЁ ВИДЕО: Раскомментируйте iframe ниже и укажите ссылку на видео -->
            <div class="video-placeholder">
                <div class="video-poster">
                    <!-- Иконка Play (SVG) -->
                    <div class="play-icon">
                        <div class="play-triangle"></div>
                    </div>
                    <!-- ПОДПИСЬ ПОД ВИДЕО -->
                    <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
                    <p class="video-caption">Приветственное видео</p>
                </div>
            </div>
            <!-- 
                КАК ЗАМЕНИТЬ НА РЕАЛЬНОЕ ВИДЕО:
                1. Если видео на YouTube/Vimeo - используйте iframe:
                <iframe src="https://www.youtube.com/embed/ВАШ_ID" frameborder="0" allowfullscreen style="width:100%;height:100%;border-radius:12px;"></iframe>
                
                2. Если видео локальное - используйте тег video:
                <video controls style="width:100%;border-radius:12px;">
                    <source src="video/hero.mp4" type="video/mp4">
                </video>
            -->
        </div>
    </div>
</section>
<!-- КОНЕЦ СЕКЦИИ HERO -->
