let customSlideIndex = 0;
let customSlides = document.querySelectorAll(".custom-slide");

function customShowSlide(index) {
    // Циклично переключаем слайды
    if (index >= customSlides.length) {
        customSlideIndex = 0;
    } else if (index < 0) {
        customSlideIndex = customSlides.length - 1;
    } else {
        customSlideIndex = index;
    }

    customSlides.forEach((slide, i) => {
        slide.style.display = (i === customSlideIndex) ? "block" : "none";
    });
}

// Функция для кнопок "вперед" и "назад"
function customChangeSlide(direction) {
    customShowSlide(customSlideIndex + direction);
}

// Инициализация слайд-шоу с показом первого слайда
customShowSlide(customSlideIndex);

// Автоматическое переключение слайдов
let customAutoSwitchInterval = 3000; // 3 секунды
setInterval(() => customChangeSlide(1), customAutoSwitchInterval);



document.addEventListener("DOMContentLoaded", function () {
    let currentIndex = 0;
    const slides = document.querySelectorAll(".gallery-slide");
    const slideWidth = slides[0].offsetWidth; // Ширина одного слайда
    const totalSlides = slides.length;
    let slidesToShow = 4; // По умолчанию показываем 4 слайда

    const prevButton = document.querySelector(".gallery-prev");
    const nextButton = document.querySelector(".gallery-next");

    let startX = 0; // Начальная точка касания
    let currentX = 0; // Текущая точка касания
    let isDragging = false; // Флаг перемещения

    // Обновление слайдов и адаптивность под мобильные устройства
    function updateSlides() {
        // Изменяем slidesToShow в зависимости от ширины экрана
        if (window.innerWidth <= 768) {
            slidesToShow = 1; // На мобильных показываем по 1 слайду
        } else {
            slidesToShow = 4; // На больших экранах показываем по 4 слайда
        }

        const offset = -currentIndex * slideWidth;
        document.querySelector(".gallery-slideshow").style.transform = `translateX(${offset}px)`;
        updateButtons(); // Обновляем состояние кнопок
    }

    function updateButtons() {
        // Отключаем кнопку "Назад", если текущий индекс равен 0
        prevButton.disabled = currentIndex === 0;

        // Отключаем кнопку "Вперед", если текущий индекс достиг конца списка
        nextButton.disabled = currentIndex >= totalSlides - slidesToShow;
    }

    function changeSlide(direction) {
        currentIndex += direction;

        // Проверяем границы для currentIndex
        if (currentIndex < 0) {
            currentIndex = 0;
        } else if (currentIndex > totalSlides - slidesToShow) {
            currentIndex = totalSlides - slidesToShow;
        }

        updateSlides();
    }

    prevButton.addEventListener("click", function () {
        changeSlide(-1);
    });

    nextButton.addEventListener("click", function () {
        changeSlide(1);
    });

    // Добавляем поддержку свайпа для мобильных устройств
    const slideshow = document.querySelector(".gallery-slideshow");

    slideshow.addEventListener("touchstart", function (e) {
        startX = e.touches[0].clientX; // Получаем начальную позицию касания
        isDragging = true;
    });

    slideshow.addEventListener("touchmove", function (e) {
        if (!isDragging) return;

        currentX = e.touches[0].clientX;
        const deltaX = currentX - startX; // Разница между текущей и начальной позицией

        // Перемещаем слайды в зависимости от движения пальца
        slideshow.style.transform = `translateX(${-currentIndex * slideWidth + deltaX}px)`;
    });

    slideshow.addEventListener("touchend", function () {
        isDragging = false;
        const deltaX = currentX - startX;

        // Если свайп больше 50px, перемещаем слайды
        if (Math.abs(deltaX) > 50) {
            if (deltaX > 0) {
                changeSlide(-1); // Свайп вправо (переход к предыдущему слайду)
            } else {
                changeSlide(1); // Свайп влево (переход к следующему слайду)
            }
        } else {
            // Если свайп был слишком маленьким, возвращаем слайды на место
            updateSlides();
        }
    });

    window.addEventListener('resize', updateSlides); // Обновляем слайды при изменении размера окна

    updateSlides(); // Изначально отображаем правильные слайды и обновляем состояние кнопок
});



let currentIndex = 0;
const reviewItems = document.querySelectorAll('.review-item');
const totalReviews = reviewItems.length;
let reviewVisibleCount = 3; // По умолчанию отображаем 3 отзыва на десктопе
let autoSwitchInterval; // Для автоматического переключения

// Функция для установки количества видимых отзывов в зависимости от ширины экрана
function updateReviewVisibleCount() {
    if (window.innerWidth <= 768) {
        reviewVisibleCount = 1; // Для мобильных показываем по одному отзыву
    } else {
        reviewVisibleCount = 3; // Для десктопа показываем 3 отзыва
    }
}

function showReviews() {
    reviewItems.forEach((item, index) => {
        // Условие для добавления класса active
        if (index >= currentIndex && index < currentIndex + reviewVisibleCount) {
            item.classList.add('active'); // Добавляем класс active к видимым
        } else {
            item.classList.remove('active'); // Удаляем класс active у скрытых
        }
    });
}

function changeReview(direction) {
    const maxIndex = totalReviews - reviewVisibleCount;

    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex > maxIndex) {
        currentIndex = maxIndex;
        clearInterval(autoSwitchInterval); // Остановить автопрокрутку, если конец
    }

    showReviews();
}

// Обработчики касаний
function handleTouchStart(event) {
    startX = event.touches[0].clientX; // Запоминаем начальную позицию касания
}

function handleTouchMove(event) {
    endX = event.touches[0].clientX; // Запоминаем конечную позицию касания
}

function handleTouchEnd() {
    if (startX > endX + 50) {
        // Если движение было влево
        changeReview(1);
    } else if (startX < endX - 50) {
        // Если движение было вправо
        changeReview(-1);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    updateReviewVisibleCount(); // Обновляем количество отзывов при загрузке
    showReviews(); // Показать начальные отзывы

    // Кнопки "вперед" и "назад"
    document.querySelector('.gallery-prev1').addEventListener('click', () => {
        changeReview(-1);
    });

    document.querySelector('.gallery-next1').addEventListener('click', () => {
        changeReview(1);
    });

    // Автоматическое переключение отзывов каждые 5 секунд, если отзывов больше, чем видимо
    if (totalReviews > reviewVisibleCount) {
        autoSwitchInterval = setInterval(() => changeReview(1), 5000);
    }

    // Пересчитываем количество видимых отзывов при изменении размера окна
    window.addEventListener('resize', () => {
        updateReviewVisibleCount();
        showReviews();
    });

    // Добавляем обработчики касания
    const reviewsContainer = document.querySelector('.reviews-container'); // Замените на ваш контейнер
    reviewsContainer.addEventListener('touchstart', handleTouchStart, false);
    reviewsContainer.addEventListener('touchmove', handleTouchMove, false);
    reviewsContainer.addEventListener('touchend', handleTouchEnd, false);
});
