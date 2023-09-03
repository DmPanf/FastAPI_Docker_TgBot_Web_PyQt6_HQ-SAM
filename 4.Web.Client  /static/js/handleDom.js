// handleDom.js

// DOM Elements
export const elements = {
    fileInput: document.getElementById("fileInput"),
    dropZone: document.getElementById("dropZone"),
    originalImage: document.getElementById("originalImage"),
    processedImage: document.getElementById("processedImage"),
    // downloadLink: document.getElementById("downloadLink"),
    modelSelect: document.getElementById("modelSelect"),
    processButton: document.getElementById("processButton"),
    saveButton: document.getElementById("saveButton")
};


// Функция для обработки выбранного файла
export const handleFile = (file) => {
    // Создаем новый объект FileReader для чтения содержимого файла
    const reader = new FileReader();

    // Читаем содержимое файла и преобразуем его в Data URL (base64)
    reader.readAsDataURL(file);

    // Добавляем обработчик события onload, который будет вызван, когда чтение файла завершится успешно
    reader.onload = () => {
        // Задаем источник изображения как результат чтения файла (в формате Data URL)
        elements.originalImage.src = reader.result;
    };

    // Добавляем обработчик события onerror для отлавливания ошибок при чтении файла
    reader.onerror = (error) => {
        // Выводим сообщение об ошибке в консоль
        console.error("Ошибка чтения файла: ", error);
    };

    // Добавляем обработчик события onabort для отлавливания прерываний при чтении файла
    reader.onabort = () => {
        // Выводим сообщение о прерывании в консоль
        console.error("Чтение файла было прервано");
    };
};


export const handleDrop = (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
};


function saveimg() {
    // Находим элемент с обработанным изображением
    const imageElement = document.getElementById("processedImage");

    // Получаем URL изображения
    const imageUrl = imageElement.src;

    // Создаем элемент "a" для скачивания
    const link = document.createElement("a");

    // Устанавливаем URL и другие атрибуты
    link.href = imageUrl;
    link.download = 'processed_image.png';

    // Добавляем элемент на страницу (невидимый)
    document.body.appendChild(link);

    // Программно кликаем по нему, чтобы начать загрузку
    link.click();

    // Удаляем элемент со страницы
    document.body.removeChild(link);
};
