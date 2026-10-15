import StoryArea from "@components/ContentArea/ChatBox/ChatInterface";
import ProfilePanel from "@components/ContentArea/Profile/ProfilePageInterface";
import { useParams } from "react-router-dom";
import "@components/GlobalInterface/Global.css";
import { useState } from "react";
import ActionHistoryPanel from "@components/StoryAssistant/RightPanelInterface";

import NavigationPanel from "@components/NavigationPanel/NavigationPanel";
export default function SessionChatPage() {
  const [actions, setActions] = useState([]);

  return (
    <div className="home-layout">
      <StoryArea
        setActions={setActions}
      />

      <ActionHistoryPanel
        actions={actions}
      />
    </div>
  );
}