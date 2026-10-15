import { Outlet } from "react-router-dom";
import NavigationPanel from "@components/NavigationPanel/NavigationPanel";
      
export default function MainLayout() {
  return (
    <div className="home-layout">
      {/* 1. LEFT PANE: The static sidebar */}
      <NavigationPanel />
      
      {/* 2. THE REST OF THE SCREEN: This Outlet will hold a component 
             that splits itself into the Middle and Right panes */}
      <div className="workspace-area">
        <Outlet />
      </div>
    </div>
  );
}