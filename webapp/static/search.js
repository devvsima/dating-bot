// Поиск анкет - Telegram WebApp с Swipe механикой
const tg = window.Telegram.WebApp;

// Глобальные переменные
let currentUserId = null;
let searchProfiles = [];
let currentProfileIndex = 0;
let currentPhotoIndex = 0;
let currentPhotos = [];

// Переменные для свайпа
let touchStartX = 0;
let touchStartY = 0;
let touchEndX = 0;
let touchEndY = 0;
let isDragging = false;
let currentCard = null;
let startTime = 0;
let swipeDirection = null; // 'horizontal' или 'vertical'

// Константы для свайпа
const SWIPE_THRESHOLD = window.innerWidth > 768 ? 50 : 80; // Меньший порог для десктопа
const SWIPE_VELOCITY_THRESHOLD = 0.5; // Минимальная скорость свайпа
const ROTATION_FACTOR = 0.15; // Коэффициент поворота карточки
const RESISTANCE_FACTOR = 0.7; // Сопротивление при малых движениях
const DIRECTION_LOCK_THRESHOLD = 20; // Порог для определения направления

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
  tg.expand();
  initApp();
});

/**
 * Инициализация приложения
 */
async function initApp() {
  const initData = tg.initDataUnsafe;

  if (!initData.user) {
    document.getElementById("cardsContainer").innerHTML = `
      <div class="error">
        <h2>⚠️ Ошибка</h2>
        <p>Откройте это приложение через Telegram бота</p>
      </div>
    `;
    return;
  }

  currentUserId = initData.user.id;
  await loadSearchProfiles();
}

/**
 * Загрузка анкет для поиска
 */
async function loadSearchProfiles() {
  const container = document.getElementById("cardsContainer");
  container.innerHTML = '<div class="loading">Поиск анкет...</div>';

  try {
    const response = await fetch(`/api/search/${currentUserId}`);

    if (!response.ok) {
      throw new Error("Ошибка загрузки анкет");
    }

    const data = await response.json();
    searchProfiles = data.profiles;
    currentProfileIndex = 0;

    if (searchProfiles.length === 0) {
      container.innerHTML = `
        <div class="error">
          <h2>😔 Анкеты не найдены</h2>
          <p>Попробуйте позже или измените настройки поиска</p>
        </div>
      `;
      return;
    }

    // Показываем первые 2 карточки (текущая и следующая)
    showCards();
  } catch (error) {
    console.error("Error loading search profiles:", error);
    container.innerHTML = `
      <div class="error">
        <h2>❌ Ошибка</h2>
        <p>Не удалось загрузить анкеты</p>
      </div>
    `;
  }
}

/**
 * Показать карточки
 */
function showCards() {
  const container = document.getElementById("cardsContainer");
  container.innerHTML = "";

  if (currentProfileIndex >= searchProfiles.length) {
    container.innerHTML = `
      <div class="error">
        <h2>🎉 Это все!</h2>
        <p>Вы просмотрели все доступные анкеты</p>
      </div>
    `;
    document.getElementById("photoIndicators").innerHTML = "";
    return;
  }

  // Создаем текущую карточку
  const profile = searchProfiles[currentProfileIndex];
  const card = createCard(profile);
  container.appendChild(card);

  // Создаем следующую карточку (если есть)
  if (currentProfileIndex + 1 < searchProfiles.length) {
    const nextProfile = searchProfiles[currentProfileIndex + 1];
    const nextCard = createCard(nextProfile);
    nextCard.classList.add("card-next");
    container.appendChild(nextCard);
  }

  currentCard = card;
  currentPhotos = profile.photos || [];
  currentPhotoIndex = 0;
  updatePhotoIndicators();

  // Добавляем обработчики свайпа
  setupSwipeHandlers(card);
}

/**
 * Создать карточку профиля
 */
