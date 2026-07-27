import html
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(
    page_title="Lumina AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── App background ── */
.stApp {
    background: #111827;
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
:focus-visible { outline: 2px solid #6366f1 !important; outline-offset: 2px !important; }

/* ── Hide streamlit default padding ── */
.block-container { padding: 0 !important; max-width: 100% !important; }
.element-container { margin: 0 !important; }

/* ═══════════════════════════════════
   SIDEBAR — Ultra Premium Design
═══════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
    padding: 0;
    box-shadow: 4px 0 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    position: relative;
    overflow: hidden;
}
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: 
        radial-gradient(circle at 20% 30%, rgba(99,102,241,0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(139,92,246,0.1) 0%, transparent 50%);
    pointer-events: none;
}
section[data-testid="stSidebar"] > div { 
    padding: 40px 24px !important;
    position: relative;
    z-index: 1;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 28px 24px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    position: relative;
}
.sidebar-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
}
.sidebar-logo {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; flex-shrink: 0;
    box-shadow: 
        0 8px 24px rgba(99,102,241,0.5), 
        0 0 0 2px rgba(99,102,241,0.2),
        inset 0 1px 0 rgba(255,255,255,0.2);
    animation: logoPulse 3s ease-in-out infinite;
    position: relative;
}
.sidebar-logo::before {
    content: '';
    position: absolute;
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7, #6366f1);
    border-radius: 18px;
    z-index: -1;
    opacity: 0;
    filter: blur(8px);
    animation: logoGlow 3s ease-in-out infinite;
}
@keyframes logoPulse {
    0%, 100% { box-shadow: 0 8px 24px rgba(99,102,241,0.5), 0 0 0 2px rgba(99,102,241,0.2); }
    50% { box-shadow: 0 8px 32px rgba(99,102,241,0.7), 0 0 0 3px rgba(99,102,241,0.3); }
}
@keyframes logoGlow {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.6; }
}
.sidebar-title { 
    font-size: 1.15rem; font-weight: 800; color: white; 
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 0%, #e0e7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-sub { 
    font-size: 0.76rem; color: rgba(255,255,255,0.55); 
    margin-top: 3px; font-weight: 600; letter-spacing: 0.02em;
}

.sidebar-section { 
    padding: 28px 28px; 
    border-bottom: 1px solid rgba(255,255,255,0.08);
    position: relative;
}
.sidebar-section::before {
    content: '';
    position: absolute;
    bottom: 0; left: 24px; right: 24px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.sidebar-label {
    font-size: 0.72rem; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.15em; color: rgba(255,255,255,0.5); margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}
.sidebar-label::before {
    content: '';
    width: 8px; height: 8px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(99,102,241,0.5);
}

.status-pill {
    display: inline-flex; align-items: center; gap: 10px;
    background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(16,185,129,0.1));
    border: 1px solid rgba(16,185,129,0.4);
    padding: 8px 16px; border-radius: 100px;
    font-size: 0.8rem; color: #6ee7b7; font-weight: 700;
    box-shadow: 0 4px 16px rgba(16,185,129,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.status-pill::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}
.status-pill:hover::before {
    left: 100%;
}
.status-pill:hover {
    background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(16,185,129,0.15));
    border-color: rgba(16,185,129,0.6);
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 24px rgba(16,185,129,0.4), inset 0 1px 0 rgba(255,255,255,0.15);
}
.status-pill.offline {
    background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(239,68,68,0.1));
    border-color: rgba(239,68,68,0.4);
    color: #fca5a5;
    box-shadow: 0 4px 16px rgba(239,68,68,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
}
.status-pill.offline:hover {
    background: linear-gradient(135deg, rgba(239,68,68,0.3), rgba(239,68,68,0.15));
    border-color: rgba(239,68,68,0.6);
    box-shadow: 0 8px 24px rgba(239,68,68,0.4);
}
.status-dot { 
    width: 10px; height: 10px; border-radius: 50%; background: #10b981; 
    flex-shrink:0;
    box-shadow: 0 0 12px #10b981, 0 0 24px rgba(16,185,129,0.5);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 12px #10b981, 0 0 24px rgba(16,185,129,0.5); }
    50% { opacity: 0.8; transform: scale(1.15); box-shadow: 0 0 16px #10b981, 0 0 32px rgba(16,185,129,0.6); }
}
.status-dot.offline { background: #ef4444; box-shadow: 0 0 12px #ef4444, 0 0 24px rgba(239,68,68,0.5); }

.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.stat-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px; padding: 16px 18px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.stat-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
}
.stat-box::after {
    content: '';
    position: absolute;
    bottom: -50%; right: -50%;
    width: 100%; height: 100%;
    background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.stat-box:hover {
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
    border-color: rgba(255,255,255,0.2);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 32px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.1);
}
.stat-box:hover::after {
    opacity: 1;
}
.stat-val { 
    font-size: 1.5rem; font-weight: 900; color: white; 
    background: linear-gradient(135deg, #fff 0%, #c7d2fe 50%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.stat-key { 
    font-size: 0.72rem; color: rgba(255,255,255,0.5); 
    margin-top: 4px; font-weight: 700; letter-spacing: 0.03em;
    text-transform: uppercase;
}

.quick-action {
    display: flex; align-items: center; gap: 14px;
    padding: 14px 16px; border-radius: 14px;
    background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.85); font-size: 0.88rem; cursor: pointer;
    margin-bottom: 10px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-weight: 600;
    position: relative;
    overflow: hidden;
}
.quick-action::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #6366f1, #8b5cf6);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.quick-action:hover { 
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
    border-color: rgba(255,255,255,0.2);
    transform: translateX(6px);
    color: white;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.quick-action:hover::before {
    opacity: 1;
}
.qa-icon { font-size: 1.2rem; }

/* Slider overrides */
div[data-testid="stSlider"] label { 
    color: rgba(255,255,255,0.8) !important; 
    font-size: 0.88rem !important; 
    font-weight: 700 !important;
    letter-spacing: 0.02em;
}
div[data-testid="stSlider"] { margin-top: 0 !important; }
div[data-testid="stSlider"] [role="slider"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7) !important;
    box-shadow: 0 0 16px rgba(99,102,241,0.4) !important;
}

/* Clear button */
.stButton button {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.08)) !important;
    color: #fca5a5 !important;
    border: 1px solid rgba(239,68,68,0.35) !important;
    border-radius: 14px !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    padding: 12px 0 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100%;
    box-shadow: 0 6px 20px rgba(239,68,68,0.2), inset 0 1px 0 rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
}
.stButton button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transition: left 0.5s ease;
}
.stButton button:hover::before {
    left: 100%;
}
.stButton button:hover {
    background: linear-gradient(135deg, rgba(239,68,68,0.25), rgba(239,68,68,0.12)) !important;
    border-color: rgba(239,68,68,0.5) !important;
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(239,68,68,0.3), inset 0 1px 0 rgba(255,255,255,0.15);
}

