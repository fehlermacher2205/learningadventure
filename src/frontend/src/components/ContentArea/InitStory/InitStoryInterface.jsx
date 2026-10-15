import { useState, useEffect } from "react";
import { useNavigate,useParams } from "react-router-dom";
import { LuCheck, LuTrash2, LuPlus } from "react-icons/lu";

import { getProfileAPI } from "@api/profile";
import { 
  getStoryAPI, 
  generateBackgroundStory,
  editStorybackgroundAPI,
  editsnapshotAPI
} from '@api/story';

export default function StoryInitArea() {
  const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const { profile_id, story_id } = useParams();
    const [background, setBackground] = useState("");
    const [loadingSnap,setloadingSnap]= useState(false)
    const [error, setError] = useState("");

    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState([]);
    const [snapshot, setAnswers_snapshot] = useState([]);

    useEffect(() => {
        async function fetchSnapshotData(){
            try {
                const data = await getStoryAPI(story_id);
                setAnswers_snapshot(data.answers_snapshot);
                setBackground(data.background);    
            } catch (err) {
                console.error("Failed to load answers snapshot:", err);
                setError("Failed to load data.");
            } finally {
                setLoading(false);
            }
        }

        fetchSnapshotData();
    }, [story_id]);

    // ADDED: Missing handler to update the textareas without losing data
    const handleSnapshotChange = (index, partIndex, newValue) => {
        const updatedSnapshots = [...snapshot];
        updatedSnapshots[index][partIndex] = newValue;
        setAnswers_snapshot(updatedSnapshots);
    };
    const handleUpdateSnapshot = async () => {
        try {
            setloadingSnap(true);
            await editsnapshotAPI(story_id,snapshot);
            await editStorybackgroundAPI(story_id, background);
        }
        catch (err) {
            console.error("Failed to update snapshot:", err);
            setError("Failed to load data.");
        }
        finally{
            setloadingSnap(false);
        }

    };

    if (loading) return <div>Loading data...</div>;
    if (error) return <div className="error-text">{error}</div>;

    return (
        <div className="content-area-container">
            <div className="floating-button-row">
                <button
                    onClick={() => navigate(`/profile/${profile_id}/stories/${story_id}`)}
                >
                    To the Story
                </button>
                <button 
                    onClick={handleUpdateSnapshot} disabled={loading}>
                    {loadingSnap ? "Saving..." : "Save your personalized data"}
                </button>
                <button
                    onClick={() => navigate(`/profile/${profile_id}/me_active_profile`)}
                    >
                        Check your goals!
                </button>
            </div>            
            <h2 style={{ margin: "0 0 12px 0", color: "var(--accent-color)" }}>This will affect on how your new task is created!</h2>

{/* BACKGROUND editor*/}
            <h3 style={{marginBottom: "16px"}}>Enter your customized task here</h3>
            <div className="textarea-wrapper" style={{minHeight: "100px", position: "relative"}}>
                <textarea 
                   profile_id="page-prompt-input" 
                    className="textarea" 
                    placeholder="Enter your task..."
                    value={background}
                    onChange={(e) => setBackground(e.target.value)}
                />
                <button className="icon-btn"
                    style={{ position: 'absolute', bottom: '20px', right: '20px' }}
                    onClick={async () => {
                        await editStorybackgroundAPI(story_id, background);
                        alert("Your new background is saved!");
                    }}
                >
                    <LuCheck />
                </button>
            </div>



            {/* YOUR SNAPSHOT */}
            <h3 style={{marginBottom: "16px", marginTop: "24px"}}>Your Profile</h3>
            
            <div className="snapshot-list">
                {snapshot.map(([question, answer], index) => (
                    <div key={index} className="snapshot-card" style={{ marginBottom: "20px", padding: "15px", border: "1px solid #ccc", borderRadius: "8px" }}>
                        <span className="snapshot-number" style={{ fontWeight: "bold" }}>#{index + 1}</span>
                        
                        {/* Question Textarea */}
                        <div className="textarea-wrapper" style={{ marginTop: "10px" }}>
                            <label style={{ display: "block", fontSize: "14px", marginBottom: "4px" }}>Question:</label>
                            <textarea 
                                className="textarea" 
                                placeholder="Edit question..."
                                value={question}
                                onChange={(e) => handleSnapshotChange(index, 0, e.target.value)}
                                style={{ width: "100%", minHeight: "60px" }}
                            />
                        </div>

                        {/* Answer Textarea */}
                        <div className="textarea-wrapper" style={{ marginTop: "10px" }}>
                            <label style={{ display: "block", fontSize: "14px", marginBottom: "4px" }}>Answer:</label>
                            <textarea 
                                className="textarea" 
                                placeholder="Edit answer..."
                                value={answer}
                                onChange={(e) => handleSnapshotChange(index, 1, e.target.value)}
                                style={{ width: "100%", minHeight: "60px" }}
                            />
                        </div>
                    </div>
                ))}
            </div>
{
    /* Button to add more personal data   */
}
            <button 
                className="btn secondary-btn" 
                // FIXED: Wrapped state update inside an arrow function
                onClick={() => setAnswers_snapshot([...snapshot, ["", ""]])}
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    marginTop: "12px",
                    padding: "8px 16px",
                    cursor: "pointer"
                }}
            >
                <LuPlus /> Add more personal touch
            </button>  



        </div>
    );
}