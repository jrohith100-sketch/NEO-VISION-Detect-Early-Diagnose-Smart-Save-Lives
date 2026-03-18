🧠 AI-Based Cancer Detection System (CT & MRI)
📌 Overview

This project is a deep learning-based cancer detection system designed to analyze CT and MRI scan images and predict whether a tumor is cancerous or non-cancerous.
It is developed as a final year VTU Computer Science Engineering project, with a focus on healthcare AI applications.
The system integrates:

🧠 Deep Learning Models (CNN)

⚙️ FastAPI Backend

🎨 Modern Healthcare-Themed Frontend

🚀 Features

✅ Tumor detection using CT & MRI images
✅ Supports multiple imaging modalities
✅ Probability-based prediction output
✅ User-friendly web interface
✅ REST API for model inference
✅ Real-time prediction results
✅ Clean and professional healthcare UI

🏗️ Tech Stack

🔹 Machine Learning

Python
PyTorch
NumPy
torchvision

🔹 Backend

FastAPI
Uvicorn

🔹 Frontend

React.js
HTML5, CSS3
Bootstrap / Custom UI

🧠 Model Details

Convolutional Neural Network (CNN)
Trained on medical imaging datasets (CT & MRI scans)
Handles classification tasks such as:
Glioma
Meningioma
Pituitary Tumor
No Tumor

⚙️ Installation & Setup

🔹 1. Clone the Repository
git clone https://github.com/your-username/ai-cancer-detection.git
cd ai-cancer-detection
🔹 2. Backend Setup
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app:app --reload

Backend runs at:

http://127.0.0.1:8000
🔹 3. Frontend Setup
cd frontend

# Install dependencies
npm install

# Run React app
npm start

Frontend runs at:

http://localhost:3000
📡 API Endpoint
🔹 Predict Tumor

POST /predict

Request:

Image file (CT/MRI)

Response:
{
  "prediction": "Glioma",
  "confidence": 0.9659
}
📊 Results

Achieved strong performance on validation dataset
Handles multi-class tumor classification
Model shows high confidence in predictions

🧪 Future Improvements

🔬 Integration with real hospital datasets
📊 Explainable AI (Grad-CAM visualization)
🧾 Automated medical report generation
☁️ Cloud deployment (AWS / Azure)
📱 Mobile application integration

⚠️ Disclaimer

This project is for educational and research purposes only.
It is not intended for clinical or medical use.

👨‍💻 Author

Rohith J
Zain Moosaraza
Priyanka Sharma

⭐ Acknowledgements

Medical imaging datasets (public sources)
PyTorch community
Open-source contributors