/* ═══════════════════════════════════
   MAIN CHAT AREA
═══════════════════════════════════ */
.chat-wrapper {
    display: flex; flex-direction: column;
    height: 100vh; background: #111827; position: relative;
}

/* Topbar */
.topbar {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 24px;
    background: rgba(17,24,39,0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    position: sticky; top: 0; z-index: 100;
    flex-shrink: 0;
}
.topbar-avatar {
    width: 42px; height: 42px; border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.3);
}
.topbar-info { flex: 1; }
.topbar-name { font-size: 1rem; font-weight: 600; color: white; }
.topbar-status {
    font-size: 0.72rem; color: #10b981; margin-top: 1px;
    display: flex; align-items: center; gap: 5px;
}
.topbar-dot {
    width: 6px; height: 6px; background: #10b981;
    border-radius: 50%; display: inline-block;
}
.topbar-meta {
    font-size: 0.72rem; color: rgba(255,255,255,0.35);
    font-family: 'JetBrains Mono', monospace;
}

/* Messages scroll area */
.messages-area {
    flex: 1; overflow-y: auto; padding: 24px 16px;
    scroll-behavior: smooth;
}
.messages-area::-webkit-scrollbar { width: 5px; }
.messages-area::-webkit-scrollbar-track { background: transparent; }
.messages-area::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 10px; }

