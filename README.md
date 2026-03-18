AI-Based Tri-Modal Cancer Detection System (CT, MRI, & Clinical Logic)
Project Overview
This project is a deep learning-based diagnostic support system designed to analyze multi-modal medical data—specifically CT scans, MRI scans, and hematological reports—to differentiate between various brain tumor types. Developed as a final-year VTU Computer Science and Engineering capstone, the system focuses on the practical application of Artificial Intelligence and clinical logic in a healthcare setting.

The platform integrates a high-performance convolutional neural network, an adaptive clinical rules engine, a robust FastAPI backend, and a professional interface designed for medical practitioners.

Core Features
Tri-Modal Analysis: Specialized detection leveraging CT imaging, MRI imaging, and patient blood biomarkers.

Granular Classification: Supports identification of specific tumor types including Glioma, Meningioma, and Pituitary tumors.

Adaptive Clinical Logic: A demographic-aware engine that evaluates 16 blood markers, adjusting thresholds based on patient age and sex.

Late Fusion Architecture: Decision-level integration that synthesizes visual features and biochemical "red flags" into a single diagnostic output.

Probabilistic Reporting: Provides a confidence score for every prediction to assist in clinical decision-making.

RESTful Architecture: Decoupled backend and frontend for scalable model inference.

Technical Stack
Machine Learning & Data Science
Language: Python

Framework: PyTorch & Torchvision (ResNet-18 Architecture)

Numerical Processing: NumPy & Pandas

Logic Engine: Custom Python-based Clinical Ruleset

Backend Engineering
Framework: FastAPI

Server: Uvicorn

Data Validation: Pydantic

Frontend Development
Library: React.js

Styling: Bootstrap and custom CSS for healthcare-standard UI/UX.

Model Architecture and Logic
The system utilizes a multi-stage inference pipeline:

Visual Experts: Two fine-tuned CNNs (ResNet-18) extract spatial features from MRI and CT scans.

Biochemical Expert: A deterministic algorithm processes blood markers (e.g., Hb, WBC, CRP) to calculate a normalized systemic risk score.

Fusion Head: A final linear layer synthesizes these inputs to classify the case into:

Glioma

Meningioma

Pituitary Tumor

No Tumor (Healthy/Non-cancerous)

Installation and Deployment
1. Repository Access
Bash
git clone https://github.com/your-username/ai-cancer-detection.git
cd ai-cancer-detection
2. Backend Environment Setup
Bash
cd backend
python -m venv venv

# Activation
# Windows:
venv\Scripts\activate 
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
The backend service will be available at: http://127.0.0.1:8000

3. Frontend Application Setup
Bash
cd frontend
npm install
npm start
The application will be available at: http://localhost:3000

API Documentation
Unified Prediction Endpoint
Endpoint: POST /predict

Request Format: Multipart form-data (MRI file, CT file, and JSON-formatted blood data)

Response Schema:

JSON
{
  "prediction": "Meningioma",
  "confidence": 0.8942,
  "blood_risk_detected": true
}
Performance Results
The model has achieved high precision and recall on validated medical datasets. By integrating blood markers with imaging data, the system demonstrates increased sensitivity, maintaining high confidence scores even in cases where visual markers are subtle.

Future Research Directions
Integration with live hospital PACS (Picture Archiving and Communication Systems).

Implementation of Explainable AI (XAI) using Grad-CAM to visualize tumor localization.

Expansion of the clinical engine to include hormonal assays and genetic markers.

Cloud-native deployment on AWS or Azure for remote diagnostic support.

Disclaimer
This project is conducted for educational and research purposes. It is not intended for clinical use or to replace the professional judgment of a qualified medical practitioner.

Authorship
Rohith J, Zain Moosaraza, Priyanka Sharma Department of Computer Science & Engineering

Acknowledgements
We would like to thank the open-source medical imaging communities and the PyTorch research team for providing the datasets and frameworks necessary to conduct this research.
