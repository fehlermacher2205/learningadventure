import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// NOTE: Import your actual API calls here. Adjust the paths and names to match your project.
import {
  getUserFromCookiesAPI,
  get_my_created_profilesAPI
} from '@api/user'


export default function YourCreatedProfile() {
  const [profiles, setProfiles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Added missing state variables
  const [isLoggedIn, setIsLoggedIn] = useState(false); 
  const [isSubmitting, setIsSubmitting] = useState(false); 
  
  const navigate = useNavigate();

  useEffect(() => {
    setIsLoading(true);
    
    async function fetchProfilesData() {
      try {
        const user = await getUserFromCookiesAPI();
        const activeProfiles = await get_my_created_profilesAPI();
        
        if (user && user.id) {
          setIsLoggedIn(true); // Fixed: was setLoggedIn(true)
          
          if (activeProfiles) {
            setProfiles(activeProfiles);
          }
        } else {
          setIsLoggedIn(false); // Fixed: was setLoggedIn(false)
          setProfiles([]);
        }
      } catch (err) {
        console.error("Auth check failed:", err);
        setIsLoggedIn(false); // Fixed: was setLoggedIn(false)
        setError("Failed to load profiles");
      } finally {
        setIsLoading(false); // Fixed: was setLoading(false)
      }
    }
    
    fetchProfilesData();
  }, []);

  const truncateText = (text, maxLength = 200) => {
    if (!text) return "No background provided.";
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <h2>Discovering Profiles...</h2>
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-message">
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="discovery-container">
      <header className="discovery-header">
        <h1>Your Created Profiles</h1>
        <p> Select a profile to edit.</p>
        

      </header>

      <div className="profiles-grid">
        {profiles.map((profile) => (
          <div 
            key={profile.profile_id} 
            className="profile-card"
            onClick={() => navigate(`/profile/${profile.profile_id}`)}
          >
            <div className="profile-card-header">
              <h3 className="profile-name">{profile.profile_name}</h3>
              <span className="profile-id-badge">#{profile.profile_id}</span>
            </div>
            
            <div className="profile-background">
              <p>{truncateText(profile.predefined_background)}</p>
            </div>
          </div>
        ))}

        {profiles.length === 0 && (
          <div className="no-profiles-message">
            <p>No profiles found. Start creating one!</p>
          </div>
        )}
      </div>
    </div>
  );
}