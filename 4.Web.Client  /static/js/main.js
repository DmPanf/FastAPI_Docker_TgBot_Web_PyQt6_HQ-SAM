// main.js

// Импортируем нужные элементы и функции из других модулей
import { elements, handleFile, handleDrop, saveimg } from './handleDom.js';
import { predict } from './apiCalls.js';

// Event Listeners

// Добавляем слушатель события для изменения входного файла.
// При выборе файла вызывается функция handleFile
elements.fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));

// Добавляем слушатель события для перетаскивания файла (dragover).
// Предотвращаем стандартное поведение события
elements.dropZone.addEventListener("dragover", (e) => e.preventDefault());

// Добавляем слушатель события для отпускания файла (drop).
// Вызывается функция handleDrop
elements.dropZone.addEventListener("drop", handleDrop);

// Добавляем слушатель события для кнопки обработки.
// Вызывается функция predict при клике на кнопку
elements.processButton.addEventListener("click", predict);

// Добавляем слушатель события для кнопки сохранения изображения.
// Вызывается функция saveimg при клике на кнопку
elements.saveButton.addEventListener("click", saveimg);
