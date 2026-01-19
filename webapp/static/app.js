// Получаем объект Telegram WebApp API
const tg = window.Telegram.WebApp;

// Глобальные переменные
let currentUserId = null;
let searchProfiles = [];
let currentProfileIndex = 0;
let currentPhotoIndex = 0;
let currentPhotos = [];

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
  // Расширяем WebApp на весь экран
  tg.expand();

  // Инициализируем
  initApp();
});

/**
 * Инициализация приложения
 */
async function initApp() {
  const initData = tg.initDataUnsafe;

  // Проверяем наличие данных пользователя
  if (!initData.user) {
    document.getElementById("searchCard").innerHTML = `
      <div class="error">
        <h2>⚠️ Ошибка</h2>
        <p>Откройте это приложение через Telegram бота</p>
      </div>
    `;
    return;
  }

  currentUserId = initData.user.id;

  // Загружаем анкеты для поиска
  await loadSearchProfiles();
}

/**
 * Загрузка анкет для поиска
 */
async function loadSearchProfiles() {
  const searchCard = document.getElementById("searchCard");
  searchCard.innerHTML = '<div class="loading">Поиск анкет...</div>';

  try {
    const response = await fetch(`/api/search/${currentUserId}`);

    if (!response.ok) {
      throw new Error("Ошибка загрузки анкет");
    }

    const data = await response.json();
    searchProfiles = data.profiles;
    currentProfileIndex = 0;

    if (searchProfiles.length === 0) {
      searchCard.innerHTML = `
        <div class="error">
          <h2>😔 Анкеты не найдены</h2>
          <p>Попробуйте позже или измените настройки поиска</p>
        </div>
      `;
      return;
    }

    // Показываем первую анкету
    showCurrentProfile();
  } catch (error) {
    console.error("Error loading search profiles:", error);
    searchCard.innerHTML = `
      <div class="error">
        <h2>❌ Ошибка</h2>
        <p>Не удалось загрузить анкеты</p>
      </div>
    `;
  }
}

/**
 * Показать текущую анкету
 */
function showCurrentProfile() {
  if (currentProfileIndex >= searchProfiles.length) {
    document.getElementById("searchCard").innerHTML = `
      <div class="error">
        <h2>🎉 Это все!</h2>
        <p>Вы просмотрели все доступные анкеты</p>
      </div>
    `;
    document.getElementById("photoIndicators").innerHTML = "";
    return;
  }

  const profile = searchProfiles[currentProfileIndex];
  currentPhotos = profile.photos || [];
  currentPhotoIndex = 0;

  displayProfile(profile);
  updatePhotoIndicators();
}

/**
 * Отображение данных профиля
 */
function displayProfile(profile) {
  const profileCard = document.getElementById("searchCard");

  // Формируем иконку пола
  const genderIcon = profile.gender === "male" ? "👨" : "👩";

  // Формируем HTML профиля
  let html = "";

  // Фото (если есть)
  if (currentPhotos.length > 0) {
    html += `<img src="${currentPhotos[currentPhotoIndex]}" alt="Photo" class="profile-avatar" onclick="nextPhoto()">`;
  }

  // Имя
  html += `<h1 class="profile-name">${genderIcon} ${profile.name}</h1>`;

  // Возраст и город
  html += `<div class="profile-info">${profile.age} лет • ${profile.city}</div>`;

  // Username
  if (profile.username) {
    html += `
      <div class="profile-detail">
        <div class="profile-detail-icon">📱</div>
        <div class="profile-detail-text">
          <a href="https://t.me/${profile.username}" class="profile-username" target="_blank">
            @${profile.username}
          </a>
        </div>
      </div>
    `;
  }

  // Instagram
  if (profile.instagram) {
    html += `
      <div class="profile-detail">
        <div class="profile-detail-icon">📷</div>
        <div class="profile-detail-text">
          <a href="https://instagram.com/${profile.instagram}" class="profile-username" target="_blank">
            @${profile.instagram}
          </a>
        </div>
      </div>
    `;
  }

  // Описание
  if (profile.description) {
    html += `
      <div class="profile-description">
        <strong>📝 О себе:</strong><br>
        ${profile.description}
      </div>
    `;
  }

  // Счетчик
  html += `<div class="profile-counter">${currentProfileIndex + 1} / ${
    searchProfiles.length
  }</div>`;

  profileCard.innerHTML = html;
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
 * Следующая фотография
 */
function nextPhoto() {
  if (currentPhotos.length <= 1) return;

  currentPhotoIndex = (currentPhotoIndex + 1) % currentPhotos.length;

  // Обновляем только фото
  const img = document.querySelector(".profile-avatar");
  if (img) {
    img.src = currentPhotos[currentPhotoIndex];
  }

  updatePhotoIndicators();
  tg.HapticFeedback?.impactOccurred("light");
}

/**
 * Лайк анкеты
 */
async function like() {
  if (currentProfileIndex >= searchProfiles.length) return;

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
      // Вибрация при успешном лайке
      tg.HapticFeedback?.impactOccurred("medium");

      // Переходим к следующей анкете
      currentProfileIndex++;
      showCurrentProfile();
    }
  } catch (error) {
    console.error("Error liking profile:", error);
    tg.showAlert("❌ Ошибка при отправке лайка");
  }
}

