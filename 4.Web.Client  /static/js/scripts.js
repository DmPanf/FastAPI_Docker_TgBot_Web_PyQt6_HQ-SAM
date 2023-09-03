// DOM Elements
const elements = {
    fileInput: document.getElementById("fileInput"),
    dropZone: document.getElementById("dropZone"),
    originalImage: document.getElementById("originalImage"),
    processedImage: document.getElementById("processedImage"),
    modelSelect: document.getElementById("modelSelect"),
    processButton: document.getElementById("processButton"),
    saveButton: document.getElementById("saveButton")
};


// File Handling
let currentFile = null;
const handleFile = (file) => {
    currentFile = file;
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
        elements.originalImage.src = reader.result;
    };
};


const handleDrop = (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
};


// Fetch API call for prediction
async function predict() {
    //console.log("Predict function started"); // Контрольная точка 1: Начало функции
    if (!currentFile) {  // Проверка на наличие файла
        // Контрольная точка 2: Ошибка - файл не выбран
        console.error("No image selected.");
        return;
    }

    // console.log("Current file:", currentFile);  // Контрольная точка 3: выводим текущий файл
    const server = document.querySelector('input[name="server"]:checked').value;  // Получаем сервер из выбранной радиокнопки
    const model = elements.modelSelect.value;  // Получаем выбранную модель

    const formData = new FormData();
    formData.append("file", currentFile);  // Добавляем файл
    if (model) {
        formData.append("mdl_name", model);  // Добавляем имя модели, если оно есть
    }

    // console.log("FormData prepared", formData);  // Контрольная точка 4: FormData сформирована

    try {
        // console.log(`Sending request to ${server}/predict`); // Контрольная точка 5: Начало отправки запроса
        const response = await fetch(`${server}/predict`, {
            method: "POST",
            headers: {
                'accept': 'application/json',
            },
            body: formData  // Передаем FormData
        });

        // console.log("Received response", response);  // Контрольная точка 6: Получен ответ
        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const blob = await response.blob();  // Получаем обработанное изображение в виде Blob
        const blobUrl = URL.createObjectURL(blob);  // Создаем URL из Blob

        // console.log("Blob and Blob URL", blob, blobUrl);   // Контрольная точка 7: Blob и URL Blob-а
        elements.processedImage.src = blobUrl;  // Устанавливаем URL в src элемента для отображения обработанного изображения
    } catch (error) {
        // Контрольная точка 8: Поймана ошибка
        console.error(error);
    }
    // console.log("Predict function finished"); // Контрольная точка 9: Конец функции
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
}



// Event Listeners
elements.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
elements.dropZone.addEventListener("dragover", (e) => e.preventDefault());
elements.dropZone.addEventListener("drop", handleDrop);
elements.processButton.addEventListener("click", predict);
elements.saveButton.addEventListener("click", saveimg);
