import Header from "../components/Header";
import InteractionForm from "../components/InteractionForm";
import ChatPanel from "../components/ChatPanel";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />

      <div className="grid grid-cols-2 gap-6 p-6">
        <InteractionForm />
        <ChatPanel />
      </div>
    </div>
  );
}