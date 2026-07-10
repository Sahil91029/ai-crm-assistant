import { useState, useRef, useEffect } from "react";
import { useDispatch } from "react-redux";
import { updateMultipleFields } from "../redux/interactionSlice";

import api from "../services/api";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";

export default function ChatPanel() {
  const dispatch = useDispatch();

  const bottomRef = useRef(null);

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text:
        "👋 Hello! I'm your AI CRM Assistant.\n\nDescribe your interaction or use the microphone and I'll automatically fill the CRM form.",
    },
  ]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // ----------------------------
  // Text To Speech
  // ----------------------------

  const speak = (text) => {
    if (!window.speechSynthesis || !text) return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = "en-US";
    utterance.rate = 1;

    window.speechSynthesis.speak(utterance);
  };

  // ----------------------------
  // Send Message
  // ----------------------------

  const handleSend = async (text) => {
    if (!text.trim()) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
    ]);

    setLoading(true);

    try {
      console.log("Sending:", text);

      const response = await api.post("/chat", {
        message: text,
      });

      console.log("Response:", response);

      const data = response.data;

      console.log("Data:", data);

      // Update CRM Form
      if (data.form) {
        dispatch(updateMultipleFields(data.form));
      }

      // AI Reply
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            data.reply ||
            "Interaction logged successfully.",
        },
      ]);

      speak(data.reply);

    } catch (error) {

      console.error("Axios Error:", error);

      let message = "Unable to connect to backend.";

      if (error.response) {

        console.log(error.response);

        message =
          error.response.data?.detail ||
          JSON.stringify(error.response.data);

      } else if (error.message) {

        message = error.message;

      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "❌ " + message,
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

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-50 p-5 space-y-4">

        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message}
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
                  AI is analysing your interaction...
                </span>

              </div>

            </div>

          </div>
        )}

        <div ref={bottomRef} />

      </div>

      {/* Chat Input */}

      <div className="border-t p-5">

        <ChatInput
          onSend={handleSend}
          loading={loading}
        />

      </div>

    </div>
  );
}