/**
 * Дизлайк анкеты
 */
async function dislike() {
  if (currentProfileIndex >= searchProfiles.length) return;

  const profile = searchProfiles[currentProfileIndex];

  try {
    const response = await fetch("/api/dislike", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: currentUserId,
        target_id: profile.user_id,
      }),
    });

    if (response.ok) {
      // Легкая вибрация
      tg.HapticFeedback?.impactOccurred("light");

      // Переходим к следующей анкете
      currentProfileIndex++;
      showCurrentProfile();
    }
  } catch (error) {
    console.error("Error disliking profile:", error);
  }
}

/**
 * Показать модальное окно сообщения
 */
function showMessageModal() {
  document.getElementById("messageModal").classList.add("show");
  document.getElementById("messageText").value = "";
  tg.HapticFeedback?.impactOccurred("medium");
}

/**
 * Закрыть модальное окно сообщения
 */
function closeMessageModal() {
  document.getElementById("messageModal").classList.remove("show");
}

/**
 * Отправить сообщение с лайком
 */
async function sendMessage() {
  if (currentProfileIndex >= searchProfiles.length) return;

  const profile = searchProfiles[currentProfileIndex];
  const messageText = document.getElementById("messageText").value.trim();

  if (!messageText) {
    tg.showAlert("⚠️ Введите сообщение");
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
        message: messageText,
      }),
    });

    if (response.ok) {
      closeMessageModal();
      tg.HapticFeedback?.notificationOccurred("success");
      tg.showAlert("✅ Сообщение отправлено!");

      // Переходим к следующей анкете
      currentProfileIndex++;
      showCurrentProfile();
    }
  } catch (error) {
    console.error("Error sending message:", error);
    tg.showAlert("❌ Ошибка при отправке сообщения");
  }
}

/**
 * Показать модальное окно жалобы
 */
function showComplaintModal() {
  document.getElementById("complaintModal").classList.add("show");
  tg.HapticFeedback?.impactOccurred("medium");
}

/**
 * Закрыть модальное окно жалобы
 */
function closeComplaintModal() {
  document.getElementById("complaintModal").classList.remove("show");
}

/**
 * Отправить жалобу
 */
async function sendComplaint(reason) {
  if (currentProfileIndex >= searchProfiles.length) return;

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
      closeComplaintModal();
      tg.HapticFeedback?.notificationOccurred("success");
      tg.showAlert("✅ Жалоба отправлена");

      // Переходим к следующей анкете
      currentProfileIndex++;
      showCurrentProfile();
    }
  } catch (error) {
    console.error("Error sending complaint:", error);
    tg.showAlert("❌ Ошибка при отправке жалобы");
  }
}

// Закрытие модальных окон по клику на фон
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("modal")) {
    closeMessageModal();
    closeComplaintModal();
  }
});
