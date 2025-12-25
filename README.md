# 🚦 Banff Mobility & Parking Prediction System 
### CMPT 3835 – Machine Learning & Software Engineering Project

A production-ready machine learning and analytics system designed to support the Town of Banff in understanding and predicting **parking occupancy** and **traffic flow**.  
This project demonstrates modern software engineering and MLOps practices, including modular architecture, clean data pipelines, reproducible modeling, and a deployed web application built with **React + Vite** and a **SQL-driven backend**.

**Technologies:** 
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-025E8C?style=flat&logo=sqlite&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=flat&logo=powerbi&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![Proxmox](https://img.shields.io/badge/Proxmox-E57000?style=flat&logo=proxmox&logoColor=white)
![Cloudflare Tunnel](https://img.shields.io/badge/Cloudflare_Tunnel-F38020?style=flat&logo=cloudflare&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)


---

## 📌 Project Overview

The increasing volume of visitors in Banff creates pressure on **parking infrastructure**, **traffic corridors**, and **mobility planning**.  
Our project predicts:

- Parking occupancy (residents and visitors)  
- Traffic volumes across major access routes  
- A web interface to explore predictions and query mobility data

The system integrates field observations, municipal datasets, predictive modeling, and a deployed frontend application.

---

## 📂 1. Data Collection

All datasets were provided by the **Town of Banff**.  
Although multiple files were delivered, only a subset was usable due to inconsistent dates.

Final datasets included:

- ✅ **Parking + Plate File:** Jan 2024–Apr 2024 and Aug 2024–Aug 2025  
- ✅ **Traffic:** Jan 2024–Aug 2025  
- ✅ **Routes:** Bridge Ave, Mountain Ave, West Entrance, East Entrance  

⚠️ Additional datasets were excluded due to inconsistent timelines and missing intervals.

---

## 🧹 2. Data Processing Pipeline

- Standardizing timestamps  
- Cleaning missing entries  
- Feature engineering (hour, weekday, visitor vs resident patterns)  
- Merging parking + traffic  
- Preparing data for modeling and dashboards  

---

## 🤖 3. Modeling Approach

- Models for **resident** and **visitor** occupancy  
- Traffic prediction by route  
- Metrics: MAE, RMSE, R²  
- Models reveal peak hours, seasonality, and tourist impact  

---

## 🏗️ 4. System Architecture

The system is composed of three main services composed to handle specific workloads, along with a dedicated database layer.

  ### 1. 🧠 Backend API (Prediction Service)
  * **Framework:** FastAPI
  * **Function:** Loads trained ML models and processes requests from the frontend to return predictions.
  * **Deployment:** Runs in its own dedicated container.
  * **Key Endpoints:**
    * `/predict/resident`
    * `/predict/visitor`

  ### 2. 💬 SQL Chatbot API (Query Service)
  * **Framework:** FastAPI
  * **Function:** Handles natural-language questions by converting text → SQL queries.
  * **Deployment:** Runs in a separate container to ensure workload isolation.

  ### 3. 💻 Frontend App
  * **Stack:** React + Vite
  * **Function:** Serves as the user interface for both the prediction engine and the chatbot.
  * **Connectivity:** Communicates with both FastAPI services.
  * **Delivery:** Served through a Cloudflare tunnel.

  ### 4. 🗄️ Database Layer
  * **Type:** SQL
  * **Function:** Stores cleaned datasets and provides the necessary tables for chatbot queries.

---

## 🖥️ 5. Application Usage

### Frontend
```
npm install
npm run dev
```

### Backend
- Load SQL tables  
- Run prediction scripts  
- Use UI to select model and generate forecasts  

Endpoints:

- GET /health → Health check
- POST /predict/resident → Predict resident parking occupancy
- POST /predict/visitor → Predict visitor parking occupancy

### Chatbot
Queries mobility data such as:
- “Traffic at West Entrance yesterday”  
- “Visitor parking downtown last weekend”  

---

## 📁 6. Project Structure

```ssh
banff-mobility-project/
│
├── data/
│   ├── raw/                     # Original datasets from the Town of Banff
│   ├── processed/               # Cleaned + merged datasets
│   └── exports/                 # Outputs for Power BI and analysis
│
├── backend/
│   ├── api/                     # Prediction FastAPI service
│   │   ├── models/              # Serialized resident/visitor models
│   │   └── main.py              # API entry point (8000)
│   │
│   ├── chatbot/                 # SQL-powered chatbot service
│   │   ├── sql/                 # Templates + DB handlers
│   │   └── main.py              # Chatbot entry point (8001)
│   │
│   └── db/
│       └── init.sql             # Database schema + table setup
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── data/
│   │   ├── App.jsx
│   │   └── styles/
│   │
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   └── vite.config.js
│
├── dashboards/
│   ├── powerbi/
│   └── assets/
│
├── docs/
│   ├── report/
│   ├── architecture/
│   ├── api/
│   └── presentation/
│
├── docker/
│   ├── prediction.Dockerfile
│   ├── chatbot.Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
└── README.md
```

---

## 📊 7. Key Findings

- Visitors peak on weekends and summer months  
- Residents show consistent patterns  
- Bridge Ave & Mountain Ave have highest traffic  
- Predictions support planning and resource allocation  

---

## 📅 8. Project Status

### ✔️ Completed  
- Data processing  
- Model development  
- Chatbot  
- React app  
- Dashboards  
- Final presentation (Dec 10, 2025)

### 🚀 Future Work  
- Weather/event integration  
- Real-time ingestion  
- Better chatbot routing  
- Docker + CI/CD deployment  

---

## 🤝 9. Contributing

1. Fork the repo  
2. Create a feature branch  
3. Commit  
4. Push  
5. Open PR  

---

## 🙏 10. Acknowledgements

- **Town of Banff**  
- **NorQuest College**  
- Project team  

---

## 📬 Contact

CMPT 2500 – Machine Learning Deployment & Software Development  
NorQuest College  
2025
