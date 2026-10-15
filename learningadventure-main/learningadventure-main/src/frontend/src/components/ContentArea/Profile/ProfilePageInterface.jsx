import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ProfileView.css"; 

import { getProfileAPI } from "@api/profile";
import {getUserFromCookiesAPI} from '@api/user'

import { 
  CirclePlus,
  BookPlus,
  BookUser,
  MapPlus,
  Settings,
  SquarePen,
  Search,
  User,
  RotateCcw 
} from 'lucide-react';
export default function ProfileView() {
    const { profile_id } = useParams();
    const navigate = useNavigate();

    // State to hold the fetched data
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [profileName, setProfileName] = useState("");
    const [background, setBackground] = useState("");
    const [goals, setGoals] = useState([]);
    const [questions, setQuestions] = useState([]);
    
    // Optional: Include these if you want to display the internal configuration
    const [questPrompt, setQuestPrompt] = useState("");
    const [pagePrompt, setPagePrompt] = useState("");
    const [goalPrompt, setGoalPrompt] = useState("");
    const [actionPrompt, setActionPrompt] = useState("");
    const [visibility, setVisibility] = useState(-1);
    const [isOwner, setisOwner] = useState(false);
    useEffect(() => {
        async function fetchProfile() {
            try {
                const data = await getProfileAPI(profile_id);
                // Map the response payload to our local state
                setProfileName(data.profile_name || "Unnamed Profile");
                setBackground(data.predefined_background || "No background story provided.");
                setGoals(data.predefined_goals || []);
                setQuestions(data.questions || []);
                
                setQuestPrompt(data.prompt?.quest_prompt || "");
                setPagePrompt(data.prompt?.page_prompt || "");
                setGoalPrompt(data.prompt?.goal_prompt || "");
                setActionPrompt(data.prompt?.action_prompt || "");
                setVisibility(data.visible ?? -1);
                const user = await getUserFromCookiesAPI();
                setisOwner(user.id == data.user_id? true : false);
            } catch (err) {
                console.error("Failed to load profile:", err);
                setError("Failed to load profile data.");
            } finally {
                setLoading(false);
            }
        }

        fetchProfile();
    }, [profile_id]);

    // Helper function to render visibility status
    const getVisibilityLabel = (val) => {
        switch(val) {
            case -1: return "Draft";
            case 0: return "Private";
            case 1: return "Link Only";
            case 2: return "Public";
            default: return "Unknown";
        }
    };

    if (loading) return <div>Loading profile data...</div>;
    if (error) return <div className="error-text">{error}</div>;
  const handleStart = async () =>{
    try {
      navigate(`/profile/${profile_id}/me_active_profile`)
    } catch (err) {
      console.error(err);
      setError("Error, you can't start this adventure.");
    } 
  };
    return (
        <div className="content-area-container profile-view">
            <div className="floating-button-row">
                <button
                    onClick={handleStart}
                >
                    Get your own version
                </button>
                {isOwner && (
                <button 
                onClick={() => navigate(`/profile/${profile_id}/edit`)}
                >
                    Edit
                </button>
                )}
            </div>


            {/* HEADER / NAME */}
            <header className="profile-header" style={{ marginBottom: "32px", borderBottom: "1px solid var(--secondary-color)", paddingBottom: "16px" }}>
                <h1 style={{ margin: "0 0 12px 0", color: "var(--accent-color)" }}>{profileName}</h1>

                
                {/* Reusing your global goal-badge for a clean status pill */}
                <span className="goal-badge level" style={{ display: "inline-block", width: "fit-content" }}>
                    Status: {getVisibilityLabel(visibility)}
                </span>
            </header>

            {/* PREDEFINED BACKGROUND */}
            <section className="profile-section" style={{ marginBottom: "32px" }}>
                <h3 style={{ marginBottom: "16px", color: "var(--text-color)" }}>Default Task</h3>
                {/* Reusing textarea-wrapper for a consistent boxed look without the textarea */}
                <div className="textarea-wrapper" style={{ minHeight: "auto" }}>
                    <p style={{ whiteSpace: "pre-wrap", margin: 0, color: "var(--text-color)", opacity: 0.9 }}>
                        {background}
                    </p>
                </div>
            </section>

            {/* GOALS LIST */}
            <section className="profile-section" style={{ marginBottom: "32px" }}>
                <h3 style={{ marginBottom: "16px", color: "var(--text-color)" }}>Study Goals</h3>
                
                {goals.length === 0 ? (
                    <p style={{ color: "var(--text-color)", opacity: 0.7 }}>No study goals set.</p>
                ) : (
                    <div className="goals-list">
                        {goals.map((goal, index) => (
                            <div key={index} className="goal-card">
                                <div className="goal-content">
                                    <div className="goal-header">
                                        <span className="goal-number">#{index + 1}</span>
                                        <p className="goal-title">{goal.title}</p>
                                    </div>
                                    
                                    <div className="goal-metadata">
                                        {goal.category && <span className="goal-badge category">{goal.category}</span>}
                                        {goal.skill && <span className="goal-badge skill">{goal.skill}</span>}
                                        {goal.level && <span className="goal-badge level">Level: {goal.level}</span>}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </section>

            {/* QUESTIONS LIST */}
            <section className="profile-section" style={{ marginBottom: "32px" }}>
                <h3 style={{ marginBottom: "16px", color: "var(--text-color)" }}>Questions</h3>
                
                {questions.length === 0 ? (
                    <p style={{ color: "var(--text-color)", opacity: 0.7 }}>No questions added.</p>
                ) : (
                    <div className="questions-list">
                        {questions.map((q, index) => (
                            <div key={q.id || index} className="question-card">
                                <div className="question-content">
                                    <span className="question-number">
                                        #{q.position || index + 1}
                                    </span>
                                    <p className="question-text">{q.question_text}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </section>

            
            {isOwner && (

            <section className="profile-section" style={{ marginTop: "48px", paddingTop: "24px", borderTop: "1px dashed var(--secondary-color)" }}>
                <h2 style={{ marginBottom: "24px", color: "var(--accent-color)" }}>System Configurations (Visible to Owner only)</h2>
                
                <div style={{ marginBottom: "16px", color: "var(--text-color)" }}>
                    <strong style={{ color: "var(--primary-color)" }}>Task Generation Rule: </strong>
                    <span style={{ opacity: 0.8 }}>{questPrompt || "None"}</span>
                </div>
                <div style={{ marginBottom: "16px", color: "var(--text-color)" }}>
                    <strong style={{ color: "var(--primary-color)" }}>Follow-up Rule: </strong>
                    <span style={{ opacity: 0.8 }}>{pagePrompt || "None"}</span>
                </div>
                <div style={{ marginBottom: "16px", color: "var(--text-color)" }}>
                    <strong style={{ color: "var(--primary-color)" }}>Goal Generation Rule: </strong>
                    <span style={{ opacity: 0.8 }}>{goalPrompt || "None"}</span>
                </div>
                <div style={{ color: "var(--text-color)" }}>
                    <strong style={{ color: "var(--primary-color)" }}>Action Evaluation Rule: </strong>
                    <span style={{ opacity: 0.8 }}>{actionPrompt || "None"}</span>
                </div>
            </section>
            )}
        </div>
    );
}