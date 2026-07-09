import { useState, useRef } from "react";

export default function ChatInput({ onSend }) {
  const [text, setText] = useState("");
  const [listening, setListening] = useState(false);

  const recognitionRef = useRef(null);

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      let transcript = "";

      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript + " ";
      }

      setText(transcript.trim());
    };

    recognition.onerror = () => {
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();

    recognitionRef.current = recognition;
  };

  const stopListening = () => {
    recognitionRef.current?.stop();

    if (text.trim()) {
      onSend(text);
      setText("");
    }
  };

  const handleSend = () => {
    if (!text.trim()) return;

    onSend(text);
    setText("");
  };

  return (
    <div className="space-y-4">

      {/* Voice Status */}

      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-4 border">

        <div className="flex items-center gap-3">

          <div className="text-3xl">
            🤖
          </div>

          <div>

            <h3 className="font-bold text-lg">
              AI Voice Assistant
            </h3>

            <p className="text-sm text-gray-600">
              Speak naturally or type your interaction.
            </p>

          </div>

        </div>

      </div>

      {/* Recording */}

      {listening && (

        <div className="bg-red-50 border border-red-300 rounded-xl p-4">

          <div className="flex items-center gap-2 mb-3">

            <span className="w-3 h-3 rounded-full bg-red-600 animate-pulse"></span>

            <span className="font-semibold text-red-600">
              Listening...
            </span>

          </div>

          <div className="bg-white rounded-lg p-3 min-h-[70px] text-gray-700">

            {text || "Speak now..."}

          </div>

        </div>

      )}

      {/* Input */}

      <textarea
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Describe your interaction..."
        className="w-full border rounded-xl p-4 resize-none focus:ring-2 focus:ring-blue-500 outline-none"
      />

      {/* Buttons */}

      <div className="flex justify-between">

        <div className="flex gap-3">

          <button
            onClick={startListening}
            disabled={listening}
            className={`px-5 py-3 rounded-xl text-white font-semibold transition ${
              listening
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-green-600 hover:bg-green-700"
            }`}
          >
            🎤 Start Recording
          </button>

          <button
            onClick={stopListening}
            disabled={!listening}
            className={`px-5 py-3 rounded-xl text-white font-semibold transition ${
              listening
                ? "bg-red-600 hover:bg-red-700"
                : "bg-gray-400 cursor-not-allowed"
            }`}
          >
            ⏹ Stop Recording
          </button>

        </div>

        <button
          onClick={handleSend}
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-semibold transition"
        >
          🚀 Send
        </button>

      </div>

    </div>
  );
}