function createCard(profile) {
  const card = document.createElement("div");
  card.className = "profile-card swipeable";
  card.dataset.userId = profile.user_id;

  const genderIcon = profile.gender === "male" ? "👨" : "👩";
  const photos = profile.photos || [];

  let html = "";

  // Фото
  if (photos.length > 0) {
    html += `<div class="card-photo-container" onclick="nextPhoto()">
      <img src="${photos[0]}" alt="Photo" class="profile-avatar">`;

    // Если фото больше одного, показываем индикатор
    if (photos.length > 1) {
      html += `<div class="photo-counter">+${photos.length - 1}</div>`;
    }

    html += `</div>`;
  }

  // Информация
  html += `<div class="card-info">
    <h1 class="profile-name">${genderIcon} ${profile.name}, ${profile.age}</h1>
    <div class="profile-info">📍 ${profile.city}</div>`;

  if (profile.username) {
    html += `<div class="profile-detail">
      📱 <a href="https://t.me/${profile.username}" target="_blank">@${profile.username}</a>
    </div>`;
  }

  if (profile.instagram) {
    html += `<div class="profile-detail">
      📷 <a href="https://instagram.com/${profile.instagram}" target="_blank">@${profile.instagram}</a>
    </div>`;
  }

  if (profile.description) {
    html += `<div class="profile-description">
      <strong>📝 О себе:</strong><br>
      ${profile.description}
    </div>`;
  }

  html += `<div class="profile-counter">${currentProfileIndex + 1} / ${
    searchProfiles.length
  }</div>`;
  html += `</div>`;

  card.innerHTML = html;
  return card;
}

/**
 * Настройка обработчиков свайпа
 */
function setupSwipeHandlers(card) {
  // Touch события
  card.addEventListener("touchstart", handleTouchStart, { passive: false });
  card.addEventListener("touchmove", handleTouchMove, { passive: false });
  card.addEventListener("touchend", handleTouchEnd, { passive: false });

  // Mouse события (для десктопа)
  card.addEventListener("mousedown", handleMouseDown);
  document.addEventListener("mousemove", handleMouseMove);
  document.addEventListener("mouseup", handleMouseUp);
}

function handleTouchStart(e) {
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
  touchEndX = touchStartX;
  touchEndY = touchStartY;
  isDragging = true;
  startTime = Date.now();
  swipeDirection = null; // Сбрасываем направление

  currentCard.style.transition = "";
  tg.HapticFeedback.impactOccurred("light");
}

function handleTouchMove(e) {
  if (!isDragging) return;
  e.preventDefault();

  touchEndX = e.touches[0].clientX;
  touchEndY = e.touches[0].clientY;

  const deltaX = touchEndX - touchStartX;
  const deltaY = touchEndY - touchStartY;

  // Определяем направление свайпа (один раз в начале)
  if (
    swipeDirection === null &&
    (Math.abs(deltaX) > DIRECTION_LOCK_THRESHOLD ||
      Math.abs(deltaY) > DIRECTION_LOCK_THRESHOLD)
  ) {
    swipeDirection =
      Math.abs(deltaX) > Math.abs(deltaY) ? "horizontal" : "vertical";
  }

  // Применяем сопротивление для более плавного движения
  let adjustedX = deltaX;
  let adjustedY = deltaY;

  // Блокируем движение в зависимости от выбранного направления
  if (swipeDirection === "horizontal") {
    adjustedY = 0; // Блокируем вертикальное движение
    if (Math.abs(deltaX) < SWIPE_THRESHOLD) {
      adjustedX = deltaX * RESISTANCE_FACTOR;
    }
  } else if (swipeDirection === "vertical") {
    adjustedX = 0; // Блокируем горизонтальное движение
    if (Math.abs(deltaY) < SWIPE_THRESHOLD) {
      adjustedY = deltaY * RESISTANCE_FACTOR;
    }
  } else {
    // Пока не определено направление, применяем сопротивление ко всем осям
    if (Math.abs(deltaX) < DIRECTION_LOCK_THRESHOLD) {
      adjustedX = deltaX * RESISTANCE_FACTOR;
    }
    if (Math.abs(deltaY) < DIRECTION_LOCK_THRESHOLD) {
      adjustedY = deltaY * RESISTANCE_FACTOR;
    }
  }

  // Поворот карточки зависит от горизонтального смещения
  const rotation = adjustedX * ROTATION_FACTOR;

  // Прозрачность зависит от расстояния
  const maxDistance = window.innerWidth / 2;
  const distance = Math.sqrt(adjustedX * adjustedX + adjustedY * adjustedY);
  const opacity = Math.max(0.3, 1 - distance / maxDistance);

  // Двигаем карточку
  currentCard.style.transform = `translate(${adjustedX}px, ${adjustedY}px) rotate(${rotation}deg)`;
  currentCard.style.opacity = opacity;

  // Показываем индикатор
  updateSwipeIndicator(deltaX, deltaY);
}

