import './RightPanelInterface.css';
import { useParams } from 'react-router-dom';
export default function ActionHistoryPanel({ actions }) {
  const {story_id,profile_id} = useParams();
  return (
    <div className="action-panel">
      <div className="action-panel-header">
        <h3>Consequences</h3>
      </div>

      <div className="action-list">
        {actions.map((action) => (
          <div
            key={action.id}
            className={`action-card ${action.type}`}
          >
            <div className="action-card-header">
              <span className="action-title">
                {action.title}
              </span>

              <span
                className={`action-value ${
                  action.value > 0
                    ? 'positive'
                    : 'negative'
                }`}
              >
                {action.value > 0
                  ? `+${action.value}`
                  : action.value}
              </span>
            </div>

            <div className="action-meta">
              {action.category} • {action.skill}
            </div>

            <div className="action-text">
              {action.action}
            </div>

            <div className="action-reasoning">
              {action.reasoning}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}