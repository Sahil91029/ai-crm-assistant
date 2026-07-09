import { useState, useRef, useEffect } from "react";
import { useDispatch } from "react-redux";
import { updateMultipleFields } from "../redux/interactionSlice";

import api from "../services/api";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

export default function ChatPanel() {
  const dispatch = useDispatch();

  const bottomRef = useRef(null);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text:
        "👋 Hello! I'm your AI CRM Assistant.\n\nDescribe your interaction or use the microphone and I'll automatically fill the CRM form.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const speak = (text) => {
    if (!window.speechSynthesis) return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = "en-US";
    utterance.rate = 1;

    window.speechSynthesis.speak(utterance);
  };

  const handleSend = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      role: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      const { data } = await api.post("/chat", {
        message: text,
      });

      console.log("Backend Response:", data);

      if (data.form) {
        dispatch(updateMultipleFields(data.form));
      }

      const aiMessage = {
        role: "assistant",
        text: data.reply,
      };

      setMessages((prev) => [...prev, aiMessage]);

      speak(data.reply);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            "❌ Unable to connect to the backend. Please check if FastAPI is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg h-[82vh] flex flex-col">

      {/* Header */}
      <div className="border-b p-5">

        <h2 className="text-2xl font-bold">
          🤖 AI CRM Assistant
        </h2>

        <p className="text-gray-500 text-sm mt-1">
          Chat or use your voice to log HCP interactions.
        </p>

      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50">

        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            message={msg}
          />
        ))}

        {loading && (
          <div className="flex">

            <div className="bg-white border rounded-xl px-4 py-3 shadow">

              <div className="flex items-center gap-2">

                <span className="animate-pulse">
                  🤖
                </span>

                <span className="text-gray-600">
                  AI is analyzing your interaction...
                </span>

              </div>

            </div>

          </div>
        )}

        <div ref={bottomRef} />

      </div>

      {/* Chat Input */}
      <div className="border-t p-5">
        <ChatInput onSend={handleSend} />
      </div>

    </div>
  );
}