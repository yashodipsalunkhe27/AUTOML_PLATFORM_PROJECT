# 🚀 AutoML Platform

[![Backend](https://img.shields.io/badge/Backend-Live-brightgreen?style=for-the-badge&logo=render)](https://automl-platform-project.onrender.com)
[![Frontend](https://img.shields.io/badge/Frontend-Live-blue?style=for-the-badge&logo=vercel)](https://automl-platform-project.vercel.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#-license)

An End-to-End **AutoML Platform** built using **FastAPI** (backend) and **React + Vite** (frontend) that automates the complete Machine Learning workflow. Users can upload datasets, analyze data, preprocess features, train multiple machine learning models, compare their performance, generate reports, and make predictions through an intuitive, fully deployed web interface.

The platform supports both **Classification** and **Regression** problems with automatic model selection, hyperparameter tuning, and performance evaluation.

---

## 🔗 Live Demo

| Layer | Link |
|---|---|
| 🌐 Frontend (Vercel) | **[automl-platform-project.vercel.app](https://automl-platform-project.vercel.app/)** |
| ⚙️ Backend API (Render) | **[automl-platform-project.onrender.com](https://automl-platform-project.onrender.com)** |
| 📄 API Docs (Swagger) | [automl-platform-project.onrender.com/docs](https://automl-platform-project.onrender.com/docs) |

> ⚠️ **Note:** The backend is hosted on Render's free tier, so the first request after inactivity may take 30–60 seconds to spin up (cold start).

---

# 📌 Project Overview

This project is designed to simplify the Machine Learning workflow by providing an easy-to-use web application that automates every major step of the ML pipeline — from raw data to a deployed prediction interface.

Instead of writing Python code for every stage, users can:

- Upload datasets
- Analyze datasets
- Preprocess data
- Train multiple ML models
- Automatically select the best model
- Perform hyperparameter tuning
- Compare model performance
- Make predictions
- Download reports

The platform is suitable for beginners, students, and professionals who want to build machine learning models without manually coding every step.

---

# ✨ Features

## 📂 Dataset Management
- Upload CSV datasets
- Upload Excel datasets
- Upload JSON datasets
- Dataset validation
- Automatic file handling

## 📊 Dataset Analysis
- Total Rows
- Total Columns
- Missing Value Detection
- Duplicate Row Detection
- Numerical Columns
- Categorical Columns
- Data Type Detection

## ⚙ Data Preprocessing
- Missing Value Handling
- Label Encoding
- One-Hot Encoding
- Feature Scaling
- Feature Selection

## 🤖 Model Training

**Classification Models**
- Logistic Regression
- Decision Tree
- Random Forest
- Extra Trees
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- XGBoost
- CatBoost

**Regression Models**
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor
- CatBoost Regressor

## 🎯 Automatic ML
- Automatic Problem Type Detection
- Automatic Best Model Selection
- Hyperparameter Tuning
- Cross Validation

## 📈 Model Evaluation
- Accuracy Score
- Precision, Recall, F1 Score
- ROC AUC Score
- Confusion Matrix
- Feature Importance
- Model Comparison Graph

## 🔮 Prediction
- Single Prediction
- Batch Prediction
- Prediction Confidence

## 📑 Reports
- Training Summary
- Model Information
- Prediction Report
- History Tracking

---

# 🖥 Screenshots

## Dashboard
<img width="1919" height="884" alt="Dashboard" src="https://github.com/user-attachments/assets/34a6e856-5198-46d9-ad4d-c01d0afaa30b" />

## Dataset Upload
<img width="1919" height="936" alt="Dataset Upload" src="https://github.com/user-attachments/assets/88e7cde2-5966-4341-9427-19a4ec69a542" />

## Dataset Analysis
<img width="1919" height="940" alt="Dataset Analysis" src="https://github.com/user-attachments/assets/010e61d6-77b8-4198-92a1-e6b7695061e9" />

## Model Training
<img width="1919" height="938" alt="Model Training 1" src="https://github.com/user-attachments/assets/be2a327d-3db0-4d81-995f-5c9862299f39" />
<img width="1919" height="926" alt="Model Training 2" src="https://github.com/user-attachments/assets/7660bd4b-4837-4397-a41b-7569c952659c" />

## Results Dashboard
<img width="1916" height="933" alt="Results Dashboard" src="https://github.com/user-attachments/assets/cc248141-cab4-47f0-a317-57036ccea0d4" />

## Prediction
<img width="1919" height="936" alt="Prediction" src="https://github.com/user-attachments/assets/1e858738-d767-49c0-b52e-734efddf117d" />

---

# 🛠 Tech Stack

## Frontend
- React.js
- Vite
- React Router
- Axios
- React Icons
- Recharts
- CSS3
- **Deployed on Vercel**

## Backend
- FastAPI
- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- CatBoost
- Joblib
- Matplotlib
- Seaborn
- **Deployed on Render**

## Tools
- Git & GitHub
- VS Code
- Render (Backend Hosting)
- Vercel (Frontend Hosting)

---

# 🏗 Architecture

```
┌──────────────────┐        HTTPS / REST API        ┌───────────────────┐
│   React + Vite    │ ───────────────────────────▶  │     FastAPI        │
│  (Vercel Hosted)   │ ◀───────────────────────────  │  (Render Hosted)   │
│  automl-frontend  │        JSON Responses          │  app.py + src/     │
└──────────────────┘                                 └───────────────────┘
                                                              │
                                                              ▼
                                                    models / graphs / reports
                                                       (generated per run)
```

The frontend communicates with the deployed FastAPI backend via Axios over REST endpoints, handling dataset upload, training triggers, live results, and predictions — all rendered through interactive dashboards built with Recharts.

---

# 📁 Project Structure

```text
AUTOML_PLATFORM_PROJECT
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
├── models/
├── uploads/
├── graphs/
├── reports/
├── static/
│
├── automl-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env
│
└── venv/
```

---

# ⚙ Installation (Run Locally)

## Clone Repository
```bash
git clone https://github.com/yashodipsalunkhe27/AUTOML_PLATFORM_PROJECT.git
cd AUTOML_PLATFORM_PROJECT
```

## 🔧 Backend Setup
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
- Backend URL: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`

## 💻 Frontend Setup
```bash
cd automl-frontend
npm install
npm run dev
```
- Frontend URL: `http://localhost:5173`

> ℹ️ When running locally, update the API base URL in the frontend `.env` file to point to `http://127.0.0.1:8000` instead of the deployed Render URL.

---

# 🌐 API Endpoints

## Dataset
```http
POST /upload
GET  /dataset-analysis
```

## Training
```http
POST /train
GET  /model-info
```

## Prediction
```http
GET  /prediction-schema
POST /predict
POST /batch-predict
```

## Results
```http
GET /model-results
GET /classification-report
GET /feature-importance
GET /confusion-matrix-graph
GET /roc-curve-graph
```

---

# 🚀 Deployment

## Backend — Render
- Deployed as a web service directly from GitHub
- Live at: **https://automl-platform-project.onrender.com**

## Frontend — Vercel
- Deployed directly from the `automl-frontend` directory
- Live at: **https://automl-platform-project.vercel.app/**
- Configured to communicate with the Render backend via environment variables

---

# 🔮 Future Enhancements

- User Authentication
- Role-Based Access
- MLflow Integration
- Docker Support
- Kubernetes Deployment
- Cloud Storage Integration
- Explainable AI (SHAP)
- Model Versioning
- Automatic Model Monitoring
- Email Report Generation

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Create a Pull Request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## Yashodip Salunkhe
**B.Tech – Artificial Intelligence & Data Science**

### Skills
- Data Science
- Machine Learning
- Deep Learning
- FastAPI
- React.js
- Python
- SQL
- Generative AI
- Agentic AI

🔗 [Live Frontend](https://automl-platform-project.vercel.app/) · [Live Backend](https://automl-platform-project.onrender.com) · [GitHub Repo](https://github.com/yashodipsalunkhe27/AUTOML_PLATFORM_PROJECT)

---

⭐ If you like this project, don't forget to **Star** the repository on GitHub.
