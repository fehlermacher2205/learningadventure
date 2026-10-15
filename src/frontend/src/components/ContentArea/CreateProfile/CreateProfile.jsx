import { useState, useEffect } from "react";
import {useNavigate, useParams } from "react-router-dom";
import { LuCheck, LuTrash2 } from "react-icons/lu";

import {
    editProfileNameAPI,
    editPromptsAPI,
    add_questionAPI,
    getProfileAPI,
    change_visibility,
    addGoalAPI,
    editBackgroundAPI

} from "@api/profile";

export default function CreateProfile() {
    const {profile_id } = useParams();
    const navigate = useNavigate();

    // 2. State to hold the fetched data
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [profileName, setProfileName] = useState("");
    const [questPrompt, setQuestPrompt] = useState("");
    const [pagePrompt, setPagePrompt] = useState("");
    const [goalPrompt, setGoalPrompt] = useState("");
    const [actionPrompt, setActionPrompt] = useState("");
    const [questions, setQuestions] = useState([]);
    const [visibility, setVisibility] = useState(-1); // Default to -1 (Draft)
    const [newGoal, setNewGoal] = useState({
        title: "",
        category: "",
        skill: "",
        level: "Beginner",
    });
    const [goals, setGoals] = useState([])
    const [background,setBackground] = useState("")
    const [newQuestionText, setNewQuestionText] = useState("");
    useEffect(() => {
        async function fetchProfile() {
            if (!profile_id) {
                setLoading(false);
                return;
            }

            try {
                const data = await getProfileAPI(profile_id);
                // Map the response payload to our local state
                setProfileName(data.profile_name || "");
                setQuestPrompt(data.prompt?.quest_prompt || "");
                setPagePrompt(data.prompt?.page_prompt || "");
                setGoalPrompt(data.prompt?.goal_prompt || "");
                setActionPrompt(data.prompt?.action_prompt || "");
                setQuestions(data.questions || []);
                setGoals(data.predefined_goals||[]);
                setBackground(data.predefined_background||"")
                setVisibility(data.visible ?? -1);
            } catch (err) {
                console.error("Failed to load profile:", err);
                setError("Failed to load profile data.");
            } finally {
                setLoading(false);
            }
        }

        fetchProfile();
    }, [profile_id]);
    const handleVisibilityChange = async (e) => {
            const newValue = Number(e.target.value);
            setVisibility(newValue);
            try {
                await change_visibility(profile_id, newValue);
                alert("Visibility updated successfully!");
            } catch (err) {
                console.error("Failed to update visibility:", err);
                alert("Could not update visibility setting.");
            }
        };
    if (loading) return <div>Loading profile data...</div>;
    if (error) return <div className="error-text">{error}</div>;

    return (
        <div className="content-area-container">
        <div className="floating-button-row">
            <button
            onClick={() => navigate(`/profile/${profile_id}/me_active_profile`)}
            >
                Get started
            </button>
        </div>
            {/* NAME */}
            <h3 style={{marginBottom: "16px"}}>Name</h3>
            <div className="textarea-wrapper" style={{minHeight: "100px"}}>
                <textarea 
                   profile_id="profile-name-input" 
                    className="textarea" 
                    placeholder="Enter your profile name..."
                    value={profileName}
                    onChange={
                        (e) => setProfileName(e.target.value)
                        
                    }
                />
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick= {async () => {
                        await editProfileNameAPI(profile_id, profileName);
                        window.dispatchEvent(new Event("profilesUpdated"));
                        await alert("Name saved!");
                    }}
                >
                    <LuCheck />
                </button>
            </div>
            {/* PREDEFINED BACK GROUND*/}
            <h3 style={{marginBottom: "16px"}}>Define your first task</h3>
            <div className="textarea-wrapper" style={{minHeight: "100px"}}>
                <textarea 
                   profile_id="page-prompt-input" 
                    className="textarea" 
                    placeholder="Enter your first task"
                    value={background}
                    onChange={(e) => setBackground(e.target.value)}
                />
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick= {async () => {
                        await editBackgroundAPI(profile_id, background);
                        await alert("Your task is saved!");
                    }}
                >
                    <LuCheck />
                </button>
            </div>

        

{/* GOALS LIST */}
            <h3 style={{marginBottom: "16px"}}>Predefined Goals</h3>
            
            {goals.length === 0 && <p style={{color: "var(--text-color)"}}>No predefined Goals</p>}
            
            <div className="goals-list">
                {goals.map((goal, index) => (
                    <div key={index} className="goal-card">
                        
                        <div className="goal-content">
                            {/* Top row: Number and Title */}
                            <div className="goal-header">
                                <span className="goal-number">#{index + 1}</span>
                                <p className="goal-title">{goal.title}</p>
                            </div>
                            
                            {/* Bottom row: Badges for the extra JSON data */}
                            <div className="goal-metadata">
                                {goal.category && <span className="goal-badge category">{goal.category}</span>}
                                {goal.skill && <span className="goal-badge skill">{goal.skill}</span>}
                                {goal.level && <span className="goal-badge level">Level: {goal.level}</span>}
                               {/*  {goal.skill_score !== undefined && <span className="goal-badge score">Score: {goal.skill_score}</span>} */}
                            </div>
                        </div>
                        
                        <button 
                            className="delete-btn"
                            onClick={() => alert("Delete goal clicked!")}
                            title="Delete Goal"
                        >
                            <LuTrash2 />
                        </button>

                    </div>
                ))}
            </div>
            {/* NEW GOAL FORM */}
            <div className="goal-creator">

            <div className="goal-creator-header">
                <h4>Add New Goal</h4>
            </div>

            <div className="goal-form-grid">

                <div className="goal-input-group goal-title-field">
                <label>Goal title</label>
                <input
                    type="text"
                    placeholder="Build the new Profile Dashboard"
                    value={newGoal.title}
                    onChange={(e) =>
                    setNewGoal((prev) => ({ ...prev, title: e.target.value }))
                    }
                />
                </div>

                <div className="goal-input-group">
                <label>Category</label>
                <input
                    type="text"
                    placeholder="Development"
                    value={newGoal.category}
                    onChange={(e) =>
                    setNewGoal((prev) => ({ ...prev, category: e.target.value }))
                    }
                />
                </div>

                <div className="goal-input-group">
                <label>Skill</label>
                <input
                    type="text"
                    placeholder="React.js"
                    value={newGoal.skill}
                    onChange={(e) =>
                    setNewGoal((prev) => ({ ...prev, skill: e.target.value }))
                    }
                />
                </div>

                <div className="goal-input-group">
                <label>Level</label>

                <select
                    value={newGoal.level}
                    onChange={(e) =>
                    setNewGoal((prev) => ({ ...prev, level: e.target.value }))
                    }
                >
                    <option>Beginner</option>
                    <option>Intermediate</option>
                    <option>Advanced</option>
                </select>
                </div>

            </div>

            <button
                className="add-goal-btn"
                disabled={!newGoal.title.trim()}
                onClick={async () => {
                try {
                    
                    const updatedGoals = await addGoalAPI(profile_id, newGoal);

                    setGoals(updatedGoals)
                    setNewGoal({
                    title: "",
                    category: "",
                    skill: "",
                    level: "Beginner",
                    });

                } catch (err) {
                    console.error("Failed to add goal:", err);
                }
                }}
            >
                <LuCheck />
                Add Goal
            </button>

            </div>
        {/* VISIBILITY DROPDOWN */}
            <h3 style={{ marginBottom: "16px" }}>Profile Visibility</h3>
            <div style={{ marginBottom: "24px" }}>
                <select 
                    value={visibility} 
                    onChange={handleVisibilityChange}
                    className="textarea" // Reusing textarea base styling for look & feel consistency
                    style={{ minHeight: "40px", padding: "8px", width: "100%", borderRadius: "4px" }}
                >
                    <option value={-1}>Draft</option>
                    <option value={0}>Private</option>
                    <option value={1}>Link Only</option>
                    <option value={2}>Public</option>
                </select>
            </div>
            <h2 style={{ marginBottom: "16px" }}> It is recommended for better experiences!</h2>
            {/* BACKGROUND / QUEST PROMPT */}
            <h3 style={{marginBottom: "16px"}}>Background generation's Rule</h3>
            <div className="textarea-wrapper" style={{minHeight: "100px"}}>
                <textarea 
                   profile_id="quest-prompt-input" 
                    className="textarea" 
                    placeholder="Enter background/quest prompt..."
                    value={questPrompt}
                    onChange={
                        (e) => setQuestPrompt(e.target.value)
                    }
                />
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick= {async () => {
                        await editPromptsAPI(profile_id, questPrompt, "quest_prompt");
                        await alert("Quest prompt saved!");
                    }}
                >
                    <LuCheck 
                    />
                </button>
            </div>

            {/* STORY PAGE PROMPT */}
            <h3 style={{marginBottom: "16px"}}>Story Generation's Rule</h3>
            <div className="textarea-wrapper" style={{minHeight: "100px"}}>
                <textarea 
                   profile_id="page-prompt-input" 
                    className="textarea" 
                    placeholder="Enter story page prompt..."
                    value={pagePrompt}
                    onChange={(e) => setPagePrompt(e.target.value)}
                />
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick= {async () => {
                        await editPromptsAPI(profile_id, pagePrompt, "page_prompt");
                        await alert("Page prompt saved!");
                    }}
                >
                    <LuCheck />
                </button>
            </div>

            {/* GOAL PROMPT */}


            {/* ACTION VALUATION PROMPT */}
            <h3 style={{marginBottom: "16px"}}>Action Evaluation Rule</h3>
            <div className="textarea-wrapper" style={{minHeight: "100px"}}>
                <textarea 
                   profile_id="action-prompt-input" 
                    className="textarea" 
                    placeholder="Enter action valuation prompt..."
                    value={actionPrompt}
                    onChange={(e) => setActionPrompt(e.target.value)}
                />
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick= {async () => {
                        await editPromptsAPI(profile_id, actionPrompt, "action_prompt");
                        await alert("Action valuation prompt saved!");
                    }}
                >
                    <LuCheck />
                </button>
            </div>



{/* QUESTIONS LIST */}
            <h2 style={{
                marginTop: "16px",
                marginBottom: "16px",
                color : "var(--error-color)",
            }}> A question can't be edited once it is added!</h2>

            <h3 style={{marginBottom: "16px"}}>Questions</h3>
            
            {questions.length === 0 && <p style={{color: "var(--text-color)"}}>No predefined Questions</p>}
            
            <div className="questions-list">
                {questions.map((q, index) => (
                    <div key={q.id || index} className="question-card">
                        
                        <div className="question-content">
                            <span className="question-number">#{q.position || index + 1}</span>
                            <p className="question-text">{q.question_text}</p>
                        </div>


                    </div>
                ))}
            </div>
{/* NEW QUESTION INPUT */}
            <div className="textarea-wrapper" style={{marginTop: "20px"}}>
                <textarea 
                   profile_id="new-question-input" 
                    className="textarea" 
                    placeholder="Type a new question to add..."
                    value={newQuestionText}
                    onChange={(e) => setNewQuestionText(e.target.value)}
                />
                
                {/* CORRECTED ADD BUTTON */}
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick={async () => {
                        try {
                            const updatedProfile = await add_questionAPI(profile_id, newQuestionText);
                            
                            setQuestions(updatedProfile.questions || []);
                            
                            setNewQuestionText("");
                        } catch (err) {
                            console.error("Failed to add question:", err);
                            alert("Could not add the question.");
                        }
                    }}
                >
                    <LuCheck />
                </button>
            </div>

        </div>
    );
}