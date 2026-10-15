import { useState } from "react";
import "./Global.css";
import { loginUserAPI } from "@api/user";
import { useNavigate } from "react-router-dom";

export default function UserLoginModal({ onClose }) {
  const [matriculation_number, setMatriculationNumber] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleMatriculationChange = (e) => {
    const value = e.target.value;
    if (/^\d*$/.test(value)) {
      setMatriculationNumber(value);
      setError("");
    }
  };

  const validateForm = () => {
    if (!matriculation_number || !password) {
      return "Please fill in all fields.";
    }
    if (matriculation_number.length !== 7) {
      return "Matriculation number must be exactly 7 digits.";
    }
    if (password.length < 8) {
      return "Password must be at least 8 characters long.";
    }
    return null;
  };

  const handleRegister = () => {
    onClose();
    navigate("/register");
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
      await loginUserAPI({
        matriculation_number,
        password,
      });

      window.dispatchEvent(new Event("authChanged"));

      onClose();
      navigate("/");

    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to log in user");
    } finally {
      
      setIsLoading(false);
      window.location.reload();
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">

        <button className="modal-close" onClick={onClose}>
          ✕
        </button>

        <h2>Login</h2>
        <p>Please enter your credentials below.</p>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Matriculation Number</label>
            <input
              type="text"
              placeholder="e.g., 1234567"
              value={matriculation_number}
              onChange={handleMatriculationChange}
              maxLength={7}
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="At least 8 characters"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError("");
              }}
            />
          </div>

          {error && <p className="error-text">{error}</p>}

          <div className="button-row">
            <button
              type="button"
              className="secondary-submit-button"
              onClick={handleRegister}
            >
              Register
            </button>

            <button
              type="submit"
              className="submit-button"
              disabled={isLoading}
            >
              {isLoading ? "Logging in..." : "Login"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}