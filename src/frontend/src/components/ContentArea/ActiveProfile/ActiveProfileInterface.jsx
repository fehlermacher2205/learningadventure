import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { 
  getProfileAPI,
  get_me_activeGoalsAPI,
  addallgoalsAPI,
  addonegoalAPI,
  removeonegoalAPI,
  changegoalPriorityAPI,
  get_active_storyAPI
} from "@api/profile"; 
import { LuPlus, LuMinus } from "react-icons/lu";
import { StarOff, Star } from "lucide-react";

export default function ActiveProfileInterface() {
    const [toast, setToast] = useState(null);
    const { profile_id } = useParams();
    const navigate = useNavigate();

    // State to hold the fetched data
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [profileName, setProfileName] = useState("");
    
    // Predefined goals and active goals
    const [goals, setGoals] = useState([]);
    const [personalGoals, setPersonalGoals] = useState([]);
    const [activeStoryId, setActiveStoryId] = useState("");

    // Handle Toast Timeouts
    useEffect(() => {
        if (toast) {
            const timer = setTimeout(() => setToast(null), 3000);
            return () => clearTimeout(timer);
        }
    }, [toast]);

    // Fetch Profile Data
    useEffect(() => {
        async function fetchProfile() {
            if (!profile_id) {
                setLoading(false);
                return;
            }

            try {
                const data = await getProfileAPI(profile_id);
                setProfileName(data.profile_name || "Unnamed Profile");
                setGoals(data.predefined_goals || []);
                
                const data2 = await get_me_activeGoalsAPI(profile_id);
                setPersonalGoals(data2.goals || []);
                setActiveStoryId(data2.active_story_id);
            } catch (err) {
                console.error("Failed to load active goals:", err);
                setToast({ type: "error", message: "Failed to load active goals."});
                setError("Failed to load profile data.");
            } finally {
                setLoading(false);
            }
        }

        fetchProfile();
        // Removed activeStoryId from dependencies to prevent infinite loops
    }, [profile_id]); 

    const handleEditBackground = async () => {
        try {
            navigate(`/profile/${profile_id}/stories/${activeStoryId}/init`);
        } catch (err) {
            console.error(err);
            setToast({ type: "error", message: "Failed to load your Adventure"});
        } 
    };
    
    const handleAddAll = async () => {
        try {
            const data = await addallgoalsAPI(profile_id);
            setPersonalGoals(data.goals || []);
            setToast({ type: "success", message: "All goals added successfully!"});
        } catch (err) {
            console.error(err);
            setToast({ type: "error", message: "Failed to add all goals"});
        } 
    };

    const handleAddGoal = async (predefinedId) => {
        try {
            const data = await addonegoalAPI(profile_id, predefinedId);
            setPersonalGoals(data || []);
            setToast({ type: "success", message: "Goal added!" });
        } catch (err) {
            console.error("Failed to add goal:", err);
            setToast({ type: "error", message: "Failed to add goal." });
        }
    };

    const handleRemoveGoal = async (predefinedId) => {
        try {
            const data2 = await removeonegoalAPI(profile_id, predefinedId);
            setPersonalGoals(data2 || []);
            setToast({ type: "success", message: "Goal removed!" });
        } catch (err) {
            console.error("Failed to remove goal:", err);
            setToast({ type: "error", message: "Failed to remove goal." });
        }
    };
    const handleStartCourse = async ()=>{
        try {
            const active_story = await get_active_storyAPI(profile_id);
            window.dispatchEvent(new CustomEvent("storyCreated"));
            navigate(`/profile/${profile_id}/stories/${active_story.story_id}`)
        }
        catch (err){
            console.error("Failed get active story", err);
            setToast({ type: "error", message: "Failed get active story" });     
        }
    }
    const handleToggleFocus = async (predefinedId) => {
        try {
            const data = await changegoalPriorityAPI(profile_id, predefinedId);
            setPersonalGoals(data || []);
            setToast({ type: "success", message: "Focus updated!" });
        } catch (err) {
            console.error("Failed to toggle focus:", err);
            setToast({ type: "error", message: "Failed to update focus." });
        }
    };

    if (loading) return <div>Loading profile data...</div>;
    if (error) return <div className="error-text">{error}</div>;

    return (
        <div className="content-area-container profile-view">
            
            {/* ACTION BUTTONS */}
            <div className="floating-button-row">
                <button onClick={handleAddAll}>
                    Add all goals!
                </button>
                <button onClick={handleEditBackground}>
                    Personalize your Experience
                </button>
                <button onClick={handleStartCourse}>
                    Start the Course
                </button>
            </div>
            
            {toast && (
                <div className={`toast ${toast.type}`}>
                    {toast.message}
                </div>
            )}
            
            {/* HEADER / NAME */}
            <header className="profile-header" style={{ marginBottom: "32px", borderBottom: "1px solid var(--secondary-color)", paddingBottom: "16px" }}>
                <h1 style={{ margin: "0 0 12px 0", color: "var(--accent-color)" }}>{profileName}</h1>
            </header>

            <h2 style={{
                marginTop: "16px",
                marginBottom: "16px",
                color :"var(--error-color)",
            }}> 
                For better experiences, it is recommended to add all predefined goals to your active course.
            </h2>

            {/* PREDEFINED GOALS LIST */}
            <section className="profile-section" style={{ marginBottom: "32px" }}>
                <h3 style={{ marginBottom: "16px", color: "var(--text-color)" }}>Course Goals</h3>
                
                {goals.length === 0 ? (
                    <p style={{ color: "var(--text-color)", opacity: 0.7 }}>No predefined goals available.</p>
                ) : (
                    <div className="goals-list">
                        {goals.map((goal, index) => {
                            const activeGoalMatch = personalGoals.find(pg => pg.predefinedgoal_id === goal.id);
                            const isActive = !!activeGoalMatch;

                            return (
                                <div key={goal.id} className={`goal-card ${isActive ? 'active-goal' : ''}`}>
                                    <div className="goal-content" style={{ display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%" }}>
                                        
                                        <div className="goal-info">
                                            <div className="goal-header">
                                                <span className="goal-number">#{index + 1}</span>
                                                <p className="goal-title">{goal.title}</p>
                                            </div>
                                            
                                            <div className="goal-metadata">
                                                {goal.category && <span className="goal-badge category">{goal.category}</span>}
                                                {goal.skill && <span className="goal-badge skill">{goal.skill}</span>}
                                                {goal.level && <span className="goal-badge level">Level: {goal.level}</span>}
                                            
                                                <span
                                                className={`goal-badge skill_score ${
                                                    isActive && activeGoalMatch.skill_score != null ? "" : "hidden"
                                                }`}
                                                >
                                                Score: {activeGoalMatch?.skill_score ?? ""}
                                                </span>
                                            </div>
                                        </div>
                                        {isActive ? (
                                            <div className="button-row">
                                                <button 
                                                    className="remove-goal-btn"
                                                    onClick={() => handleRemoveGoal(activeGoalMatch.predefinedgoal_id)}
                                                >
                                                    <LuMinus /> Remove
                                                </button>
                                                <button 
                                                    className="toggle-focus-btn"
                                                    onClick={() => handleToggleFocus(activeGoalMatch.predefinedgoal_id)}
                                                >
                                                    {activeGoalMatch.is_focused ? <StarOff /> : <Star  />}
                                                </button>
                                            </div>
                                        ) : (
                                            <div className="button-row">
                                                <button 
                                                    className="add-goal-btn"
                                                    onClick={() => handleAddGoal(goal.id)}
                                                >
                                                    <LuPlus /> Add
                                                </button>
                                                
                                                {/* ADD THE CLASSNAME HERE */}
                                                <button 
                                                    className="toggle-focus-btn" 
                                                    style={{ visibility: 'hidden', pointerEvents: 'none' }}
                                                    aria-hidden="true"
                                                >
                                                    <Star /> 
                                                </button>
                                            </div>
                                        )}

                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </section>
        </div>
    );
}