/* Date divider */
.date-divider {
    text-align: center; margin: 20px 0 16px;
    position: relative;
}
.date-divider span {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.4); font-size: 0.7rem;
    padding: 4px 12px; border-radius: 100px;
    font-family: 'JetBrains Mono', monospace; letter-spacing: 0.04em;
}

/* Message rows */
.msg-row {
    display: flex; gap: 10px; margin-bottom: 4px;
    align-items: flex-end; animation: msgIn 0.22s ease;
}
.msg-row.user { justify-content: flex-end; }
@keyframes msgIn { from { opacity:0; transform: translateY(10px); } to { opacity:1; transform: translateY(0); } }

/* Group spacing */
.msg-row.group-start { margin-top: 16px; }
.msg-row.group-end   { margin-bottom: 12px; }

/* Avatars */
.msg-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0; margin-bottom: 2px;
}
.msg-avatar.ai   { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.msg-avatar.user { background: linear-gradient(135deg, #0ea5e9, #2563eb); }
.msg-avatar.hide { visibility: hidden; }

/* Bubble container */
.bubble-wrap { display: flex; flex-direction: column; max-width: min(68%, 560px); }
.bubble-wrap.user { align-items: flex-end; }

/* Bubble */
.bubble {
    padding: 10px 14px;
    font-size: 0.925rem; line-height: 1.6;
    word-break: break-word; white-space: pre-wrap;
    position: relative;
}
/* AI bubble */
.bubble.ai {
    background: #1e2a3a;
    border: 1px solid rgba(255,255,255,0.08);
    color: rgba(255,255,255,0.92);
    border-radius: 4px 18px 18px 18px;
}
.bubble.ai.first { border-top-left-radius: 18px; border-bottom-left-radius: 4px; }
.bubble.ai.last  { border-top-left-radius: 4px;  border-bottom-left-radius: 18px; }
.bubble.ai.only  { border-radius: 18px; }

/* User bubble */
.bubble.user {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: white;
    border-radius: 18px 4px 18px 18px;
    box-shadow: 0 4px 14px rgba(99,102,241,0.3);
}
.bubble.user.first { border-top-right-radius: 18px; border-bottom-right-radius: 4px; }
.bubble.user.last  { border-top-right-radius: 4px;  border-bottom-right-radius: 18px; }
.bubble.user.only  { border-radius: 18px; }

/* Error bubble */
.bubble.error {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    color: #fca5a5;
    border-radius: 18px;
}

/* Timestamp */
.bubble-meta {
    font-size: 0.65rem; color: rgba(255,255,255,0.3);
    margin-top: 3px; padding: 0 2px;
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 5px;
}
.bubble-meta.user { justify-content: flex-end; }
.check-icon { color: #6366f1; }

/* Typing indicator */
.typing-row {
    display: flex; gap: 10px; align-items: flex-end;
    margin-top: 16px; margin-bottom: 12px;
    animation: msgIn 0.22s ease;
}
.typing-bubble {
    background: #1e2a3a; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px; padding: 12px 18px;
    display: flex; gap: 5px; align-items: center;
}
.typing-bubble span {
    width: 7px; height: 7px; border-radius: 50%;
    background: rgba(99,102,241,0.8);
    animation: typingBounce 1.2s infinite ease-in-out;
}
.typing-bubble span:nth-child(2) { animation-delay: 0.15s; }
.typing-bubble span:nth-child(3) { animation-delay: 0.3s; }
@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.35; }
    30%            { transform: translateY(-6px); opacity: 1; }
}

/* Empty state */
.empty-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; height: 55vh; text-align: center;
    color: rgba(255,255,255,0.35);
}
.empty-icon { font-size: 3rem; margin-bottom: 16px; opacity: 0.7; }
.empty-title { font-size: 1.2rem; font-weight: 600; color: rgba(255,255,255,0.7); margin-bottom: 6px; }
.empty-sub { font-size: 0.85rem; max-width: 280px; line-height: 1.6; }

.suggestion-chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 20px; }
.chip {
    background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25);
    color: rgba(255,255,255,0.65); padding: 6px 14px; border-radius: 100px;
    font-size: 0.78rem; cursor: default; transition: background 0.15s ease;
}

