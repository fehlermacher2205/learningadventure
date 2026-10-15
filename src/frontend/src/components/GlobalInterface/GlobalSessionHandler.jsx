import { useState, useEffect } from 'react';
import UserLoginModal from './UserLoginModal'; 
import { useLocation, useNavigate } from "react-router-dom";
import { LogOut, LogIn,Sun,Moon } from 'lucide-react';
// 1. Import your new API function
import { logoutUserAPI, getUserFromCookiesAPI } from '@api/user'; 

export default function GlobalSessionHandler({ children }) {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();
  
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  const PUBLIC_ROUTES = ["/register"];
  const isPublicRoute = PUBLIC_ROUTES.some(route =>
    location.pathname.startsWith(route)
  );
  const toggleTheme = () => {
      if (isDarkMode) {
        document.documentElement.setAttribute("data-theme", "light");
        setIsDarkMode(false);
      } else {
        document.documentElement.setAttribute("data-theme", "dark");
        setIsDarkMode(true);
      }
    };
  useEffect(() => {
    const verifyInitialSession = async () => {
      try {
        const response = await getUserFromCookiesAPI();
        
        if (response && response.id) {
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      } catch (error) {
        console.error("Cookie session verification failed:", error);
        setIsLoggedIn(false);
      }
    };

    verifyInitialSession();
  }, []); // <-- Empty array ensures this fires only once on load


  // --- EXISTING EFFECT: Syncs with route changes & custom login events ---
  useEffect(() => {
    const checkAuthStatus = () => {
      // Note: If you are transitioning entirely to cookies, you may want to 
      // phase out this localStorage check in the future to avoid state conflicts.
      const token = localStorage.getItem("token") || sessionStorage.getItem("token");
      
      // Only update to true if we find a token (preventing it from overriding 
      // a successful cookie check if token happens to be missing)
      if (token) {
        setIsLoggedIn(true);
      }
    };

    checkAuthStatus();

    window.addEventListener("authChanged", checkAuthStatus);

    return () => {
      window.removeEventListener("authChanged", checkAuthStatus);
    };
  }, [location.pathname]);

  const handleLogout = async () => {
    try {
      await logoutUserAPI();
    } catch (err) {
      console.error("Backend logout failed:", err);
    }

    alert("Logged out successfully!");
    localStorage.clear();
    sessionStorage.clear();
    
    setIsLoggedIn(false);
    setShowLoginModal(false);
    navigate("/");
  };


  return (
    <>
      {children}
        <button className="icon-btn"
            style={{ position: 'absolute', bottom: '20px', left: '150px' }}
            onClick={toggleTheme}
        >
            {isDarkMode ? <Sun /> : <Moon /> }
        </button>
      {showLoginModal && (
        <UserLoginModal onClose={() => setShowLoginModal(false)} />
      )}
      
      {!isPublicRoute && (
        <div 
          style={{
            position: 'absolute',
            bottom: '20px',
            left: '20px',
            zIndex: 1000 
          }}
        >
          {isLoggedIn ? (
            <button 
              className="icon-text-stretch-btn" 
              style={{ width: '100px' }}
              onClick={handleLogout}
            >
              <LogOut size={20} />
              <span>logout</span>
            </button>
          ) : (
            <button 
              className="icon-text-stretch-btn" 
              style={{ width: '100px' }}
              onClick={() => setShowLoginModal(true)}
            >
              <LogIn size={20} />
              <span>Login</span>
            </button>
          )}
        </div>
      )}
    </>
  );
}