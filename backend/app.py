from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import numpy as np
import json
from torchvision import transforms

from models import load_ct_model, load_mri_model, load_fusion_model


app = FastAPI(title="Neovision – Multimodal Tumor Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = "cpu"



ct_model = load_ct_model("models/best_ct_model_3ch.pth")
mri_model = load_mri_model("models/resnet18_model.pth")
fusion_model = load_fusion_model("models/final_fusion_model.pth")



FUSION_LABELS = ["Glioma", "Meningioma", "Notumour", "Pituitary"]


transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])



def predict_image(model, image):
    img = transform(image).unsqueeze(0)
    with torch.no_grad():
        out = model(img)
        probs = torch.softmax(out, dim=1)
    return probs.numpy()[0]


def generate_binary_flags(raw_values: dict, sex: str):
    sex = sex.lower()
    binary_flags = []

  
    def get(key):
        return raw_values.get(key, None)

    val = get("Hb")
    if val is not None:
        binary_flags.append(
            1 if (sex == "male" and val < 13.0) or (sex == "female" and val < 12.0) else 0
        )

    val = get("WBC")
    if val is not None:
        binary_flags.append(1 if val > 12.0 else 0)

  
    val = get("Neutrophils")
    if val is not None:
        binary_flags.append(1 if val > 75 else 0)

  
    val = get("Lymphocytes")
    if val is not None:
        binary_flags.append(1 if val < 20 else 0)

   
    val = get("Platelets")
    if val is not None:
        binary_flags.append(1 if val > 400 else 0)

   
    val = get("CRP")
    if val is not None:
        binary_flags.append(1 if val > 5.0 else 0)

    val = get("ESR")
    if val is not None:
        esr_upper = 15 if sex == "male" else 20
        binary_flags.append(1 if val > esr_upper else 0)

    val = get("Glucose")
    if val is not None:
        binary_flags.append(1 if val > 140 else 0)

    val = get("Creatinine")
    if val is not None:
        binary_flags.append(
            1 if (sex == "male" and val > 1.3) or (sex == "female" and val > 1.1) else 0
        )

  
    val = get("Sodium")
    if val is not None:
        binary_flags.append(1 if val < 135 or val > 145 else 0)

    
    val = get("Prolactin")
    if val is not None:
        if sex == "male":
            binary_flags.append(1 if val < 2 or val > 18 else 0)
        else:
            binary_flags.append(1 if val < 2 or val > 29 else 0)

    
    val = get("ACTH")
    if val is not None:
        binary_flags.append(1 if val < 7 or val > 63 else 0)

   
    val = get("Cortisol")
    if val is not None:
        binary_flags.append(1 if val < 6 or val > 23 else 0)

   
    val = get("TSH")
    if val is not None:
        binary_flags.append(1 if val < 0.4 or val > 4.0 else 0)

    
    val = get("FreeT4")
    if val is not None:
        binary_flags.append(1 if val < 0.8 or val > 1.8 else 0)

    
    val = get("IGF1")
    if val is not None:
        binary_flags.append(1 if val < 100 or val > 300 else 0)

    return binary_flags



def assess_malignancy_risk(diagnosis: str, red_flag_count: int):
    
    if diagnosis == "Notumour":
        return "Notumor"

    if red_flag_count <= 2:
        return "Benign – Low Risk"

    elif red_flag_count <= 5:
        return "Malignant – Moderate Risk"

    else:
        return "Malignant – High Risk"




@app.post("/predict")
async def predict(
    ct_image: UploadFile = File(...),   
    mri_image: UploadFile = File(...),
    patient_age: int = Form(...),
    patient_sex: str = Form(...),
    blood_report: str = Form(...)
):
    
    mri_img = Image.open(mri_image.file).convert("RGB")

    
    mri_probs = predict_image(mri_model, mri_img)   # (4,)

    
    mri_index = int(np.argmax(mri_probs))
    diagnosis = FUSION_LABELS[mri_index]
    mri_conf = float(mri_probs[mri_index])

   
    mri_prediction_percentages = {
    "Glioma": round(float(mri_probs[0]) * 100, 2),
    "Meningioma": round(float(mri_probs[1]) * 100, 2),
    "Notumour": round(float(mri_probs[2]) * 100, 2),
    "Pituitary": round(float(mri_probs[3]) * 100, 2)
}


    blood_dict = json.loads(blood_report)
    blood_flags = generate_binary_flags(blood_dict, patient_sex)
    red_flag_count = sum(blood_flags)

    malignancy_assessment = assess_malignancy_risk(diagnosis, red_flag_count)


    if malignancy_assessment:
     display_diagnosis = f"{diagnosis} ({malignancy_assessment})"
    else:
     display_diagnosis = diagnosis

    return {
        "prediction_model": "Brain Tumor Classifier",
        "diagnosis": diagnosis,
        "malignancy_assessment": malignancy_assessment,
        "mri_confidence": round(mri_conf, 3),
        "mri_prediction_percentages": mri_prediction_percentages,
        "blood_red_flags": red_flag_count,
        "total_blood_markers": len(blood_flags)
    }

   

