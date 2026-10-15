import { useState } from 'react';
import './GoalsInterface.css';
import { addGoalToProfile } from '../../api/profile';
import { useParams } from "react-router-dom";

export default function GoalsInterface() {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [skill, setSkill] = useState('');
  const [level, setLevel] = useState('');
  const [skill_score, setSkillScore] = useState('');
  const { session_id } = useParams();

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleNumberInput = (setter) => (e) => {
    const value = e.target.value;
    if (/^\d*$/.test(value)) {
      setter(value);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // reset messages
    setError('');
    setSuccess('');

    if (
      !title.trim() ||
      !category.trim() ||
      !skill.trim() ||
      !level.trim() ||
      !skill_score
    ) {
      setError('Please fill in all fields.');
      return;
    }

    setIsLoading(true);

    try {
      const data = await addGoalToProfile(session_id, {
        title,
        category,
        skill,
        level,
        skill_score: Number(skill_score), // ✅ fix type
      });

      console.log('Goal created:', data);

      // Reset form
      setTitle('');
      setCategory('');
      setSkill('');
      setLevel('');
      setSkillScore('');

      // ✅ success message
      setSuccess('Goal created successfully!');

      // auto-hide after 3s
      setTimeout(() => {
        setSuccess('');
      }, 3000);

    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to create goal');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="goals-container">
      <header className="goals-header">
        <h1>Create New Goal</h1>
        <p>Define a new learning goal below.</p>
      </header>

      <form className="goals-form" onSubmit={handleSubmit}>

        <div className="input-group">
          <label>Title</label>
          <input
            type="text"
            placeholder="Goal title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Category</label>
          <input
            type="text"
            placeholder="e.g., Programming"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Skill</label>
          <input
            type="text"
            placeholder="e.g., React"
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Level</label>
          <input
            type="text"
            placeholder="e.g., Beginner / Intermediate"
            value={level}
            onChange={(e) => setLevel(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Skill Score</label>
          <input
            type="text"
            placeholder="0 - 100"
            value={skill_score}
            onChange={handleNumberInput(setSkillScore)}
          />
        </div>

        {/* ✅ messages */}
        {error && <p className="error-text">{error}</p>}
        {success && <p className="success-text">{success}</p>}

        <button
          type="submit"
          className="submit-button"
          disabled={isLoading}
        >
          {isLoading ? 'Creating...' : 'Create Goal'}
        </button>
      </form>
    </div>
  );
}