function handleTouchEnd(e) {
  if (!isDragging) return;
  isDragging = false;

  const deltaX = touchEndX - touchStartX;
  const deltaY = touchEndY - touchStartY;
  const deltaTime = Date.now() - startTime;

  // Вычисляем скорость свайпа
  const velocity = Math.sqrt(deltaX * deltaX + deltaY * deltaY) / deltaTime;

  // Определяем направление свайпа
  const absX = Math.abs(deltaX);
  const absY = Math.abs(deltaY);

  let shouldSwipe = false;
  let direction = null;

  // Используем установленное направление для определения действия
  if (swipeDirection === "horizontal") {
    if (
      (absX > SWIPE_THRESHOLD && velocity > SWIPE_VELOCITY_THRESHOLD) ||
      absX > SWIPE_THRESHOLD * 1.5
    ) {
      shouldSwipe = true;
      direction = deltaX > 0 ? "right" : "left";
    }
  } else if (swipeDirection === "vertical") {
    if (
      (absY > SWIPE_THRESHOLD && velocity > SWIPE_VELOCITY_THRESHOLD) ||
      absY > SWIPE_THRESHOLD * 1.5
    ) {
      shouldSwipe = true;
      direction = deltaY < 0 ? "up" : "down";
    }
  }

  if (shouldSwipe) {
    switch (direction) {
      case "right":
        swipeRight();
        break;
      case "left":
        swipeLeft();
        break;
      case "up":
        swipeUp();
        break;
      case "down":
        swipeDown();
        break;
    }
  } else {
    resetCard();
  }

  swipeDirection = null; // Сбрасываем направление
  hideSwipeIndicator();
}

function handleMouseDown(e) {
  // Игнорируем клики по ссылкам и интерактивным элементам
  if (e.target.tagName === "A" || e.target.closest("a")) {
    return;
  }

  touchStartX = e.clientX;
  touchStartY = e.clientY;
  touchEndX = touchStartX;
  touchEndY = touchStartY;
  isDragging = true;
  startTime = Date.now();
  swipeDirection = null; // Сбрасываем направление

  currentCard.style.transition = "";
}

