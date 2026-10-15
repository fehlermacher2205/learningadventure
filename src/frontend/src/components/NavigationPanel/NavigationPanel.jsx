import { useNavigate, useParams,Link } from "react-router-dom";
import "./NavigationPanel.css";
import { useState, useEffect } from "react";
import {  
  getUserFromCookiesAPI, 
  createProfileAPI,
  logoutUserAPI,
  get_active_profilesAPI,
  discoverProfileAPI,
  get_my_created_profilesAPI
} from '@api/user';
import { 
  get_active_storyAPI,
  get_expire_storiesAPI
 } from '@api/profile';
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
import { LuRocket } from 'react-icons/lu';

export default function NavigationPanel({ setActiveView }) {
  const navigate = useNavigate();
  
  const [loggedIn, setLoggedIn] = useState(false);
  const [profiles, setProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [selectedStory,setSelectedStory] = useState(null);
  const [isOwnerOfSelectedProfile,setisOwnerOfSelectedProfile] = useState(false);
  const [activestory, setActiveStory] = useState(null);
  const [expiredstories, setExpiredStories] = useState([]);

  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false); 
  const [error, setError] = useState("");
  const [user_id, setUserID] = useState(null);
  const [is_admin, setIsAdmin] = useState(false);
  // --- UPDATED EFFECT ---
  useEffect(() => {
    setLoading(true);
    async function fetchAuthAndProfiles() {
      try {
        const user = await getUserFromCookiesAPI();
        const profiles = await get_active_profilesAPI();
        if (user && user.id) {
          setUserID(user.id)
          setIsAdmin(user.is_admin);
          setLoggedIn(true);
          
          if (profiles) {
            setProfiles(profiles);
          }
        } else {
          setUserID(null)
          setLoggedIn(false);
          setProfiles([]);
        }
      } catch (err) {
        console.error("Auth check failed:", err);
        setLoggedIn(false);
        setError("Failed to load profiles");
      } finally {
        setLoading(false);
      }
    }
//Run it once when the component mounts
    fetchAuthAndProfiles();

//Listen for the custom event we added in CreateProfile
    window.addEventListener("profilesUpdated", fetchAuthAndProfiles);
  //Clean up the listener when the component unmounts
    return () => {
        window.removeEventListener("profilesUpdated", fetchAuthAndProfiles);
      };

  }, []);

  const handleRegenerateBackground = async () =>{
    setIsSubmitting(true);
    try {
      const data = await createStoryAPI(selectedProfile.profile_id);
      navigate(`/profile/${selectedProfile.profile_id}/stories/${data.id}`)
    } catch (err) {
      console.error(err);
      setError(" Unknown error when creating new profile!");
    } finally {
      setIsSubmitting(false);
    }
  };



  const handleCreateNewStory = async () =>{
    setIsSubmitting(true);
    try {
      const data = await createStoryAPI(selectedProfile.profile_id);
      navigate(`/profile/${selectedProfile.profile_id}/stories/${data.id}`)
    } catch (err) {
      console.error(err);
      setError(" Unknown error when creating new profile!");
    } finally {
      setIsSubmitting(false);
    }
  };
  const handleCreateProfile = async () => {
    setIsSubmitting(true);
    try {
      const data = await createProfileAPI();
      navigate(`/profile/${data.profile_id}/edit`);
    } catch (err) {
      console.error(err);
      setError(" Unknown error when creating new profile!");
    } finally {
      setIsSubmitting(false);
    }
  };
  const handleYourCreatedProfile = async () => {
    setIsSubmitting(true);
    try {
      const data = await get_my_created_profilesAPI()
      navigate(`/my_profile`);
    } catch (err) {
      console.error(err);
      setError("Failed to load public profiles Pages!");
    } finally {
      setIsSubmitting(false);
    }
  };
  const handleDiscoveryProfile = async () => {
    setIsSubmitting(true);
    try {
      const data = await discoverProfileAPI()
      navigate(`/discover`);
    } catch (err) {
      console.error(err);
      setError("Failed to load public profiles Pages!");
    } finally {
      setIsSubmitting(false);
    }
  };
  async function handleProfileClick(profile) {
    try {
      const activeStorydata = await get_active_storyAPI(profile.profile_id);
      const expiredStoriesdata = await get_expire_storiesAPI(profile.profile_id);
      setSelectedProfile(profile);
      
      setActiveStory(activeStorydata);
      setExpiredStories(expiredStoriesdata);
      setisOwnerOfSelectedProfile(user_id === profile.user_id);
    } catch (err) {
      console.error(err);
      setError("Failed to load stories");
    }
  }
  async function  handleStoryClick(story) {
    
    try {
      navigate(`/profile/${selectedProfile.profile_id}/stories/${story.story_id}`)
      setSelectedStory(story)
    } catch (err) {
      console.error(err);
      setError(" Unknown error when selecting a story!");
    } finally {
      setIsSubmitting(false);
    }
  };
  function handleBackToProfiles() {
    setSelectedProfile(null);
    setActiveStory(null);
  }
  if (loading) {
      return (
        <div className="navigation-panel">
          <div className="icons-section" style={{ display: 'flex', justifyContent: 'center', paddingTop: '40px' }}>
            {/* We are overriding the size inline to make it a "small" icon as requested */}
            <div 
              className="spinner" 
              style={{ 
                width: '30px', 
                height: '30px', 
                borderWidth: '3px',
                borderColor: 'rgba(255, 255, 255, 0.1)', // Adapts the border for dark mode
                borderTopColor: 'var(--accent-color)'
              }} 
            />
          </div>
        </div>
      );
    }

  return (
    <div className="navigation-panel">
      <div className="icons-section">
        {!selectedProfile ? (
          <>
            <h3>Navigation</h3>
            
            {/* Only show creation buttons if they are actually logged in */}
            {loggedIn && is_admin && (
              <button className="icon-text-stretch-btn" 
                onClick={handleCreateProfile}
                disabled={isSubmitting}
              >
                <CirclePlus size={20} />
                {isSubmitting ? "Creating..." : "New Profile"}
              </button>
            )}
            {loggedIn && (
              <button className="icon-text-stretch-btn" 
                onClick= {handleDiscoveryProfile}
                disabled={isSubmitting}
              >
                <Search size={20} />
                Discover Profiles
              </button>
            )}
            {loggedIn && is_admin && (
              <button className="icon-text-stretch-btn" 
                onClick= {handleYourCreatedProfile}
                disabled={isSubmitting}
              >
                <User  size={20} />
                Your created Profiles
              </button>
            )}
            
            {error && <p className="error-text">{error}</p>}
          {!selectedProfile && (
            <h3>Your Profiles</h3>
          )}
            {!loggedIn && !loading && (
              <p>Please log in to view your profiles.</p>
            )}

            {loggedIn && profiles.length === 0 && (
              <p>No profiles found.</p>
            )}

            {profiles.map((profile) => (
              <div
                key={profile.profile_id}
                className="profile-item"
                onClick={() => handleProfileClick(profile)}
              >
                {profile.profile_name}
              </div>
            ))}
          </>
        ) : (
          <>
            <button className="icon-text-stretch-btn" 
              onClick={() => handleBackToProfiles()}
            >
              <BookUser size={20} color="white" strokeWidth={2}/>
              Return to your recent Profile
            </button>

            {isOwnerOfSelectedProfile  && (
              <button className="icon-text-stretch-btn" 
              onClick={() => navigate(`/profile/${selectedProfile.profile_id}/edit`)}
              >
              <Settings  size={20} color="white" strokeWidth={2}/>

                Edit
              </button>
            )}
            <button className="icon-text-stretch-btn" 
              onClick={() => navigate(`/profile/${selectedProfile.profile_id}/me_active_profile`)}
            >
              <SquarePen   size={20} color="white" strokeWidth={2} />
              Edit Active Goal
            </button>

            <button className="icon-text-stretch-btn" 
              onClick={() => handleCreateNewStory() }
            >
              <MapPlus  size={20} color="white" strokeWidth={2} />
              Start a new Story
            </button>

            {selectedStory  && (            
              <button className="icon-text-stretch-btn" 
                onClick={() => handleRegenerateBackground() }
              >
                <RotateCcw size={20} color="white" strokeWidth={2} />
                Regenerate the Background
              </button>
            )}
{/* Active stories block  */}
            {selectedProfile && (
              <h3>Active Story</h3>
            )}
              <div
                key={activestory.story_id}
                className="story-item"
                onClick={() => handleStoryClick(activestory)}
              >
                {activestory.title}
              </div>
{/* Inactive stories block  */}
            {selectedProfile && (
              <h3>Expired Stories</h3>
            )}

              {expiredstories.length === 0 && (
                <p>No Stories found.</p>
              )}
              {expiredstories.map((story) => (
                <div
                  key={story.story_id}
                  className="story-item"
                  onClick={() => handleStoryClick(story)}
                >
                  {story.title}
                </div>
              ))}

          </>
        )}
      </div>
    </div>
  );
}