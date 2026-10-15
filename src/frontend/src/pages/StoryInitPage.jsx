import StoryInitArea from "@components/ContentArea/InitStory/InitStoryInterface";
import { useParams } from "react-router-dom";
import "@components/GlobalInterface/Global.css";
import { useState } from "react";
import ActionHistoryPanel from "@components/StoryAssistant/RightPanelInterface";

import NavigationPanel from "@components/NavigationPanel/NavigationPanel";
export default function StoryInitPage() {
  const [actions, setActions] = useState([]);

  return (
    <div className="home-layout">
      <StoryInitArea/>

    </div>
  );
}