/* ═══════════════════════════════════════════════
   INPUT PILL — dark pill, no white anywhere
═══════════════════════════════════════════════ */

/* 1. Background of the fixed bottom bar */
[data-testid="stBottom"] {
    background: #1a1a1a !important;
    border-top: none !important;
    padding: 12px 20px 16px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    border-radius: 50px 50px 0 0 !important;
    box-shadow: 0 -2px 20px rgba(0,0,0,0.4) !important;
}
[data-testid="stBottom"] > div {
    background: #1a1a1a !important;
    border-top: none !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    border-radius: 50px 50px 0 0 !important;
}

/* 2. Container — centres & max-widths the pill */
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
[data-testid="stChatInputContainer"] > form {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    max-width: 720px !important;
    width: 100% !important;
}

/* 3. The pill itself - dark grey rounded rectangle */
[data-testid="stChatInput"] {
    background: #2a2a2a !important;
    border: none !important;
    border-radius: 999px !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    position: relative !important;
    padding: 0 !important;
    min-height: 38px !important;
    overflow: hidden !important;
}
[data-testid="stChatInput"]:focus-within {
    border: none !important;
    box-shadow: none !important;
}
/* Additional border removal for all nested elements */
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] form,
[data-testid="stChatInput"] form > div,
[data-testid="stChatInput"] input[type="text"],
[data-testid="stChatInput"] textarea {
    border: none !important;
    border-width: 0px !important;
    box-shadow: none !important;
    outline: none !important;
    background: #2a2a2a !important;
}
/* Force remove borders and set dark background — EXCLUDING button children */
[data-testid="stChatInput"] *:not(button):not(button *):not(svg):not(svg *):not(path):not(circle) {
    border: none !important;
    border-width: 0px !important;
    outline: none !important;
    background: #2a2a2a !important;
}

/* Button children must always be transparent — no dark box behind the arrow */
[data-testid="stChatInput"] button svg,
[data-testid="stChatInput"] button svg *,
[data-testid="stChatInput"] button path,
[data-testid="stChatInput"] button circle,
[data-testid="stChatInput"] button span {
    background: transparent !important;
    background-color: transparent !important;
}

/* 4. "+" on the far left - white plus icon */
[data-testid="stChatInput"]::before {
    content: "+";
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: white !important;
    font-size: 1.4rem;
    font-weight: 400;
    pointer-events: none;
    z-index: 2;
    line-height: 1;
}



/* 6. Textarea - sits between the + and the right elements */
[data-testid="stChatInput"] textarea {
    background: #2a2a2a !important;
    color: rgba(255,255,255,0.9) !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    caret-color: rgba(255,255,255,0.7) !important;
    border: none !important;
    box-shadow: none !important;
    padding: 8px 160px 8px 50px !important;
    resize: none !important;
    line-height: 1.4 !important;
    min-height: 24px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255,255,255,0.4) !important;
}

/* 7. Send button — base layout (shared) */
[data-testid="stChatInput"] button {
    border-radius: 50% !important;
    border: none !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: absolute !important;
    right: 8px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    box-shadow: none !important;
    transition: background 0.18s ease, opacity 0.18s ease !important;
}

/* EMPTY — gray, not-allowed cursor */
[data-testid="stChatInput"] button:disabled,
[data-testid="stChatInput"] button[disabled] {
    background: #383838 !important;
    cursor: not-allowed !important;
    opacity: 0.55 !important;
}
[data-testid="stChatInput"] button:disabled svg,
[data-testid="stChatInput"] button[disabled] svg {
    fill: rgba(255,255,255,0.35) !important;
    width: 16px !important;
    height: 16px !important;
}

