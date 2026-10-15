import { useEffect, useState } from "react";
import NavigationPanel from "@components/NavigationPanel/NavigationPanel";
import Discover from "@components/ContentArea/Discovery/DiscoveryInterface";

export default function DiscoverPage() {
  return (
    <div className="home-layout">
      <Discover />
    </div>
  );
}