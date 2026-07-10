import { useEffect, useRef, useState } from "react";
import {
  FaMicrophone,
  FaMicrophoneSlash,
  FaPaperPlane,
} from "react-icons/fa";
import { AiOutlineLoading3Quarters } from "react-icons/ai";

export default function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState("");

  const [liveTranscript, setLiveTranscript] = useState("");

  const [isListening, setIsListening] = useState(false);

  const [isProcessing, setIsProcessing] = useState(false);

  const recognitionRef = useRef(null);

  const transcriptRef = useRef("");

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";

    // Keep listening until user presses Stop
    recognition.continuous = true;

    recognition.interimResults = true;

    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      console.log("🎤 Recording Started");

      transcriptRef.current = "";

      setMessage("");

      setLiveTranscript("");

      setIsListening(true);

      setIsProcessing(false);
    };

    recognition.onresult = (event) => {
      let interim = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        const transcript =
          event.results[i][0].transcript;

        if (event.results[i].isFinal) {
          transcriptRef.current +=
            transcript + " ";
        } else {
          interim += transcript;
        }
      }

      setLiveTranscript(interim);

      const finalText =
        (
          transcriptRef.current +
          " " +
          interim
        ).trim();

      setMessage(finalText);

      console.log(
        "Current Transcript:",
        finalText
      );
    };

    recognition.onerror = (event) => {
      console.log(
        "Speech Error:",
        event.error
      );

      setIsListening(false);

      setIsProcessing(false);

      setLiveTranscript("");

      if (
        event.error === "not-allowed"
      ) {
        alert(
          "Please allow microphone access."
        );
      }
    };

    recognition.onend = () => {
      console.log(
        "🎤 Recording Finished"
      );

      setIsListening(false);

      setIsProcessing(false);

      setLiveTranscript("");

      setMessage(
        transcriptRef.current.trim()
      );
    };

    recognitionRef.current =
      recognition;
  }, []);

  const startListening = () => {
    if (!recognitionRef.current) return;

    transcriptRef.current = "";

    setMessage("");

    setLiveTranscript("");

    recognitionRef.current.start();
  };

  const stopListening = () => {
    if (!recognitionRef.current) return;

    setIsProcessing(true);

    recognitionRef.current.stop();
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const text = message.trim();

    if (!text) return;

    console.log(
      "Sending Voice/Text:",
      text
    );

    onSend(text);

    transcriptRef.current = "";

    setMessage("");

    setLiveTranscript("");
  };
    return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4"
    >
      {/* Voice Status */}

      {(isListening || isProcessing) && (
        <div className="mb-4 rounded-xl border border-blue-200 bg-blue-50 p-3 dark:border-blue-700 dark:bg-blue-900/20">

          <div className="flex items-center gap-2 mb-2">

            <span
              className={`h-3 w-3 rounded-full ${
                isListening
                  ? "bg-red-500 animate-pulse"
                  : "bg-blue-500 animate-pulse"
              }`}
            />

            <p className="font-semibold text-sm text-blue-700 dark:text-blue-300">
              {isListening
                ? "🎤 Listening..."
                : "⏳ Processing..."}
            </p>

          </div>

          {liveTranscript && (
            <p className="italic text-gray-700 dark:text-gray-300 text-sm">
              {liveTranscript}
            </p>
          )}

        </div>
      )}

      {/* Text Area */}

      <textarea
        rows={4}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Describe your interaction with the healthcare professional..."
        className="w-full resize-none rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
      />

      {/* Bottom */}

      <div className="mt-4 flex items-center justify-between">

        <div className="flex items-center gap-3">

          {!isListening ? (
            <button
              type="button"
              onClick={startListening}
              className="flex h-12 w-12 items-center justify-center rounded-full bg-red-500 text-white hover:bg-red-600 transition"
            >
              <FaMicrophone size={18} />
            </button>
          ) : (
            <button
              type="button"
              onClick={stopListening}
              className="flex h-12 w-12 items-center justify-center rounded-full bg-red-700 text-white animate-pulse"
            >
              <FaMicrophoneSlash size={18} />
            </button>
          )}

          <span className="text-sm text-gray-500">
            {isListening
              ? "Recording..."
              : isProcessing
              ? "Finalizing..."
              : "Ready"}
          </span>

        </div>

        <button
          type="submit"
          disabled={loading || !message.trim()}
          className="flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <AiOutlineLoading3Quarters className="animate-spin" />
              Sending...
            </>
          ) : (
            <>
              <FaPaperPlane />
              Send
            </>
          )}
        </button>

      </div>

      <div className="mt-3 flex items-center justify-between text-xs text-gray-500">

        <span>
          {isListening
            ? "🎤 Listening"
            : isProcessing
            ? "⏳ Processing"
            : "✅ Ready"}
        </span>

        <span>
          {message.length} characters
        </span>

      </div>

    </form>
  );
}