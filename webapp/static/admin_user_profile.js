// Admin User Profile Viewer
const tg = window.Telegram.WebApp;

let userId = null;
let adminId = null;

// Инициализация приложения
function initApp() {
  tg.ready();
  tg.expand();

  // Получаем ID пользователя из URL
  const pathParts = window.location.pathname.split("/");
  userId = parseInt(pathParts[pathParts.length - 1]);

  // Получаем ID администратора из Telegram
  const user = tg.initDataUnsafe?.user;
  if (user) {
    adminId = user.id;
    loadUserProfile();
  } else {
    showError("Ошибка авторизации");
  }
}

// Загрузка профиля пользователя
async function loadUserProfile() {
  try {
    const response = await fetch(
      `/api/admin/user/${userId}?admin_id=${adminId}`
    );

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error("У вас нет прав доступа");
      } else if (response.status === 404) {
        throw new Error("Пользователь не найден");
      }
      throw new Error(`Ошибка: ${response.status}`);
    }

    const profile = await response.json();
    displayProfile(profile);
  } catch (error) {
    console.error("Error loading profile:", error);
    showError(error.message);
  }
}

// Отображение профиля
function displayProfile(profile) {
  const card = document.getElementById("profileCard");

  const photos =
    profile.photos && profile.photos.length > 0
      ? profile.photos
      : ["https://via.placeholder.com/400x400?text=No+Photo"];

  const instagramLink = profile.instagram
    ? `<div class="profile-info-item">
               <span class="profile-label">Instagram:</span>
               <a href="https://instagram.com/${profile.instagram}" target="_blank">@${profile.instagram}</a>
           </div>`
    : "";

  card.innerHTML = `
        <div class="profile-header">
            <h2>👤 Просмотр профиля</h2>
            <p class="profile-id">ID: ${profile.id}</p>
        </div>

        <div class="profile-photos">
            <img src="${photos[0]}" alt="${
    profile.name
  }" class="profile-avatar" onclick="nextPhoto()">
            ${
              photos.length > 1
                ? `
                <div class="photo-indicators" id="photoIndicators"></div>
            `
                : ""
            }
        </div>

        <div class="profile-details">
            <h1 class="profile-name">${profile.name}, ${profile.age}</h1>

            <div class="profile-info">
                <div class="profile-info-item">
                    <span class="profile-label">Пол:</span>
                    <span>${
                      profile.gender === "male" ? "Мужской 👨" : "Женский 👩"
                    }</span>
                </div>
                <div class="profile-info-item">
                    <span class="profile-label">Город:</span>
                    <span>${profile.city}</span>
                </div>
                ${
                  profile.username
                    ? `
                    <div class="profile-info-item">
                        <span class="profile-label">Username:</span>
                        <a href="https://t.me/${profile.username}" target="_blank">@${profile.username}</a>
                    </div>
                `
                    : ""
                }
                ${instagramLink}
            </div>

            ${
              profile.description
                ? `
                <div class="profile-description">
                    <span class="profile-label">О себе:</span>
                    <p>${profile.description}</p>
                </div>
            `
                : ""
            }
        </div>

        <div class="admin-actions">
            <button class="action-btn action-btn-secondary" onclick="goBack()">◀️ Назад</button>
        </div>
    `;

  // Инициализируем галерею фотографий
  if (photos.length > 1) {
    window.currentPhotos = photos;
    window.currentPhotoIndex = 0;
    updatePhotoIndicators();
  }
}

// Переключение фото
let currentPhotoIndex = 0;
let currentPhotos = [];

function nextPhoto() {
  if (currentPhotos.length <= 1) return;

  currentPhotoIndex = (currentPhotoIndex + 1) % currentPhotos.length;
  const img = document.querySelector(".profile-avatar");
  img.src = currentPhotos[currentPhotoIndex];
  updatePhotoIndicators();

  tg.HapticFeedback.impactOccurred("light");
}

function updatePhotoIndicators() {
  const container = document.getElementById("photoIndicators");
  if (!container || currentPhotos.length <= 1) return;

  container.innerHTML = currentPhotos
    .map(
      (_, index) =>
        `<span class="photo-dot ${
          index === currentPhotoIndex ? "active" : ""
        }"></span>`
    )
    .join("");
}

// Показать ошибку
function showError(message) {
  const card = document.getElementById("profileCard");
  card.innerHTML = `
        <div class="error-message">
            <h2>❌ Ошибка</h2>
            <p>${message}</p>
            <button class="action-btn" onclick="goBack()">Назад</button>
        </div>
    `;
}

// Вернуться назад
function goBack() {
  tg.close();
}

// Запускаем приложение
initApp();
