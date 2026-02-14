/**
 * PredictionResult Component
 * Displays the prediction result with risk assessment
 */
import React, { useState } from 'react';
import './PredictionResult.css';
import ApiService from '../services/apiClient';

const PredictionResult = ({ prediction, inputData, onSaved }) => {
  const [saving, setSaving] = useState(false);
  const [patientId, setPatientId] = useState('');
  const [saveStatus, setSaveStatus] = useState(null);

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'Low':
        return '#10b981';
      case 'Medium':
        return '#f59e0b';
      case 'High':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel) {
      case 'Low':
        return '✓';
      case 'Medium':
        return '⚠';
      case 'High':
        return '!';
      default:
        return 'i';
    }
  };

  const handleSavePrediction = async () => {
    if (!prediction) return;

    setSaving(true);
    setSaveStatus(null);

    const dataToSave = {
      patient_id: patientId || 'ANON',
      prediction: prediction.prediction,
      confidence: prediction.confidence,
      risk_level: prediction.risk_level,
      input_data: inputData,
    };

    const result = await ApiService.savePrediction(dataToSave);

    if (result.success) {
      setSaveStatus({
        type: 'success',
        message: `✓ Prediction saved successfully (ID: ${result.data.record_id})`,
      });
      setPatientId('');
      if (onSaved) {
        onSaved(result.data);
      }
    } else {
      setSaveStatus({
        type: 'error',
        message: `✗ Failed to save: ${result.error}`,
      });
    }

    setSaving(false);
  };

  if (!prediction) {
    return null;
  }

  const riskColor = getRiskColor(prediction.risk_level);
  const riskIcon = getRiskIcon(prediction.risk_level);

  return (
    <div className="result-container">
      <div className="result-card">
        <div className="result-header">
          <h2>Prediction Result</h2>
        </div>

        <div className="prediction-result">
          <div className="prediction-box">
            <div className="prediction-label">
              <span className="prediction-text">Status:</span>
            </div>
            <div className="prediction-value">
              <span className={`status-badge ${prediction.prediction.toLowerCase()}`}>
                {prediction.prediction}
              </span>
            </div>
          </div>

          <div className="confidence-box">
            <div className="prediction-label">
              <span className="prediction-text">Confidence:</span>
            </div>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${prediction.confidence}%` }}
              />
            </div>
            <div className="confidence-text">
              {prediction.confidence.toFixed(2)}%
            </div>
          </div>

          <div className="risk-box" style={{ borderColor: riskColor }}>
            <div className="risk-icon" style={{ color: riskColor }}>
              {riskIcon}
            </div>
            <div className="risk-content">
              <div className="risk-label">Risk Level</div>
              <div className="risk-level" style={{ color: riskColor }}>
                {prediction.risk_level}
              </div>
            </div>
          </div>
        </div>

        <div className="probability-details">
          <h4>Detailed Probabilities</h4>
          <div className="probability-row">
            <span className="prob-label">Negative:</span>
            <span className="prob-value">{prediction.probabilities.negative}%</span>
          </div>
          <div className="probability-row">
            <span className="prob-label">Positive:</span>
            <span className="prob-value">{prediction.probabilities.positive}%</span>
          </div>
        </div>

        <div className="save-section">
          <h4>Save This Prediction</h4>
          <div className="save-form">
            <input
              type="text"
              placeholder="Optional: Patient ID"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              maxLength="50"
            />
            <button
              className="btn btn-save"
              onClick={handleSavePrediction}
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save to Database'}
            </button>
          </div>

          {saveStatus && (
            <div className={`save-status ${saveStatus.type}`}>
              {saveStatus.message}
            </div>
          )}
        </div>

        <div className="interpretation">
          <h4>Interpretation</h4>
          <p className="interpretation-text">
            {prediction.risk_level === 'Low' && (
              <>
                <strong>Low Risk:</strong> The model indicates low probability of hepatitis.
                However, clinical judgment and further medical tests should always be considered.
                Regular monitoring is recommended.
              </>
            )}
            {prediction.risk_level === 'Medium' && (
              <>
                <strong>Medium Risk:</strong> The model indicates moderate probability of hepatitis.
                Further clinical evaluation and laboratory tests are recommended. Consult with a
                healthcare professional for definitive diagnosis.
              </>
            )}
            {prediction.risk_level === 'High' && (
              <>
                <strong>High Risk:</strong> The model indicates high probability of hepatitis.
                Immediate medical attention and comprehensive testing are strongly recommended. This
                should not replace professional medical diagnosis.
              </>
            )}
          </p>
        </div>

        <div className="disclaimer">
          <p>
            <strong>Disclaimer:</strong> This prediction is generated by a machine learning model
            for research and clinical support purposes only. It is not intended to replace professional
            medical diagnosis. Always consult with qualified healthcare professionals for medical advice.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PredictionResult;
