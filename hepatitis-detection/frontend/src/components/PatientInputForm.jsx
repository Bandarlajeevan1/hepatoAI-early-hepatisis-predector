/**
 * PatientInputForm Component
 * Collects patient medical data and submits for prediction
 */
import React, { useState } from 'react';
import './PatientInputForm.css';

const PatientInputForm = ({ onSubmit, loading, modelReady = true }) => {
  const [formData, setFormData] = useState({
    age: '',
    sex: '',
    steroid: '',
    antivirals: '',
    fatigue: '',
    malaise: '',
    anorexia: '',
    liver_big: '',
    liver_firm: '',
    spleen_palpable: '',
    spider_web: '',
    ascites: '',
    varices: '',
    histology: '',
    bilirubin: '',
    alk_phosphatase: '',
    sgot: '',
    sgpt: '',
    albumin: '',
    protime: '',
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: null,
      });
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Required fields
    if (!formData.age || parseFloat(formData.age) < 0 || parseFloat(formData.age) > 100) {
      newErrors.age = 'Age must be between 0 and 100';
    }
    if (!formData.sex) {
      newErrors.sex = 'Sex is required';
    }

    // Numeric fields validation
    const numericFields = ['bilirubin', 'alk_phosphatase', 'sgot', 'sgpt', 'albumin', 'protime']; // histology handled separately
    numericFields.forEach((field) => {
      if (formData[field] && parseFloat(formData[field]) < 0) {
        newErrors[field] = 'Value cannot be negative';
      }
    });

    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = validateForm();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Convert string values to numbers where appropriate
    const processedData = {};
    Object.keys(formData).forEach((key) => {
      if (formData[key] === '') {
        processedData[key] = null;
      } else if (['age', 'sex', 'steroid', 'antivirals', 'fatigue', 'malaise', 'anorexia', 'liver_big', 'liver_firm', 'spleen_palpable', 'spider_web', 'ascites', 'varices', 'histology'].includes(key)) {
        processedData[key] = parseInt(formData[key], 10) || null;
      } else {
        processedData[key] = parseFloat(formData[key]) || null;
      }
    });

    onSubmit(processedData);
  };

  const resetForm = () => {
    setFormData({
      age: '',
      sex: '',
      steroid: '',
      antivirals: '',
      fatigue: '',
      malaise: '',
      anorexia: '',
      liver_big: '',
      liver_firm: '',
      spleen_palpable: '',
      spider_web: '',
      ascites: '',
      varices: '',
      bilirubin: '',
      alk_phosphatase: '',
      sgot: '',
      sgpt: '',
      albumin: '',
      protime: '',
    });
    setErrors({});
  };

  return (
    <div className="form-container">
      <h2>Patient Information</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h3>Demographics</h3>
          <div className="form-group">
            <label htmlFor="age">Age *</label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              placeholder="Enter age (0-100)"
              min="0"
              max="100"
              required
            />
            {errors.age && <span className="error">{errors.age}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="sex">Sex *</label>
            <select id="sex" name="sex" value={formData.sex} onChange={handleChange} required>
              <option value=""></option>
              <option value="1">Male</option>
              <option value="2">Female</option>
            </select>
            <small className="select-hint">Please select one option</small>
            {errors.sex && <span className="error">{errors.sex}</span>}
          </div>
        </div>

        <div className="form-section">
          <h3>Symptoms</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="fatigue">Fatigue</label>
              <select id="fatigue" name="fatigue" value={formData.fatigue} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Mild</option>
                <option value="2">Severe</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="malaise">Malaise</label>
              <select id="malaise" name="malaise" value={formData.malaise} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="anorexia">Anorexia</label>
              <select id="anorexia" name="anorexia" value={formData.anorexia} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Clinical Findings</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="liver_big">Liver Enlargement</label>
              <select id="liver_big" name="liver_big" value={formData.liver_big} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="liver_firm">Liver Firmness</label>
              <select id="liver_firm" name="liver_firm" value={formData.liver_firm} onChange={handleChange}>
                <option value=""></option>
                <option value="0">Normal</option>
                <option value="1">Firm</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="spleen_palpable">Spleen Palpable</label>
              <select id="spleen_palpable" name="spleen_palpable" value={formData.spleen_palpable} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="spider_web">Spider Web Veins</label>
              <select id="spider_web" name="spider_web" value={formData.spider_web} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="ascites">Ascites</label>
              <select id="ascites" name="ascites" value={formData.ascites} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="varices">Esophageal Varices</label>
              <select id="varices" name="varices" value={formData.varices} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="histology">Histology (biopsy)</label>
              <select id="histology" name="histology" value={formData.histology} onChange={handleChange}>
                <option value=""></option>
                <option value="0">Not available/Normal</option>
                <option value="1">Abnormal</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Treatment</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="steroid">Steroid Usage</label>
              <select id="steroid" name="steroid" value={formData.steroid} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
                <option value="2">Previous</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>

            <div className="form-group">
              <label htmlFor="antivirals">Antiviral Treatment</label>
              <select id="antivirals" name="antivirals" value={formData.antivirals} onChange={handleChange}>
                <option value=""></option>
                <option value="0">No</option>
                <option value="1">Yes</option>
                <option value="2">Previous</option>
              </select>
              <small className="select-hint">Please select one option</small>
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Laboratory Values</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="bilirubin">Bilirubin (mg/dL)</label>
              <input
                type="number"
                id="bilirubin"
                name="bilirubin"
                value={formData.bilirubin}
                onChange={handleChange}
                placeholder="0.0"
                step="0.1"
                min="0"
              />
              {errors.bilirubin && <span className="error">{errors.bilirubin}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="alk_phosphatase">Alk. Phosphatase (U/L)</label>
              <input
                type="number"
                id="alk_phosphatase"
                name="alk_phosphatase"
                value={formData.alk_phosphatase}
                onChange={handleChange}
                placeholder="0"
                step="1"
                min="0"
              />
              {errors.alk_phosphatase && <span className="error">{errors.alk_phosphatase}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="sgot">SGOT (U/L)</label>
              <input
                type="number"
                id="sgot"
                name="sgot"
                value={formData.sgot}
                onChange={handleChange}
                placeholder="0"
                step="1"
                min="0"
              />
              {errors.sgot && <span className="error">{errors.sgot}</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="sgpt">SGPT (U/L)</label>
              <input
                type="number"
                id="sgpt"
                name="sgpt"
                value={formData.sgpt}
                onChange={handleChange}
                placeholder="0"
                step="1"
                min="0"
              />
              {errors.sgpt && <span className="error">{errors.sgpt}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="albumin">Albumin (g/dL)</label>
              <input
                type="number"
                id="albumin"
                name="albumin"
                value={formData.albumin}
                onChange={handleChange}
                placeholder="0.0"
                step="0.1"
                min="0"
              />
              {errors.albumin && <span className="error">{errors.albumin}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="protime">Prothrombin Time (sec)</label>
              <input
                type="number"
                id="protime"
                name="protime"
                value={formData.protime}
                onChange={handleChange}
                placeholder="0"
                step="1"
                min="0"
              />
              {errors.protime && <span className="error">{errors.protime}</span>}
            </div>
          </div>
        </div>

        <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading || !modelReady}
                title={!modelReady ? 'Model not trained. Run backend/train.py and restart the server.' : ''}
              >
                {loading ? 'Analyzing...' : 'Get Prediction'}
              </button>
          <button type="button" className="btn btn-secondary" onClick={resetForm} disabled={loading}>
            Clear Form
          </button>
        </div>
      </form>
      {!modelReady && (
        <div className="model-warning" style={{marginTop: '12px', color: '#b91c1c'}}>
          ⚠ Model not available: please train the ML model on the backend.
          Run: <strong>python backend/train.py</strong> and restart the API server.
        </div>
      )}
    </div>
  );
};

export default PatientInputForm;