function handleMouseMove(e) {
  if (!isDragging) return;
  e.preventDefault();

  touchEndX = e.clientX;
  touchEndY = e.clientY;

  const deltaX = touchEndX - touchStartX;
  const deltaY = touchEndY - touchStartY;

  // Определяем направление свайпа (один раз в начале)
  if (
    swipeDirection === null &&
    (Math.abs(deltaX) > DIRECTION_LOCK_THRESHOLD ||
      Math.abs(deltaY) > DIRECTION_LOCK_THRESHOLD)
  ) {
    swipeDirection =
      Math.abs(deltaX) > Math.abs(deltaY) ? "horizontal" : "vertical";
  }

  // Применяем сопротивление
  let adjustedX = deltaX;
  let adjustedY = deltaY;

  // Блокируем движение в зависимости от выбранного направления
  if (swipeDirection === "horizontal") {
    adjustedY = 0; // Блокируем вертикальное движение
    if (Math.abs(deltaX) < SWIPE_THRESHOLD) {
      adjustedX = deltaX * RESISTANCE_FACTOR;
    }
  } else if (swipeDirection === "vertical") {
    adjustedX = 0; // Блокируем горизонтальное движение
    if (Math.abs(deltaY) < SWIPE_THRESHOLD) {
      adjustedY = deltaY * RESISTANCE_FACTOR;
    }
  } else {
    // Пока не определено направление
    if (Math.abs(deltaX) < DIRECTION_LOCK_THRESHOLD) {
      adjustedX = deltaX * RESISTANCE_FACTOR;
    }
    if (Math.abs(deltaY) < DIRECTION_LOCK_THRESHOLD) {
      adjustedY = deltaY * RESISTANCE_FACTOR;
    }
  }

  const rotation = adjustedX * ROTATION_FACTOR;
  const maxDistance = window.innerWidth / 2;
  const distance = Math.sqrt(adjustedX * adjustedX + adjustedY * adjustedY);
  const opacity = Math.max(0.3, 1 - distance / maxDistance);

  currentCard.style.transform = `translate(${adjustedX}px, ${adjustedY}px) rotate(${rotation}deg)`;
  currentCard.style.opacity = opacity;

  updateSwipeIndicator(deltaX, deltaY);
}

function handleMouseUp(e) {
  if (!isDragging) return;
  handleTouchEnd(e);
}

/**
 * Обновление индикатора свайпа
 */
function updateSwipeIndicator(deltaX, deltaY) {
  const indicator = document.getElementById("swipeIndicator");
  const icon = indicator.querySelector(".swipe-icon");

  const absX = Math.abs(deltaX);
  const absY = Math.abs(deltaY);

  // Увеличиваем видимость индикатора по мере движения
  const maxDistance = 150;
  const distance = Math.max(absX, absY);
  const opacity = Math.min(1, distance / maxDistance);

  if (absX > absY && absX > 30) {
    if (deltaX > 0) {
      // Вправо - Лайк
      indicator.className = "swipe-indicator active like";
      icon.textContent = "❤️";
    } else {
      // Влево - Дизлайк
      indicator.className = "swipe-indicator active dislike";
      icon.textContent = "👎";
    }
    indicator.style.opacity = opacity;
  } else if (absY > absX && absY > 30) {
    if (deltaY < 0) {
      // Вверх - Сообщение
      indicator.className = "swipe-indicator active message";
      icon.textContent = "💌";
    } else {
      // Вниз - Жалоба
      indicator.className = "swipe-indicator active complaint";
      icon.textContent = "💢";
    }
    indicator.style.opacity = opacity;
  } else {
    indicator.className = "swipe-indicator";
    indicator.style.opacity = 0;
  }
}

function hideSwipeIndicator() {
  const indicator = document.getElementById("swipeIndicator");
  indicator.className = "swipe-indicator";
  indicator.style.opacity = 0;
}

function resetCard() {
  currentCard.style.transition =
    "all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
  currentCard.style.transform = "";
  currentCard.style.opacity = "1";
  setTimeout(() => {
    if (currentCard) {
      currentCard.style.transition = "";
    }
  }, 300);
}

/**
 * Действия свайпа
 */
function swipeRight() {
  animateSwipe("right");
  like();
  tg.HapticFeedback.notificationOccurred("success");
}

function swipeLeft() {
  animateSwipe("left");
  dislike();
  tg.HapticFeedback.impactOccurred("medium");
}

function swipeUp() {
  resetCard();
  showMessageModal();
  tg.HapticFeedback.impactOccurred("light");
}

function swipeDown() {
  resetCard();
  showComplaintModal();
  tg.HapticFeedback.impactOccurred("light");
}

