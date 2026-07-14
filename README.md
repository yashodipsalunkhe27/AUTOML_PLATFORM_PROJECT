# 🚀 AutoML Platform

An End-to-End **AutoML Platform** built using **FastAPI** that automates the complete Machine Learning workflow. Users can upload datasets, analyze data, preprocess features, train multiple machine learning models, compare their performance, generate reports, and make predictions through an intuitive web interface.

The platform supports both **Classification** and **Regression** problems with automatic model selection, hyperparameter tuning, and performance evaluation.

---

# 📌 Project Overview

This project is designed to simplify the Machine Learning workflow by providing an easy-to-use web application that automates every major step of the ML pipeline.

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

---

## 📊 Dataset Analysis

- Total Rows
- Total Columns
- Missing Value Detection
- Duplicate Row Detection
- Numerical Columns
- Categorical Columns
- Data Type Detection

---

## ⚙ Data Preprocessing

- Missing Value Handling
- Label Encoding
- One-Hot Encoding
- Feature Scaling
- Feature Selection

---

## 🤖 Model Training

### Classification Models

- Logistic Regression
- Decision Tree
- Random Forest
- Extra Trees
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- XGBoost
- CatBoost

### Regression Models

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor
- CatBoost Regressor

---

## 🎯 Automatic ML

- Automatic Problem Type Detection
- Automatic Best Model Selection
- Hyperparameter Tuning
- Cross Validation

---

## 📈 Model Evaluation

- Accuracy Score
- Precision
- Recall
- F1 Score
- ROC AUC Score
- Confusion Matrix
- Feature Importance
- Model Comparison Graph

---

## 🔮 Prediction

- Single Prediction
- Batch Prediction
- Prediction Confidence

---

## 📑 Reports

- Training Summary
- Model Information
- Prediction Report
- History Tracking

---

# 🖥 Screenshots

## Dashboard

<img width="1919" height="884" alt="image" src="https://github.com/user-attachments/assets/34a6e856-5198-46d9-ad4d-c01d0afaa30b" />


---

## Dataset Upload

<img width="1919" height="936" alt="image" src="https://github.com/user-attachments/assets/88e7cde2-5966-4341-9427-19a4ec69a542" />

---

## Dataset Analysis

<img width="1919" height="940" alt="image" src="https://github.com/user-attachments/assets/010e61d6-77b8-4198-92a1-e6b7695061e9" />


---

## Model Training
<img width="1919" height="938" alt="image" src="https://github.com/user-attachments/assets/be2a327d-3db0-4d81-995f-5c9862299f39" />

<img width="1919" height="926" alt="image" src="https://github.com/user-attachments/assets/7660bd4b-4837-4397-a41b-7569c952659c" />

---

## Results Dashboard


<img width="1916" height="933" alt="image" src="https://github.com/user-attachments/assets/cc248141-cab4-47f0-a317-57036ccea0d4" />

---

## Prediction
<img width="1919" height="936" alt="image" src="https://github.com/user-attachments/assets/1e858738-d767-49c0-b52e-734efddf117d" />


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

---

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

---

## Tools

- Git
- GitHub
- VS Code
- Render
- Vercel

---

# 📁 Project Structure

```text
LOAN_PREDICTION_PROJECT

│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│
├── models/
│
├── uploads/
│
├── graphs/
│
├── reports/
│
├── static/
│
├── automl-frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── venv/
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AutoML-Platform.git

cd LOAN_PREDICTION_PROJECT
```

Replace the repository URL with your own GitHub repository after uploading the project.

---

# 🔧 Backend Setup

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI Server

```bash
uvicorn app:app --reload
```

Backend URL

```text
http://127.0.0.1:8000
```

Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Go to frontend

```bash
cd automl-frontend
```

Install packages

```bash
npm install
```

Run application

```bash
npm run dev
```

Frontend URL

```text
http://localhost:5173
```

---

# 🌐 API Endpoints

## Dataset

```http
POST /upload
GET  /dataset-analysis
```

---

## Training

```http
POST /train
GET  /model-info
```

---

## Prediction

```http
GET  /prediction-schema

POST /predict

POST /batch-predict
```

---

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

## Backend

Deploy using **Render**

---

## Frontend

Deploy using **Vercel**

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

---

⭐ If you like this project, don't forget to **Star** the repository on GitHub.
