import { useEffect, useState } from "react";
import NavigationPanel from "@components/NavigationPanel/NavigationPanel";
import ActiveProfile from "@components/ContentArea/ActiveProfile/ActiveProfileInterface";

export default function DiscoverPage() {
  return (
    <div className="home-layout">
      <ActiveProfile />
    </div>
  );
}