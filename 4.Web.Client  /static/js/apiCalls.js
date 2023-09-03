// apiCalls.js
import { elements } from './handleDom.js'; // импорт элементов DOM

export const predict = async () => {
    if (!elements.originalImage.src) {
        console.error("No image selected.");
        return;
    }

    const server = document.querySelector('input[name="server"]:checked').value;
    const model = elements.modelSelect.value;

    const formData = new FormData();
    formData.append("image", dataURLtoFile(elements.originalImage.src, "input.png"));
    formData.append("mdl_name", model);

    try {
        const response = await fetch(`${server}/predict`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const blob = await response.blob();
        const blobUrl = URL.createObjectURL(blob);

        elements.processedImage.src = blobUrl;
        elements.originalImage.src = blobUrl;
    } catch (error) {
        console.error(error);
    }
};
