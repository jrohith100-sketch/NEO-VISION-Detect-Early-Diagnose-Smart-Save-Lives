
function setupPreview(inputId, previewId) {
  document.getElementById(inputId).addEventListener("change", function(e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(event) {
        const imgElement = document.getElementById(previewId);
        imgElement.src = event.target.result;
        imgElement.style.display = "block";
        imgElement.previousElementSibling.style.display = "none";
      };
      reader.readAsDataURL(file);
    }
  });
}

setupPreview("ct", "ctPreview");
setupPreview("mri", "mriPreview");


document.getElementById("uploadForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const btn = document.getElementById("submitBtn");
  btn.innerText = "Analyzing Neural Networks...";
  btn.disabled = true;

 
  const bloodReport = {
    Hb: parseFloat(document.getElementById("hb").value) || null,
    WBC: parseFloat(document.getElementById("wbc").value) || null,
    Neutrophils: parseFloat(document.getElementById("neutrophils").value) || null,
    Lymphocytes: parseFloat(document.getElementById("lymphocytes").value) || null,
    Platelets: parseFloat(document.getElementById("platelets").value) || null,
    CRP: parseFloat(document.getElementById("crp").value) || null,
    ESR: parseFloat(document.getElementById("esr").value) || null,
    Glucose: parseFloat(document.getElementById("glucose").value) || null,
    Creatinine: parseFloat(document.getElementById("creatinine").value) || null,
    Sodium: parseFloat(document.getElementById("sodium").value) || null,
    Prolactin: parseFloat(document.getElementById("prolactin").value) || null,
    ACTH: parseFloat(document.getElementById("acth").value) || null,
    Cortisol: parseFloat(document.getElementById("cortisol").value) || null,
    TSH: parseFloat(document.getElementById("tsh").value) || null,
    FreeT4: parseFloat(document.getElementById("freet4").value) || null,
    IGF1: parseFloat(document.getElementById("igf1").value) || null
  };

  const formData = new FormData();
  formData.append("ct_image", document.getElementById("ct").files[0]);
  formData.append("mri_image", document.getElementById("mri").files[0]);
  formData.append("patient_age", document.getElementById("age").value);
  formData.append("patient_sex", document.getElementById("sex").value);
  formData.append("blood_report", JSON.stringify(bloodReport));

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    const resultCard = document.getElementById("resultCard");
    resultCard.classList.remove("hidden");

    let displayDiagnosis = data.diagnosis;
    if (displayDiagnosis.toLowerCase().includes("notumour")) {
      displayDiagnosis = "Negative (No Tumor Detected)";
    }

    document.getElementById("resultContent").innerHTML = `
      <div style="font-size: 1.1rem;">
        <strong>Diagnosis:</strong> 
        <span style="color:var(--primary)">${displayDiagnosis}</span><br>
        <strong>Malignancy Risk:</strong> ${data.malignancy_assessment}<br>
        <strong>Blood Red Flags:</strong> ${data.blood_red_flags} detected
      </div>
    `;

    
    const classNames = ["Glioma", "Meningioma", "Pituitary", "Notumour"];

    let probHTML = `
      <div style="margin-top:20px; border-top:1px solid #eee; padding-top:20px;">
        <p style="font-weight:700; font-size:0.85rem; color:var(--text-muted); margin-bottom:15px;">
          MODEL CONFIDENCE
        </p>
    `;

    classNames.forEach(name => {
      const prob = data.mri_prediction_percentages[name] || 0;
      const isPredicted = data.diagnosis === name;

      probHTML += `
        <div style="margin-bottom: 12px;">
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:600; margin-bottom:4px;">
            <span>${isPredicted ? "▶ " : ""}${name}</span>
            <span>${prob}%</span>
          </div>
          <div style="background:#e2e8f0; border-radius:10px; height:6px; overflow:hidden;">
            <div style="
              background:${isPredicted ? 'var(--primary)' : '#94a3b8'};
              width:${prob}%;
              height:100%;
              border-radius:10px;
              transition: width 1s ease;">
            </div>
          </div>
        </div>
      `;
    });

    probHTML += `</div>`;
    document.getElementById("probabilities").innerHTML = probHTML;

  } catch (error) {
    alert("Connection to Server Failed. Please ensure the backend is running.");
  } finally {
    btn.innerText = "Run Diagnostic Analysis";
    btn.disabled = false;
  }
});
