import { useEffect, useState } from "react";
import NavigationPanel from "@components/NavigationPanel/NavigationPanel";
import YourCreatedProfile from "@components/ContentArea/Discovery/DiscoverYourCreatedProfileInterface";

export default function YourCreatedProfilePage() {
  return (
    <div className="home-layout">
      <YourCreatedProfile />
    </div>
  );
}