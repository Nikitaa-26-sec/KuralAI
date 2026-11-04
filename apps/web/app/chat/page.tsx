
"use client";

import { useEffect, useRef, useState } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import Link from "next/link";

type Source = {
  title: string;
  page: number;
  chunk: number;
  distance: number;
};

type Message = {
  role: "assistant" | "user";
  content: string;
  sources?: Source[];
};

type Language = "English" | "Tamil" | "Hindi";
type Mode = "legal" | "fir";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const legalSuggestions = [
  "What is workplace sexual harassment?",
  "Who handles a workplace harassment complaint?",
  "What is the complaint filing time limit under the POSH Act?",
];

const firSuggestions = [
  "How do I file an FIR?",
  "What information should I prepare before reporting an incident?",
  "What can I do if police refuse to register my complaint?",
  "How do I report cybercrime in India?",
  "What should I do after filing an FIR?",
];

const initialMessage: Message = {
  role: "assistant",
  content:
    "Hello! I'm KuralAI, your legal information assistant. Ask a question about the legal documents indexed in this system.",
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([initialMessage]);
  const [input, setInput] = useState("");
  const [language, setLanguage] = useState<Language>("English");
  const [mode, setMode] = useState<Mode>("legal");
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("Checking...");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const requestedMode = params.get("mode");

    if (requestedMode === "fir") {
      setMode("fir");
      setMessages([
        {
          role: "assistant",
          content:
            "Welcome to FIR Process Assistance. I can explain how to report an incident, what information to prepare, and what may happen after reporting. I cannot register or submit a complaint.",
        },
      ]);
    }

    async function checkHealth() {
      try {
        const response = await fetch(`${API_URL}/health`);
        if (!response.ok) throw new Error("API unavailable");
        setApiStatus("Online");
      } catch {
        setApiStatus("Offline");
      }
    }

    checkHealth();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(
    event?: FormEvent<HTMLFormElement>,
    suggestion?: string
  ) {
    event?.preventDefault();

    const question = (suggestion ?? input).trim();

    if (!question || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: question },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: question,
          language,
          mode,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to get a response from KuralAI."
        );
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);

      setApiStatus("Online");
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Something went wrong. Please try again.",
        },
      ]);

      setApiStatus("Offline");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void sendMessage();
    }
  }

  function changeMode(nextMode: Mode) {
    setMode(nextMode);

    setMessages([
      {
        role: "assistant",
        content:
          nextMode === "fir"
            ? "Welcome to FIR Process Assistance. Ask me about reporting an incident, preparing information, or what happens after an FIR. I do not register or submit complaints."
            : initialMessage.content,
      },
    ]);

    setInput("");

    window.history.replaceState(
      {},
      "",
      nextMode === "fir" ? "/chat?mode=fir" : "/chat"
    );
  }

  const suggestions =
    mode === "fir" ? firSuggestions : legalSuggestions;

  const colors = {
    background: "#f4f7fa",
    navy: "#17334c",
    teal: "#159b91",
    text: "#172638",
    muted: "#718096",
    border: "#e2e8f0",
    white: "#ffffff",
  };

  return (
    <main
      style={{
        minHeight: "100vh",
        background: colors.background,
        color: colors.text,
        fontFamily: "Arial, sans-serif",
      }}
    >
      <header
        style={{
          minHeight: 72,
          background: colors.white,
          borderBottom: `1px solid ${colors.border}`,
          padding: "14px 5%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 16,
          flexWrap: "wrap",
        }}
      >
        <Link
          href="/"
          style={{
            color: colors.navy,
            textDecoration: "none",
            fontSize: 23,
            fontWeight: 800,
          }}
        >
          Kural<span style={{ color: colors.teal }}>AI</span>
        </Link>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            flexWrap: "wrap",
          }}
        >
          <span style={{ color: colors.muted, fontSize: 13 }}>
            <span
              style={{
                display: "inline-block",
                width: 8,
                height: 8,
                borderRadius: "50%",
                background:
                  apiStatus === "Online" ? colors.teal : "#d69e36",
                marginRight: 7,
              }}
            />
            API {apiStatus}
          </span>

          <Link href="/" style={{ color: colors.navy, fontSize: 13 }}>
            Back to home
          </Link>
        </div>
      </header>

      <div
        style={{
          width: "min(1200px, 94%)",
          margin: "32px auto",
          display: "grid",
          gridTemplateColumns: "minmax(220px, 280px) minmax(0, 1fr)",
          gap: 24,
        }}
      >
        <aside
          style={{
            background: colors.white,
            border: `1px solid ${colors.border}`,
            borderRadius: 14,
            padding: 22,
            alignSelf: "start",
          }}
        >
          <p
            style={{
              color: colors.teal,
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: 1.5,
            }}
          >
            YOUR LEGAL INFORMATION ASSISTANT
          </p>

          <h1 style={{ fontSize: 29, lineHeight: 1.2 }}>
            Ask with confidence.
          </h1>

          <p style={{ color: colors.muted, lineHeight: 1.7 }}>
            Understand legal information through answers grounded in
            indexed documents.
          </p>

          <div style={{ marginTop: 25 }}>
            <p style={{ fontWeight: 700, fontSize: 14 }}>
              Choose assistance
            </p>

            <button
              onClick={() => changeMode("legal")}
              style={{
                width: "100%",
                padding: 12,
                marginBottom: 9,
                border: `1px solid ${colors.border}`,
                borderRadius: 8,
                background:
                  mode === "legal" ? colors.navy : colors.white,
                color: mode === "legal" ? colors.white : colors.text,
                cursor: "pointer",
                textAlign: "left",
              }}
            >
              Legal Q&A
            </button>

            <button
              onClick={() => changeMode("fir")}
              style={{
                width: "100%",
                padding: 12,
                border: `1px solid ${colors.border}`,
                borderRadius: 8,
                background:
                  mode === "fir" ? colors.navy : colors.white,
                color: mode === "fir" ? colors.white : colors.text,
                cursor: "pointer",
                textAlign: "left",
              }}
            >
              FIR Process Assistance
            </button>
          </div>

          <div style={{ marginTop: 25 }}>
            <label
              htmlFor="language"
              style={{ fontWeight: 700, fontSize: 14 }}
            >
              Response language
            </label>

            <select
              id="language"
              value={language}
              onChange={(event) =>
                setLanguage(event.target.value as Language)
              }
              style={{
                width: "100%",
                marginTop: 9,
                padding: 11,
                borderRadius: 8,
                border: `1px solid ${colors.border}`,
                background: colors.white,
              }}
            >
              <option value="English">English</option>
              <option value="Tamil">Tamil</option>
              <option value="Hindi">Hindi</option>
            </select>
          </div>

          {mode === "fir" && (
            <div
              style={{
                marginTop: 25,
                padding: 14,
                background: "#f0f8f7",
                borderRadius: 9,
                fontSize: 13,
                lineHeight: 1.7,
              }}
            >
              <strong>Official services</strong>
              <p>
                Emergency:{" "}
                <a
                  href="https://112.gov.in/"
                  target="_blank"
                  rel="noreferrer"
                >
                  112 India
                </a>
              </p>
              <p>
                Cybercrime:{" "}
                <a
                  href="https://cybercrime.gov.in/"
                  target="_blank"
                  rel="noreferrer"
                >
                  National Cyber Crime Portal
                </a>
              </p>
            </div>
          )}
        </aside>

        <section
          style={{
            minWidth: 0,
            minHeight: "75vh",
            background: colors.white,
            border: `1px solid ${colors.border}`,
            borderRadius: 14,
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              padding: 22,
              borderBottom: `1px solid ${colors.border}`,
            }}
          >
            <p
              style={{
                margin: 0,
                color: colors.teal,
                fontSize: 11,
                fontWeight: 700,
                letterSpacing: 1.5,
              }}
            >
              KURALAI ASSISTANT
            </p>

            <h2 style={{ marginBottom: 5, fontSize: 22 }}>
              {mode === "fir"
                ? "FIR Process Assistance"
                : "Legal guidance, made clearer."}
            </h2>

            <p style={{ margin: 0, color: colors.muted, fontSize: 13 }}>
              {mode === "fir"
                ? "Understand the reporting process and available official services."
                : "Ask questions about the legal documents indexed in this system."}
            </p>
          </div>

          <div
            style={{
              flex: 1,
              padding: 22,
              display: "flex",
              flexDirection: "column",
              gap: 18,
            }}
          >
            {messages.map((message, index) => (
              <div
                key={index}
                style={{
                  alignSelf:
                    message.role === "user" ? "flex-end" : "flex-start",
                  maxWidth: "90%",
                  padding: 15,
                  borderRadius: 12,
                  background:
                    message.role === "user" ? "#eaf4f3" : "#f4f7fa",
                  lineHeight: 1.7,
                  whiteSpace: "pre-wrap",
                  overflowWrap: "anywhere",
                }}
              >
                <strong style={{ fontSize: 12 }}>
                  {message.role === "user" ? "You" : "KuralAI"}
                </strong>

                <p style={{ marginBottom: 5 }}>{message.content}</p>
              </div>
            ))}

            {loading && (
              <div
                style={{
                  alignSelf: "flex-start",
                  padding: 14,
                  background: "#f4f7fa",
                  borderRadius: 10,
                  color: colors.muted,
                }}
              >
                KuralAI is preparing your response...
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          <div
            style={{
              padding: "0 22px 14px",
              display: "flex",
              flexWrap: "wrap",
              gap: 8,
            }}
          >
            {suggestions.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => void sendMessage(undefined, suggestion)}
                disabled={loading}
                style={{
                  border: `1px solid ${colors.border}`,
                  borderRadius: 20,
                  padding: "8px 12px",
                  background: colors.white,
                  color: colors.navy,
                  fontSize: 12,
                  cursor: loading ? "not-allowed" : "pointer",
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>

          <form
            onSubmit={(event) => void sendMessage(event)}
            style={{
              display: "flex",
              gap: 10,
              padding: 18,
              borderTop: `1px solid ${colors.border}`,
            }}
          >
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              rows={2}
              maxLength={2000}
              disabled={loading}
              style={{
                flex: 1,
                minWidth: 0,
                resize: "vertical",
                padding: 12,
                border: `1px solid ${colors.border}`,
                borderRadius: 9,
                font: "inherit",
              }}
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              style={{
                alignSelf: "stretch",
                padding: "0 18px",
                border: "none",
                borderRadius: 9,
                background: colors.navy,
                color: colors.white,
                fontWeight: 700,
                cursor:
                  loading || !input.trim() ? "not-allowed" : "pointer",
                opacity: loading || !input.trim() ? 0.6 : 1,
              }}
            >
              Send
            </button>
          </form>

          <p
            style={{
              padding: "0 18px 16px",
              margin: 0,
              color: colors.muted,
              fontSize: 11,
              lineHeight: 1.6,
            }}
          >
            KuralAI provides general information, not legal advice or
            emergency assistance. It does not register or submit complaints.
            Legal answers depend on the documents indexed by this installation.
          </p>
        </section>
      </div>

      <style jsx>{`
        @media (max-width: 760px) {
          main > div {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </main>
  );
}
