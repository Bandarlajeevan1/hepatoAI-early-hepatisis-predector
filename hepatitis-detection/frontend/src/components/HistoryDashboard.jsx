/**
 * HistoryDashboard Component
 * Displays prediction history with filtering and pagination
 */
import React, { useState, useEffect } from 'react';
import './HistoryDashboard.css';
import ApiService from '../services/apiClient';

const HistoryDashboard = ({ refreshTrigger }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, positive, negative
  const [sortBy, setSortBy] = useState('recent'); // recent, oldest
  const [limit, setLimit] = useState(50);

  useEffect(() => {
    fetchHistory();
  }, [refreshTrigger, limit]);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);

    const result = await ApiService.getHistory(limit);

    if (result.success) {
      setHistory(result.data.records || []);
    } else {
      setError(result.error);
      setHistory([]);
    }

    setLoading(false);
  };

  const filterRecords = () => {
    let filtered = [...history];

    if (filter === 'positive') {
      filtered = filtered.filter((r) => r.prediction === 'Positive');
    } else if (filter === 'negative') {
      filtered = filtered.filter((r) => r.prediction === 'Negative');
    }

    if (sortBy === 'oldest') {
      filtered = filtered.reverse();
    }

    return filtered;
  };

  const filteredHistory = filterRecords();

  const getStatistics = () => {
    const stats = {
      total: history.length,
      positive: history.filter((r) => r.prediction === 'Positive').length,
      negative: history.filter((r) => r.prediction === 'Negative').length,
      avgConfidence:
        history.length > 0
          ? (history.reduce((sum, r) => sum + (r.confidence || 0), 0) / history.length).toFixed(2)
          : 0,
    };
    return stats;
  };

  const stats = getStatistics();

  return (
    <div className="history-container">
      <div className="history-card">
        <div className="history-header">
          <h2>Prediction History</h2>
          <button className="btn btn-refresh" onClick={fetchHistory} disabled={loading}>
            {loading ? '↻ Refreshing...' : '↻ Refresh'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="statistics">
          <div className="stat-item">
            <span className="stat-label">Total Predictions</span>
            <span className="stat-value">{stats.total}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Positive Cases</span>
            <span className="stat-value positive">{stats.positive}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Negative Cases</span>
            <span className="stat-value negative">{stats.negative}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Avg. Confidence</span>
            <span className="stat-value">{stats.avgConfidence}%</span>
          </div>
        </div>

        <div className="controls">
          <div className="control-group">
            <label htmlFor="filter">Filter:</label>
            <select
              id="filter"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="all">All Results</option>
              <option value="positive">Positive Only</option>
              <option value="negative">Negative Only</option>
            </select>
          </div>

          <div className="control-group">
            <label htmlFor="sort">Sort:</label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
              <option value="recent">Most Recent First</option>
              <option value="oldest">Oldest First</option>
            </select>
          </div>

          <div className="control-group">
            <label htmlFor="limit">Records:</label>
            <select value={limit} onChange={(e) => setLimit(parseInt(e.target.value))}>
              <option value={20}>Last 20</option>
              <option value={50}>Last 50</option>
              <option value={100}>Last 100</option>
            </select>
          </div>
        </div>

        {loading && <div className="loading">Loading records...</div>}

        {!loading && filteredHistory.length === 0 ? (
          <div className="empty-state">
            <p>No prediction records found.</p>
            <p>Make a prediction and save it to see history here.</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Patient ID</th>
                  <th>Prediction</th>
                  <th>Risk Level</th>
                  <th>Confidence</th>
                  <th>Date / Time</th>
                </tr>
              </thead>
              <tbody>
                {filteredHistory.map((record, idx) => (
                  <tr key={record._id || idx} className={`row-${record.prediction.toLowerCase()}`}>
                    <td>
                      <span className="patient-id">
                        {record.patient_id || 'Anonymous'}
                      </span>
                    </td>
                    <td>
                      <span className={`badge badge-${record.prediction.toLowerCase()}`}>
                        {record.prediction}
                      </span>
                    </td>
                    <td>
                      <span className={`badge badge-risk-${record.risk_level.toLowerCase()}`}>
                        {record.risk_level}
                      </span>
                    </td>
                    <td>
                      <div className="confidence-small">
                        <div className="confidence-bar-small">
                          <div
                            className="confidence-fill-small"
                            style={{
                              width: `${record.confidence}%`,
                              backgroundColor:
                                record.confidence > 70
                                  ? '#ef4444'
                                  : record.confidence > 40
                                  ? '#f59e0b'
                                  : '#10b981',
                            }}
                          />
                        </div>
                        <span>{record.confidence.toFixed(1)}%</span>
                      </div>
                    </td>
                    <td className="timestamp">
                      {new Date(record.timestamp).toLocaleDateString()}{' '}
                      {new Date(record.timestamp).toLocaleTimeString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {!loading && filteredHistory.length > 0 && (
          <div className="table-footer">
            Showing {filteredHistory.length} of {history.length} records
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryDashboard;
