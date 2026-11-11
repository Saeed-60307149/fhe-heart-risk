// Plain-language form fields (code/data/DATA_DICTIONARY.md). Order must match the model's
// feature_names; app.js checks this against GET /api/model/:dataset.
export const FIELDS = {
  cleveland: [
    { name: 'age', label: 'Age', hint: 'years', type: 'number', min: 18, max: 100, step: 1, example: 57 },
    { name: 'sex', label: 'Sex', type: 'select', options: [[1, 'Male'], [0, 'Female']], example: 1 },
    { name: 'cp', label: 'Chest pain type', type: 'select', options: [[1, 'Typical angina'], [2, 'Atypical angina'], [3, 'Non-anginal pain'], [4, 'No chest pain (asymptomatic)']], example: 4 },
    { name: 'trestbps', label: 'Resting blood pressure', hint: 'mm Hg', type: 'number', min: 80, max: 220, step: 1, example: 140 },
    { name: 'chol', label: 'Cholesterol', hint: 'mg/dl', type: 'number', min: 100, max: 600, step: 1, example: 241 },
    { name: 'fbs', label: 'Fasting blood sugar above 120 mg/dl', type: 'select', options: [[0, 'No'], [1, 'Yes']], example: 0 },
    { name: 'restecg', label: 'Resting ECG', type: 'select', options: [[0, 'Normal'], [1, 'ST-T wave abnormality'], [2, 'Left ventricular hypertrophy']], example: 1 },
    { name: 'thalach', label: 'Maximum heart rate reached', hint: 'beats per minute', type: 'number', min: 60, max: 220, step: 1, example: 123 },
    { name: 'exang', label: 'Chest pain during exercise', type: 'select', options: [[0, 'No'], [1, 'Yes']], example: 1 },
    { name: 'oldpeak', label: 'ST depression after exercise', hint: 'mm, e.g. 0.0 - 6.2', type: 'number', min: 0, max: 7, step: 0.1, example: 0.2 },
    { name: 'slope', label: 'Slope of peak exercise ST segment', type: 'select', options: [[1, 'Upsloping'], [2, 'Flat'], [3, 'Downsloping']], example: 2 },
    { name: 'ca', label: 'Major vessels seen on fluoroscopy', hint: '0 - 3', type: 'select', options: [[0, '0'], [1, '1'], [2, '2'], [3, '3']], example: 0 },
    { name: 'thal', label: 'Thallium stress test', type: 'select', options: [[3, 'Normal'], [6, 'Fixed defect'], [7, 'Reversible defect']], example: 7 },
  ],
  // The public copy of the Edinburgh data names its 9 binary items x1..x9 only.
  edinburgh: Array.from({ length: 9 }, (_, i) => ({
    name: `x${i + 1}`, label: `Clinical item x${i + 1}`, hint: 'present?', type: 'select', options: [[0, 'No'], [1, 'Yes']], example: i % 2,
  })),
};