/* HAS TEXT — white button, pointer cursor */
[data-testid="stChatInput"] button:not(:disabled):not([disabled]) {
    background: #ffffff !important;
    cursor: pointer !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button:not(:disabled):not([disabled]) svg {
    fill: #0d0d0d !important;
    width: 16px !important;
    height: 16px !important;
}
[data-testid="stChatInput"] button:not(:disabled):not([disabled]):hover {
    background: #e5e7eb !important;
    transform: translateY(-50%) scale(1.06) !important;
}


/* ── 8. Kill the white rounded card Streamlit wraps around stBottom ── */
.stChatInput,
div:has(> [data-testid="stChatInput"]),
[data-testid="stBottom"] > div > div {
    background: #1a1a1a !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
}
/* Catch-all: any direct children of stBottom that have white bg */
[data-testid="stBottom"] > div > * {
    background: #1a1a1a !important;
    border: none !important;
    box-shadow: none !important;
}
section.main > div > div > div > div > div:last-child,
.stApp > div:last-child,
.stApp > section > div:last-child {
    background: #1a1a1a !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# State initialisation
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = False
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now().strftime("%H:%M")
if "total_chars" not in st.session_state:
    st.session_state.total_chars = 0

api_key_present = bool(os.getenv("GOOGLE_API_KEY"))

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    # Header
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">✨</div>
        <div>
            <div class="sidebar-title">Lumina AI</div>
            <div class="sidebar-sub">Powered by Gemini</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Connection</div>', unsafe_allow_html=True)
    if api_key_present:
        st.markdown('<div class="status-pill"><span class="status-dot"></span>Online & Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill offline"><span class="status-dot offline"></span>API Key Missing</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Settings
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Model Settings</div>', unsafe_allow_html=True)
    temp = st.slider("🌡 Creativity", 0.0, 1.2, 0.7, 0.1,
                      help="Higher = more creative, Lower = more focused")
    st.markdown('</div>', unsafe_allow_html=True)

    # Session stats
    turns = sum(1 for m in st.session_state.messages if m["role"] == "user")
    ai_turns = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    st.markdown(f"""
    <div class="sidebar-section">
        <div class="sidebar-label">Session Stats</div>
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-val">{turns}</div>
                <div class="stat-key">Messages</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{ai_turns}</div>
                <div class="stat-key">Replies</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{st.session_state.session_start}</div>
                <div class="stat-key">Started</div>
            </div>
            <div class="stat-box">
                <div class="stat-val">{len(st.session_state.messages)}</div>
                <div class="stat-key">Total</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Actions
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Actions</div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending = False
        st.session_state.total_chars = 0
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if not api_key_present:
        st.warning("⚠️ Add GOOGLE_API_KEY to your .env file to start chatting.")


# ─────────────────────────────────────────────
# LLM
# ─────────────────────────────────────────────
@st.cache_resource
def get_llm(t):
    return ChatGoogleGenerativeAI(model="models/gemini-3.5-flash", temperature=t)


def esc(text: str) -> str:
    return html.escape(text)


# ─────────────────────────────────────────────
# Build chat HTML
# ─────────────────────────────────────────────
def build_messages_html(messages, pending):
    if not messages:
        return ""

    rows = []
    today = datetime.now().strftime("%B %d, %Y")
    rows.append(f'<div class="date-divider"><span>Today — {today}</span></div>')

    # Group consecutive messages by role for WhatsApp-style grouping
    groups = []
    for m in messages:
        if groups and groups[-1][0]["role"] == m["role"]:
            groups[-1].append(m)
        else:
            groups.append([m])

    for group in groups:
        role = group[0]["role"]
        is_user = role == "user"
        is_error = group[0].get("error", False)

        for i, m in enumerate(group):
            content = esc(m["content"])
            ts = m.get("time", "")
            is_first = (i == 0)
            is_last  = (i == len(group) - 1)
            is_only  = (len(group) == 1)

            # bubble shape class
            if is_only:
                shape = "only"
            elif is_first:
                shape = "first"
            elif is_last:
                shape = "last"
            else:
                shape = ""

            # row grouping classes
            row_cls = "msg-row"
            if is_first: row_cls += " group-start"
            if is_last:  row_cls += " group-end"
            if is_user:  row_cls += " user"

            # Avatar: only show on first message of group (for AI) or last (for user)
            show_avatar_ai   = is_first and not is_user
            show_avatar_user = is_first and is_user

            if is_user:
                avatar_html = f'<div class="msg-avatar user {"" if show_avatar_user else "hide"}">👤</div>'
                bubble_cls  = "bubble user " + shape
                meta_cls    = "bubble-meta user"
                meta_html   = f'<div class="{meta_cls}">{ts} <span class="check-icon">✓✓</span></div>'
                rows.append(
                    f'<div class="{row_cls}">'
                    f'<div class="bubble-wrap user">'
                    f'<div class="{bubble_cls}">{content}</div>'
                    f'{meta_html if is_last else ""}'
                    f'</div>'
                    f'{avatar_html}'
                    f'</div>'
                )
            else:
                avatar_html = f'<div class="msg-avatar ai {"" if show_avatar_ai else "hide"}">✦</div>'
                if is_error:
                    bubble_cls = "bubble error"
                    meta_cls   = "bubble-meta"
                else:
                    bubble_cls = "bubble ai " + shape
                    meta_cls   = "bubble-meta"
                meta_html = f'<div class="{meta_cls}">Lumina · {ts}</div>'
                rows.append(
                    f'<div class="{row_cls}">'
                    f'{avatar_html}'
                    f'<div class="bubble-wrap">'
                    f'<div class="{bubble_cls}">{content}</div>'
                    f'{meta_html if is_last else ""}'
                    f'</div>'
                    f'</div>'
                )

    if pending:
        rows.append("""
        <div class="typing-row">
            <div class="msg-avatar ai">✦</div>
            <div class="typing-bubble">
                <span></span><span></span><span></span>
            </div>
        </div>
        """)

    return "".join(rows)


# ─────────────────────────────────────────────
# Topbar
# ─────────────────────────────────────────────
status_text = "Online · Gemini 3.5 Flash" if api_key_present else "Offline — API key missing"
status_color = "#10b981" if api_key_present else "#ef4444"
topbar_dot = "topbar-dot" if api_key_present else "topbar-dot" 

st.markdown(f"""
<div class="topbar">
    <div class="topbar-avatar">✨</div>
    <div class="topbar-info">
        <div class="topbar-name">Lumina AI</div>
        <div class="topbar-status" style="color:{status_color};">
            <span class="topbar-dot" style="background:{status_color};"></span>
            {status_text}
        </div>
    </div>
    <div class="topbar-meta">{datetime.now().strftime("%H:%M")}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Messages area
# ─────────────────────────────────────────────
msgs_html = build_messages_html(st.session_state.messages, st.session_state.pending)

st.markdown(f"""
<div class="messages-area" id="messages-area">
    {msgs_html}
</div>
""", unsafe_allow_html=True)

# Auto-scroll
st.components.v1.html("""
<script>
    (function() {
        function scrollToBottom() {
            var areas = window.parent.document.querySelectorAll('.messages-area');
            areas.forEach(function(el) { el.scrollTop = el.scrollHeight; });
        }
        scrollToBottom();
        setTimeout(scrollToBottom, 80);
        setTimeout(scrollToBottom, 250);
        
        // Force remove borders and set dark background on input
        function fixInputStyles() {
            var chatInput = window.parent.document.querySelector('[data-testid="stChatInput"]');
            if (chatInput) {
                // Target all parent containers
                var parents = chatInput.closest('[data-testid="stBottom"]');
                if (parents) {
                    parents.style.background = '#0d0d0d';
                    parents.style.border = 'none';
                    var grandParent = parents.parentElement;
                    if (grandParent) {
                        grandParent.style.background = '#0d0d0d';
                        grandParent.style.border = 'none';
                    }
                }
                
                var container = chatInput.closest('[data-testid="stChatInputContainer"]');
                if (container) {
                    container.style.background = 'transparent';
                    container.style.border = 'none';
                }

                var mainContainer = window.parent.document.querySelector('.main .block-container');
                if (mainContainer) {
                    mainContainer.style.background = '#0d0d0d';
                }

                var appContainer = window.parent.document.querySelector('.stApp');
                if (appContainer) {
                    appContainer.style.background = '#0d0d0d';
                }

                var bodyElement = window.parent.document.querySelector('body');
                if (bodyElement) {
                    bodyElement.style.background = '#0d0d0d';
                }
                
                chatInput.style.background = '#2a2a2a';
                chatInput.style.border = 'none';
                chatInput.style.boxShadow = 'none';
                
                var allElements = chatInput.querySelectorAll('*');
                allElements.forEach(function(el) {
                    el.style.background = '#2a2a2a';
                    el.style.border = 'none';
                    el.style.borderWidth = '0px';
                    el.style.outline = 'none';
                    el.style.boxShadow = 'none';
                });

                // Handle button state based on input
                var textarea = chatInput.querySelector('textarea');
                var sendButton = chatInput.querySelector('button');
                
                function updateButtonState() {
                    if (textarea && sendButton) {
                        var hasText = textarea.value.trim().length > 0;
                        if (hasText) {
                            sendButton.style.background = 'white';
                            sendButton.style.pointerEvents = 'auto';
                            sendButton.style.opacity = '1';
                        } else {
                            sendButton.style.background = '#3a3a3a';
                            sendButton.style.pointerEvents = 'none';
                            sendButton.style.opacity = '0.5';
                        }
                    }
                }
                
                if (textarea) {
                    textarea.addEventListener('input', updateButtonState);
                    updateButtonState(); // Initial state
                }
            }
        }
        
        setTimeout(fixInputStyles, 100);
        setTimeout(fixInputStyles, 500);
        setTimeout(fixInputStyles, 1000);
    })();
</script>
""", height=0)

# ─────────────────────────────────────────────
# Input
# ─────────────────────────────────────────────
st.markdown('<div class="input-area">', unsafe_allow_html=True)
prompt = st.chat_input(
    "Ask anything",
    disabled=st.session_state.pending or not api_key_present
)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Message flow — two-pass: show user msg + typing → fetch → show reply
# ─────────────────────────────────────────────
if prompt and not st.session_state.pending:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "time": datetime.now().strftime("%H:%M"),
    })
    st.session_state.pending = True
    st.rerun()

if st.session_state.pending:
    try:
        llm = get_llm(temp)

        from langchain_core.messages import AIMessage, HumanMessage
        history = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                history.append(HumanMessage(content=msg["content"]))
            elif not msg.get("error"):
                history.append(AIMessage(content=msg["content"]))

        res = llm.invoke(history)

        if isinstance(res.content, list):
            text = ""
            for block in res.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text += block.get("text", "")
                elif isinstance(block, str):
                    text += block
        else:
            text = str(res.content)

        st.session_state.messages.append({
            "role": "assistant",
            "content": text,
            "time": datetime.now().strftime("%H:%M"),
        })
    except Exception as e:
        err = str(e)
        if "404" in err:
            friendly = "Model not found. Please check your GOOGLE_API_KEY in .env file."
        elif "429" in err or "quota" in err.lower():
            friendly = "⚠️ Free quota exceeded. Please wait ~60 seconds and try again, or enable billing at https://aistudio.google.com"
        else:
            friendly = f"Something went wrong: {err[:300]}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": friendly,
            "time": datetime.now().strftime("%H:%M"),
            "error": True,
        })
    finally:
        st.session_state.pending = False
        st.rerun()