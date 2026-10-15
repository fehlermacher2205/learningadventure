import UserCreationInterface from '@/components/UserCreation/UserCreationI';
export default function UserCreationPage() {
  return (
    <div className="user-creation-page">
      {/* If you ever want a sidebar or navigation menu, you'd add it here next to the chat! */}
      <UserCreationInterface />
    </div>
  );
}