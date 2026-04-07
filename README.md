# 🧠 BaraQura V10 — Advanced Cognitive AI Architecture

BaraQura V10 is a production-ready, multi-tiered AI orchestration system designed for high-stakes business logic and sales automation.

## 🚀 Key Features
- **Tiered Intelligence:** Smart fallback hierarchy (Local Memory ➔ Grok ➔ Gemini 1.5 Pro ➔ OpenAI).
- **Cognitive Persona Engine:** Dynamically switches between Analyst, Driver, Expressive, and Amiable modes.
- **Uncertainty Engine (UE):** Prevents AI hallucinations by identifying low-confidence intents.
- **Long-term Memory:** Persistent context management using MongoDB.
- **Enterprise Security:** Built-in rate limiting, role-based access, and prompt injection protection.

## 🛠️ Architecture Flow
1. **Request:** Incoming message via FastAPI.
2. **Analysis:** Intent & Emotion detection using Gemini.
3. **Control:** Controller decides the best LLM to use based on the Hierarchy.
4. **Execution:** Brain generates response using selected Persona.
5. **Memory:** Interaction is saved for future context.

## 📁 Structure
- `/core`: FastAPI Server & Business Controller.
- `/ai`: Core Brain, Persona, and Intent engines.
- `/integrations`: API connectors for Grok, Gemini, and OpenAI.
- `/database`: MongoDB connection & Repository.
