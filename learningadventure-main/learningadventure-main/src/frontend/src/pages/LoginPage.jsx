{/*there is no login page but a modal*/}

import UserLoginInterface from '@/components/UserLogin/UserLoginI';
export default function LoginPage() {
  return (
    <div className="user-login-page">
      {/* If you ever want a sidebar or navigation menu, you'd add it here next to the chat! */}
      <UserLoginInterface />
    </div>
  );
}
