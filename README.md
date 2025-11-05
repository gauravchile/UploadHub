# UploadHub ⚙️

[![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge\&logo=docker\&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-darkgreen?style=for-the-badge\&logo=django\&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge\&logo=postgresql\&logoColor=white)](https://www.postgresql.org/)
[![MinIO](https://img.shields.io/badge/MinIO-S3-Compatible-orange?style=for-the-badge\&logo=minio\&logoColor=white)](https://min.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge\&logo=github\&logoColor=white)](LICENSE)

---

## 🧠 Project Overview

**UploadHub** is a lightweight, Dockerized **Django REST API** that enables **secure file uploads** using **presigned URLs** via **MinIO (S3-compatible object storage)**. It demonstrates multi-container orchestration, environment-based configuration, and practical DevOps deployment workflows.

This project is perfect for building your **DevOps portfolio** — showing skills in **Docker Compose**, **microservice integration**, **logging**, and **infrastructure automation**.

---

## ⚙️ Tech Stack

* **Django REST Framework** – API backend
* **PostgreSQL** – Relational database
* **MinIO** – Object storage (S3-compatible)
* **Gunicorn** – WSGI production server
* **Docker & Docker Compose** – Container orchestration

---

## 🏗️ Architecture

```
📦 UploadHub
├── app/
│   ├── uploadhub/          # Django project configuration
│   ├── files/              # File upload logic, views & models
│   └── manage.py
├── docker-compose.yml      # Multi-service orchestration
├── Dockerfile              # Django container image build
├── .env                    # Environment configuration (excluded from repo)
└── README.md               # Project documentation
```

---

## 🚀 Features

✅ Django REST API with presigned upload URLs
✅ MinIO for object storage and access management
✅ PostgreSQL for metadata persistence
✅ Gunicorn for production-ready deployment
✅ Docker Compose orchestration with isolated services
✅ Environment-driven configuration for flexible setups

---

## 🐋 Setup Instructions

### 1️⃣ Build and Run Containers

```bash
docker compose up --build -d
```

### 2️⃣ Check Running Services

```bash
docker ps
```

Expected containers:

* `uploadhub_web` → Django app
* `uploadhub_db` → PostgreSQL database
* `uploadhub_minio` → Object storage

### 3️⃣ Access the Services

| Service           | URL                                            |
| ----------------- | ---------------------------------------------- |
| **API**           | [http://localhost:8000](http://localhost:8000) |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) |
| **PostgreSQL**    | localhost:5432                                 |

---

## 📡 API Endpoints

### Generate a Presigned Upload URL

```bash
curl -X POST http://localhost:8000/api/presign/ \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.txt"}'
```

**Response:**

```json
{
  "upload_url": "http://localhost:9000/uploads/20251105170806_test.txt?...",
  "storage_key": "20251105170806_test.txt",
  "curl_command": "curl -X PUT -T \"test.txt\" \"http://localhost:9000/uploads/...\""
}
```

### Upload File to MinIO

```bash
curl -X PUT -T test.txt "<upload_url_from_response>"
```
---

## 🧠 DevOps Highlights

* Multi-container orchestration using Docker Compose
* Environment variable configuration for portability
* Secure presigned URL file uploads
* Service networking between Django, MinIO, and PostgreSQL
* Logging and debugging workflow with `docker compose logs`

---

## 🧰 Future Enhancements

* Add Nginx reverse proxy + HTTPS support 🔒
* Implement download presigned URLs 📥
* Add monitoring (Prometheus + Grafana) 📊
* Automate CI/CD with GitHub Actions ⚙️
* Deploy on AWS ECS / GCP Cloud Run ☁️

---

## 👨‍💻 Author

**Gaurav Chile**
DevOps & Security Enthusiast
🚀 *Automating, Orchestrating, and Optimizing Cloud-Native Systems*

---

## 🏁 License

Licensed under the **MIT License** – feel free to use and modify.