function animateSwipe(direction) {
  const distance = window.innerWidth + 200;
  const rotate = direction === "right" ? 25 : -25;
  const translateX = direction === "right" ? distance : -distance;

  currentCard.style.transition = "all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1)";
  currentCard.style.transform = `translateX(${translateX}px) rotate(${rotate}deg)`;
  currentCard.style.opacity = "0";

  setTimeout(() => {
    nextProfile();
  }, 400);
}

/**
 * Следующий профиль
 */
function nextProfile() {
  currentProfileIndex++;
  currentPhotoIndex = 0;
  showCards();
  tg.HapticFeedback.impactOccurred("light");
}

/**
 * Следующее фото
 */
function nextPhoto() {
  if (currentPhotos.length <= 1) return;

  currentPhotoIndex = (currentPhotoIndex + 1) % currentPhotos.length;
  const img = currentCard.querySelector(".profile-avatar");
  img.src = currentPhotos[currentPhotoIndex];
  updatePhotoIndicators();

  tg.HapticFeedback.impactOccurred("light");
}

/**
 * Обновление индикаторов фотографий
 */
function updatePhotoIndicators() {
  const indicators = document.getElementById("photoIndicators");

  if (currentPhotos.length <= 1) {
    indicators.innerHTML = "";
    return;
  }

  let html = "";
  for (let i = 0; i < currentPhotos.length; i++) {
    html += `<div class="photo-dot ${
      i === currentPhotoIndex ? "active" : ""
    }"></div>`;
  }
  indicators.innerHTML = html;
}

/**
 * Лайк
 */
async function like() {
  const profile = searchProfiles[currentProfileIndex];

  try {
    const response = await fetch("/api/like", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: currentUserId,
        target_id: profile.user_id,
        message: null,
      }),
    });

    if (response.ok) {
      tg.HapticFeedback.notificationOccurred("success");
    }
  } catch (error) {
    console.error("Error liking profile:", error);
  }
}

/**
 * Дизлайк
 */
async function dislike() {
  const profile = searchProfiles[currentProfileIndex];

  try {
    await fetch("/api/dislike", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: currentUserId,
        target_id: profile.user_id,
      }),
    });

    tg.HapticFeedback.impactOccurred("medium");
  } catch (error) {
    console.error("Error disliking profile:", error);
  }
}

/**
 * Модальное окно сообщения
 */
function showMessageModal() {
  document.getElementById("messageModal").style.display = "flex";
  document.getElementById("messageText").value = "";
}

function closeMessageModal() {
  document.getElementById("messageModal").style.display = "none";
}

async function sendMessage() {
  const profile = searchProfiles[currentProfileIndex];
  const message = document.getElementById("messageText").value.trim();

  if (!message) {
    tg.showAlert("Введите сообщение");
    return;
  }

  try {
    const response = await fetch("/api/like", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: currentUserId,
        target_id: profile.user_id,
        message: message,
      }),
    });

    if (response.ok) {
      tg.HapticFeedback.notificationOccurred("success");
      closeMessageModal();
      animateSwipe("right");
    }
  } catch (error) {
    console.error("Error sending message:", error);
    tg.showAlert("Ошибка отправки сообщения");
  }
}

/**
 * Модальное окно жалобы
 */
function showComplaintModal() {
  document.getElementById("complaintModal").style.display = "flex";
}

function closeComplaintModal() {
  document.getElementById("complaintModal").style.display = "none";
}

async function sendComplaint(reason) {
  const profile = searchProfiles[currentProfileIndex];

  try {
    const response = await fetch("/api/complaint", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: currentUserId,
        target_id: profile.user_id,
        reason: reason,
      }),
    });

    if (response.ok) {
      tg.HapticFeedback.notificationOccurred("warning");
      closeComplaintModal();
      animateSwipe("left");
    }
  } catch (error) {
    console.error("Error sending complaint:", error);
    tg.showAlert("Ошибка отправки жалобы");
  }
}
