## 💾 Пример интерфейса Web-Client
<!--
<p align="center">
<img src="https://raw.githubusercontent.com/DmPanf/PyQt6_FastAPI_HQ-SAM/main/images/pyqt6_01.jpg" width="40%" />
</p>
-->

<details>
<summary><h3>🌐 Пример web-клиента (HTML+JavaScript+CSS)</h3></summary>
<p align="center">
<img src="https://raw.githubusercontent.com/DmPanf/PyQt6_FastAPI_HQ-SAM/main/images/web-client-01.jpg" width="90%" />
</p>
</details>

---

## Project Title: Real-time Object Detection with YOLOv8 and FastAPI 📄🤖

### Description 🌐

This project aims to implement real-time object detection using YOLOv8 and FastAPI. The project has a web frontend built with HTML5 and JavaScript, where users can upload images to be processed. The server, written in FastAPI, accepts the image and model name, performs object detection, and sends the processed image back to the client.

### Features ✨

- Real-time Object Detection
- FastAPI Backend
- Dockerized Application
- GPU Support
- API for model prediction

### Technologies Used 🛠

- **FastAPI**: For building robust APIs
- **YOLOv8**: Object Detection algorithm
- **TensorFlow**: Backend for the YOLO model
- **Docker**: Containerization
- **JavaScript**: Frontend
- **OpenCV**: Image processing

### Installation and Setup 🚀

#### Using Docker 💎

1. Clone this repository
    ```bash
    git clone https://github.com/DmPanf/FastAPI_Docker_TgBot_Web_PyQt6_HQ-SAM.git
    ```

2. Navigate to the project folder
    ```bash
    cd project-folder
    ```

3. Build the Docker image
    ```bash
    docker-compose up --build
    ```

#### Manual Installation ☯️

1. Clone this repository
    ```bash
    git clone https://github.com/DmPanf/FastAPI_Docker_TgBot_Web_PyQt6_HQ-SAM.git
    ```

2. Install Python dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run FastAPI server
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8001
    ```

#### Python Dependencies ⚖️

- See `requirements.txt` for a list of required Python packages.

### API Usage 📝 

Use the `api_request.py` script to send a POST request to the FastAPI server for prediction. The server will respond with the processed image.

```python
python api_request.py
```

### Dockerfile and docker-compose.yml ⚙️

The project uses a Dockerfile based on the TensorFlow GPU Jupyter image. It sets up the necessary environment and copies the code files into the `/app` directory. The `docker-compose.yml` file configures the services, ports, and other settings.

### License 📃

MIT License

---

### Recommended project directory structure presented in text form:

```
Project-Title/
│
├── app/                        # FastAPI app directory
│   ├── main.py                 # FastAPI main app
│   ├── models/                 # Machine learning models (e.g., YOLOv8)
│   ├── utils/                  # Utility scripts and helper functions
│   └── routes/                 # API routes
│
├── frontend/                   # Frontend related files
│   ├── index.html              # Main HTML page
│   ├── js/                     # JavaScript files
│   └── css/                    # Stylesheets
│
├── docker-compose.yml          # Docker Compose configuration file
├── Dockerfile                  # Dockerfile for building the project image
│
├── scripts/
│   └── api_request.py          # Python script for testing API
│
├── requirements.txt            # Python dependencies
│
└── README.md                   # Project description and instructions
```

- `app/` contains the FastAPI application files, where `main.py` is the entry point.
- `app/models/` will contain your machine learning models like YOLOv8.
- `app/utils/` can contain any utility scripts and helper functions.
- `app/routes/` can contain individual route definitions for the FastAPI app.
  
- `frontend/` contains all the frontend related files like HTML, CSS, and JavaScript.

- `docker-compose.yml` contains the Docker Compose configuration to manage containers.
  
- `Dockerfile` is used for building your Docker image.

- `scripts/` can contain utility scripts like `api_request.py` that are not part of the main application but are useful for tasks like API testing.

- `requirements.txt` lists all the Python dependencies required for your project.


This is a general structure and could vary depending on the specific requirements of the project.
