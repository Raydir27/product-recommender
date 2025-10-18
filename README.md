# 🧠 Product Recommendation & Analytics Web App

*AI + ML + CV + GenAI Integration using FastAPI & React*


## 🚀 Overview

This project was developed as part of the **AI/ML Internship Assignment** — an end-to-end web application that recommends products, generates creative product descriptions, and visualizes analytics insights.

It combines multiple AI domains — **Machine Learning**, **Natural Language Processing**, **Computer Vision**, and **Generative AI** — into a single full-stack ecosystem.

---

## 🧩 Core Features

### 1. **Product Recommendation Engine**

* Embedding-based semantic search using **Pinecone Vector DB**
* Top-K recommendations based on similarity across **textual and visual embeddings**
* FastAPI endpoint `/api/recommend/query` serves recommendations in real time

### 2. **Generative AI Product Descriptions**

* Uses a **lightweight open-source LLM (Gemma-2B via LangChain)** to generate natural, engaging product descriptions
* Contextual responses tailored to the queried product

### 3. **Image Understanding (Computer Vision)**

* Fine-tuned **ResNet model** trained on custom furniture dataset for visual classification
* Used in embedding generation pipeline to improve cross-modal retrieval

### 4. **Data Analytics Dashboard**

* Separate **React route** for dataset analytics
* Displays brand/category distributions, missing-data heatmaps, and price insights
* Data sourced from the provided CSV file and pre-processed in Jupyter Notebooks

---

## ⚙️ Tech Stack

| Layer                   | Technology                                               |
| :---------------------- | :------------------------------------------------------- |
| **Backend**             | FastAPI, Uvicorn                                         |
| **Frontend**            | React, Vite                                              |
| **Database**            | Pinecone (Vector DB)                                     |
| **ML/NLP**              | scikit-learn, Transformers, LangChain                    |
| **CV**                  | PyTorch, ResNet                                          |
| **GenAI**               | Gemma-2B (open source)                                   |
| **Analytics**           | Pandas, Matplotlib, Plotly                               |
| **Deployment (Future)** | Vercel (frontend), Render / HuggingFace Spaces (backend) |

---

## 🧪 Project Structure

```
├── backend/
│   ├── main.py                  # FastAPI app setup
│   ├── routes/
│   │   ├── recommend.py         # Recommendation API endpoint
│   │   ├── analyze.py           # Analytics API (optional)
│   │   └── generate_description.py
│   ├── image_infer.py           # Image inference example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── RecommendPage.jsx
│   │   │   └── AnalyticsPage.jsx
│   │   └── components/
│   │       ├── ChatUI.jsx
│   │       └── ProductCard.jsx
│   └── package.json
│
├── notebooks/
│   ├── data_analytics.ipynb     # Phase 2A/2B analysis notebook
│   ├── embedding_pipeline.ipynb # Embedding generation and model training
│   └── model_evaluation.ipynb
│
├── data/
│   ├── intern_data_ikarus.csv
│   └── images/
│
├── README.md
└── .env.example
```

---

## 🧬 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/product-recommendation-app.git
cd product-recommendation-app
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

Add your Pinecone API key and environment variables in `.env`.

Run the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit: [http://localhost:3000](http://localhost:3000)

---

## 📊 Analytics Notebook Highlights

The analytics notebook (`data_analytics.ipynb`) visualizes:

* Missing data patterns
* Brand and category dominance
* Price distribution analysis
* Embedding space clustering insights

---

## 🤖 AI/ML Pipeline Overview

1. **Data Cleaning & Preprocessing** – Missing value imputation and feature synthesis
2. **Embedding Generation** – Text embeddings (SentenceTransformers) + Image embeddings (ResNet fine-tuned)
3. **Vector Storage** – Embeddings stored in Pinecone for similarity queries
4. **Recommendation Retrieval** – Query → Vector Search → Top-K Products
5. **GenAI Description Generation** – LangChain pipeline with Gemma-2B LLM
6. **Frontend Display** – Recommendations + AI-generated product descriptions

---

## 🧠 Future Enhancements

* Deploy backend & frontend on cloud (Render + Vercel)
* Replace ResNet with **CLIP** or **SigLIP** for better cross-modal embeddings
* Add **user feedback loop** to refine recommendations dynamically
* Integrate **RAG (Retrieval Augmented Generation)** for more context-aware GenAI outputs

---

## 👨‍💻 Author

**Rajarshi Biswas**
AI/ML Developer | Computer Vision & GenAI Research Enthusiast
📍 Mumbai, India
📧 [rajarshibiswas27@gmail.com](mailto:rajarshibiswas27@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/rajarshi-biswas-rb27)

---
