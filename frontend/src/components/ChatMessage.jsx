export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex mb-4 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-5 py-4 shadow whitespace-pre-wrap ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white border text-gray-800"
        }`}
      >
        <div className="flex items-center gap-2 mb-2">

          <div className="text-xl">
            {isUser ? "🧑" : "🤖"}
          </div>

          <div className="font-semibold">
            {isUser ? "You" : "AI Assistant"}
          </div>

        </div>

        <div className="leading-7 text-[15px]">
          {message.text}
        </div>
      </div>
    </div>
  );
}