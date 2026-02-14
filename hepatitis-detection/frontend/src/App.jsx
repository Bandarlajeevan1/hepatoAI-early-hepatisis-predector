/**
 * Main App Component
 * Root component that combines all features with Authentication
 */
import React, { useState, useCallback, useEffect } from 'react';
import './App.css';
import PatientInputForm from './components/PatientInputForm';
import PredictionResult from './components/PredictionResult';
import HistoryDashboard from './components/HistoryDashboard';
import Login from './components/Login';
import Register from './components/Register';
import ApiService from './services/apiClient';

function App() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
  const [user, setUser] = useState(null);
  const [authToken, setAuthToken] = useState(null);

  // App state
  const [predictionResult, setPredictionResult] = useState(null);
  const [currentPatientData, setCurrentPatientData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('predict');
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [apiHealth, setApiHealth] = useState(null);

  // Check if user is already logged in (check localStorage)
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setAuthToken(token);
      setUser(JSON.parse(userData));
      setIsAuthenticated(true);
      checkApiHealth();
    }
  }, []);

  const checkApiHealth = async () => {
    const result = await ApiService.getHealth();
    if (result.success) {
      setApiHealth(result.data);
    } else {
      setApiHealth({ status: 'offline' });
    }
  };

  const handleLoginSuccess = (userData, token) => {
    setUser(userData);
    setAuthToken(token);
    setIsAuthenticated(true);
    checkApiHealth();
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setUser(null);
    setAuthToken(null);
    setIsAuthenticated(false);
    setAuthMode('login');
    setPredictionResult(null);
    setActiveTab('predict');
  };

  const handlePredictionSubmit = async (patientData) => {
    setLoading(true);
    setError(null);
    setPredictionResult(null);

    const result = await ApiService.predict(patientData);

    if (result.success) {
      setPredictionResult(result.data);
      setCurrentPatientData(patientData);
      setError(null);
    } else {
      setError(result.error);
      setPredictionResult(null);
    }

    setLoading(false);
  };

  const handlePredictionSaved = useCallback(() => {
    // Trigger history refresh
    setRefreshTrigger((prev) => prev + 1);
    // Show success message
    setActiveTab('history');
  }, []);

  // Show login/register if not authenticated
  if (!isAuthenticated) {
    if (authMode === 'login') {
      return (
        <Login
          onLoginSuccess={handleLoginSuccess}
          onSwitchToRegister={() => setAuthMode('register')}
        />
      );
    } else {
      return (
        <Register
          onRegisterSuccess={() => setAuthMode('login')}
          onSwitchToLogin={() => setAuthMode('login')}
        />
      );
    }
  }

  // Main app interface
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <h1 className="app-title">🏥 Hepatitis Detection</h1>
            <p className="app-subtitle">
              Hybrid ML Ensemble (MSEM with FL-KNN & HDPSO)
            </p>
          </div>

          <div className="header-info">
            <div className="user-info">
              <span>Welcome, <strong>{user?.full_name || user?.email}</strong></span>
            </div>
            <div className="header-status">
              <div className={`api-status ${apiHealth?.status || 'offline'}`}>
                <span className="status-indicator" />
                {apiHealth?.status === 'healthy'
                  ? 'API: Online'
                  : apiHealth?.model_loaded
                  ? 'API: Ready'
                  : 'API: Offline'}
              </div>
            </div>
            <button className="logout-button" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>

      <nav className="tab-navigation">
        <button
          className={`nav-tab ${activeTab === 'predict' ? 'active' : ''}`}
          onClick={() => setActiveTab('predict')}
        >
          📋 Make Prediction
        </button>
        <button
          className={`nav-tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📊 View History
        </button>
        <button
          className={`nav-tab ${activeTab === 'about' ? 'active' : ''}`}
          onClick={() => setActiveTab('about')}
        >
          ℹ️ About
        </button>
      </nav>

      <main className="app-main">
        {/* Error Alert */}
        {error && (
          <div className="alert alert-error">
            <span className="alert-icon">✗</span>
            <div className="alert-content">
              <strong>Error:</strong> {error}
            </div>
            <button className="alert-close" onClick={() => setError(null)}>
              ×
            </button>
          </div>
        )}

        {/* Prediction Tab */}
        {activeTab === 'predict' && (
          <div className="tab-content">
            <PatientInputForm onSubmit={handlePredictionSubmit} loading={loading} />
            {predictionResult && (
              <PredictionResult
                prediction={predictionResult}
                inputData={currentPatientData}
                onSaved={handlePredictionSaved}
              />
            )}
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className="tab-content">
            <HistoryDashboard refreshTrigger={refreshTrigger} />
          </div>
        )}

        {/* About Tab */}
        {activeTab === 'about' && (
          <div className="tab-content">
            <div className="about-card">
              <h2>About This Application</h2>

              <section className="about-section">
                <h3>📖 Overview</h3>
                <p>
                  This application uses a hybrid machine learning ensemble system to predict
                  hepatitis status based on patient medical data. The model combines state-of-the-art
                  techniques including Fuzzy Logic k-Nearest Neighbors (FL-KNN) imputation,
                  Hybrid Dingo Particle Swarm Optimization (HDPSO) feature selection, and
                  Multistage Ensemble Model (MSEM) for classification.
                </p>
              </section>

              <section className="about-section">
                <h3>🤖 Machine Learning Pipeline</h3>
                <ul>
                  <li>
                    <strong>FL-KNN Imputation:</strong> Intelligently handles missing values using
                    fuzzy logic and k-nearest neighbors
                  </li>
                  <li>
                    <strong>HDPSO Feature Selection:</strong> Optimizes feature selection using
                    hybrid dingo and particle swarm optimization algorithms
                  </li>
                  <li>
                    <strong>MSEM Ensemble:</strong> Combines predictions from:
                    <ul>
                      <li>Random Forest Classifier</li>
                      <li>Support Vector Machine (SVM)</li>
                      <li>Logistic Regression</li>
                      <li>XGBoost</li>
                    </ul>
                  </li>
                  <li>
                    <strong>Meta-learner:</strong> Stacking with Logistic Regression for optimal
                    ensemble combination
                  </li>
                </ul>
              </section>

              <section className="about-section">
                <h3>⚠️ Important Disclaimer</h3>
                <p>
                  <strong>
                    This application is for research and clinical support purposes only. It is NOT
                    a substitute for professional medical advice, diagnosis, or treatment. Always
                    consult with qualified healthcare professionals for medical decisions.
                  </strong>
                </p>
              </section>

              <section className="about-section">
                <h3>📊 Risk Level Classification</h3>
                <div className="risk-levels">
                  <div className="risk-level-card low">
                    <h4>Low Risk (0.0 - 0.3)</h4>
                    <p>Low probability of hepatitis. Regular monitoring recommended.</p>
                  </div>
                  <div className="risk-level-card medium">
                    <h4>Medium Risk (0.3 - 0.7)</h4>
                    <p>Moderate probability. Further clinical evaluation recommended.</p>
                  </div>
                  <div className="risk-level-card high">
                    <h4>High Risk (0.7 - 1.0)</h4>
                    <p>High probability. Immediate medical attention required.</p>
                  </div>
                </div>
              </section>

              <section className="about-section">
                <h3>💡 How to Use</h3>
                <ol>
                  <li>
                    Go to the <strong>Make Prediction</strong> tab
                  </li>
                  <li>Enter patient medical data (required: age and sex)</li>
                  <li>
                    Click <strong>Get Prediction</strong> to analyze the data
                  </li>
                  <li>
                    Review the prediction result, risk level, and detailed probabilities
                  </li>
                  <li>
                    Optionally save the prediction to the database with a patient ID
                  </li>
                  <li>
                    Use the <strong>View History</strong> tab to see all saved predictions
                  </li>
                </ol>
              </section>

              <section className="about-section">
                <h3>🔧 Technical Details</h3>
                <table className="tech-table">
                  <tbody>
                    <tr>
                      <td>
                        <strong>Backend Framework:</strong>
                      </td>
                      <td>Flask (Python)</td>
                    </tr>
                    <tr>
                      <td>
                        <strong>Frontend Framework:</strong>
                      </td>
                      <td>React (JavaScript)</td>
                    </tr>
                    <tr>
                      <td>
                        <strong>Database:</strong>
                      </td>
                      <td>MongoDB</td>
                    </tr>
                    <tr>
                      <td>
                        <strong>ML Libraries:</strong>
                      </td>
                      <td>scikit-learn, XGBoost, NumPy, Pandas</td>
                    </tr>
                    <tr>
                      <td>
                        <strong>API Documentation:</strong>
                      </td>
                      <td>Swagger/OpenAPI at /apidocs</td>
                    </tr>
                  </tbody>
                </table>
              </section>

              <section className="about-section">
                <h3>📞 Support</h3>
                <p>
                  For issues, questions, or feedback, please visit the project repository or contact
                  the development team.
                </p>
              </section>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          ⚕️ <strong>Hepatitis Detection System</strong> | Research & Clinical Support Tool
        </p>
        <p>
          Built with using Flask, React, and Machine Learning
        </p>
        <p className="disclaimer">
          <strong>Disclaimer:</strong> For research purposes only. Not a substitute for professional
          medical advice.
        </p>
      </footer>
    </div>
  );
}

export default App;
