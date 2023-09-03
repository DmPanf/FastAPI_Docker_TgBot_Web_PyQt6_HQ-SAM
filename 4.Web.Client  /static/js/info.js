// код асинхронно отправляет GET-запрос к /info, 
// получает ответ в формате JSON и выводит его в элемент с id info-box

async function fetchInfo() {
  try {
    const response = await fetch('/info'); // URL от FastAPI эндпоинта
    if (response.ok) {
      const data = await response.json();
      const infoBox = document.getElementById('info-box');
      infoBox.innerHTML = `
        <p><b>Project:</b> <small><i>${data["Project 2023"]}</i></small></p>
      `;
    } else {
      console.error(`Failed to fetch info: ${response.status}`);
    }
  } catch (error) {
    console.error(`Failed to fetch info: ${error}`);
  }
}

// Вызов функции при загрузке страницы
window.addEventListener('load', fetchInfo);
