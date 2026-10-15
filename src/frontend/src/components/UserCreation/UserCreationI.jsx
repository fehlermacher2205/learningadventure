import { useState } from 'react';
import './UserCreationI.css'; 
import { registerUserAPI } from '@api/user';

import { useNavigate } from "react-router-dom";
export default function UserCreationInterface() {
  const navigate = useNavigate();
  const [matriculation_number, setMatriculationNumber] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const usernameRegex = /^[a-zA-Z0-9_-]+$/;

  const handleMatriculationChange = (e) => {
    const value = e.target.value;

    if (/^\d*$/.test(value)) {
      setMatriculationNumber(value);
      setError('');
    }
  };

  const validateForm = () => {
    if (!matriculation_number || !username || !password) {
      return "Please fill in all fields.";
    }

    if (matriculation_number.length !== 7) {
      return "Matriculation number must be exactly 7 digits.";
    }

    if (!usernameRegex.test(username)) {
      return "Username can only contain letters, numbers, _ and -.";
    }

    if (username.length < 3 || username.length > 20) {
      return "Username must be between 3 and 20 characters.";
    }

    if (password.length < 8) {
      return "Password must be at least 8 characters long.";
    }

    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);

    try {
      const data = await registerUserAPI({
        matriculation_number,
        username,
        password
      });

      console.log("User created:", data);

      setMatriculationNumber('');
      setUsername('');
      setPassword('');
      setError('');


      navigate("/");

    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to create user");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="creation-container">
      <header className="creation-header">
        <h1>Create New User</h1>
        <p>Please enter the student's details below.</p>
      </header>

      <form className="creation-form" onSubmit={handleSubmit}>
        

        <div className="input-group">
          <label htmlFor="matriculation_number">Matriculation Number</label>
          <input
            id="matriculation_number"
            type="text"
            placeholder="e.g., 1234567"
            value={matriculation_number}
            onChange={handleMatriculationChange}
            maxLength={7}
          />
        </div>

        {/* Username */}
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            placeholder="letters, numbers, _ or -"
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              setError('');
            }}
          />
        </div>

        {/* Password */}
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="At least 8 characters"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setError('');
            }}
          />
        </div>

        {/* Error */}
        {error && <p className="error-text">{error}</p>}

        {/* Submit */}
        <button 
          type="submit" 
          className="submit-button"
          disabled={isLoading}
        >
          {isLoading ? "Creating..." : "Create User"}
        </button>

      </form>
    </div>
  );
}