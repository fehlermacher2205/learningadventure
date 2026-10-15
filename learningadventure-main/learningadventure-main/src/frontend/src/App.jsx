import ProfileCreatePage from '@pages/ProfileCreatePage';
import ChatInterface from '@pages/StoryPage';
import YourCreatedProfilePage from '@pages/YourCreatedProfilePage'
import ActiveProfileEditorPage from '@pages/ActiveProfileEditorPage';
import GlobalSessionHandler from '@components/GlobalInterface/GlobalSessionHandler';
import ProfilePage from '@pages/ProfilePage';
import StoryInitPage from '@pages/StoryInitPage';
import DiscoverPage from '@pages/DiscoverPage';
import Home from '@pages/Home';

import UserCreationPage from '@pages/UserCreationPage';

import './components/GlobalInterface/Global.css';
import './index.css';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

export default function App() {
  const profile_id = "code_bar_programmierwerkstatt";
  return (
    <BrowserRouter>
      <GlobalSessionHandler>
        <Routes>
          
          <Route path="/register" element={<UserCreationPage />} />
          {/* 2. PROTECTED/LAYOUT ROUTES: Sidebar included */}
          <Route element={<Home />}>

            <Route path="/my_profile" element={<YourCreatedProfilePage />} />
            <Route path="/profile/:profile_id/edit" element={<ProfileCreatePage />} />
            <Route path="/profile/:profile_id/" element={<ProfilePage />} />

            
            <Route path="/profile/:profile_id/me_active_profile" element={<ActiveProfileEditorPage />} />
            <Route path="/profile/:profile_id/stories/:story_id" element={<ChatInterface />} />
            <Route path="/profile/:profile_id/stories/:story_id/init" element={<StoryInitPage />} />
            <Route path="/discover" element={<DiscoverPage />} />
            <Route path="*" element={<Navigate to="/profile/code_bar_programmierwerkstatt/" replace />} />
            
          </Route>

        </Routes>
      </GlobalSessionHandler>
    </BrowserRouter>
  );
}