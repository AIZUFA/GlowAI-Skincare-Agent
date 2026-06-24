# GlowAI 🌸✨
### Your Personal AI Skincare Agent — Powered by Google ADK & Gemini

> *"Because your skin deserves intelligent care."*

---

## 🌟 The Problem

The global skincare industry is worth over $500 billion — yet most people are completely overwhelmed by it. With thousands of products, conflicting advice, and ingredient lists that read like chemistry textbooks, finding the right routine feels impossible.

People with acne buy the wrong products. People with sensitive skin unknowingly use irritating ingredients. Dark spots get worse because of the wrong SPF. The information exists — but it's fragmented, confusing, and not personalized.

**GlowAI solves this.**

---

## ✨ The Solution

GlowAI is a multi-agent AI skincare assistant that acts as your personal dermatology-informed guide. It doesn't just answer questions — it reasons, uses tools, remembers you, and builds a complete skincare strategy tailored to your unique skin profile.

**What GlowAI can do:**
- 🔍 Analyze your skin type and concerns
- 🧴 Check any skincare ingredient for safety and effectiveness
- 📋 Generate a complete personalized morning + night routine
- 🧠 Remember your skin profile across sessions
- 🔐 Handle your data securely

---

## 🏗️ Architecture
User Input
│
▼
┌─────────────────────────────────┐
│ GlowAI Orchestrator │
│ (Google ADK Agent) │
│ Model: Gemini 2.5 Flash │
└─────────────────────────────────┘
│ │ │
▼ ▼ ▼
┌─────────┐ ┌─────────┐ ┌──────────────┐
│ Skin │ │Ingredient│ │ Routine │
│Analyzer │ │ Checker │ │ Generator │
│ Tool │ │ Tool │ │ Tool │
└─────────┘ └─────────┘ └──────────────┘
│ │ │
└───────────┴────────────┘
│
▼
Personalized Skincare Response
+ Memory stored for next session
---

## 🧠 Key Concepts Demonstrated

| Concept | Where |
|---|---|
| Agent / Multi-agent system (ADK) | Core GlowAI orchestrator with 3 specialized tools |
| Agent Skills | analyze_skin, check_ingredient, generate_routine |
| Security Features | API key protection via environment variables, input validation |
| Memory | InMemorySessionService for persistent user skin profiles |

---

## 🛠️ Tech Stack

- **Google ADK 2.0** — Agent framework
- **Gemini 2.5 Flash** — Underlying LLM
- **Python 3.12** — Core language
- **Google Colab** — Development environment
- **Google Generative AI SDK** — API integration

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AIZUFA/GlowAI-Skincare-Agent.git
cd GlowAI-Skincare-Agent
```

### 2. Install dependencies
```bash
pip install google-adk google-genai anthropic pillow requests python-dotenv
```

### 3. Set up API keys
Create a `.env` file:
GOOGLE_API_KEY=your_google_api_key_here
Or in Google Colab, add to Secrets:
- `GOOGLE_API_KEY`

### 4. Run the notebook
Open `GlowAI.ipynb` in Google Colab and run all cells!

---

## 💡 Why I Built This

I'm Aiza Fatima, a Robotics & Intelligent Systems student at Bahria University, Pakistan. I participated in **L'Oréal Brandstorm 2026**, where I developed the Affective Fragrance Synthesis framework — merging AI with beauty and sensory experiences.

That experience showed me how powerful the intersection of AI and beauty can be. GlowAI is the next step — taking that passion and building something that genuinely helps people navigate the overwhelming world of skincare.

Built during the **Google x Kaggle 5-Day Agentic AI Intensive 2026** 🚀

---

## 📁 Project Structure
GlowAI-Skincare-Agent/
│
├── GlowAI.ipynb # Main Colab notebook
├── README.md # This file
├── requirements.txt # Dependencies
└── assets/
└── architecture.png # Architecture diagram
---

## 🎯 Track

**Freestyle** — Beauty AI at the intersection of dermatology, personalization, and intelligent agent systems.

---

## 👩‍💻 Built By

**Aiza Fatima**
- 🎓 BS Robotics & Intelligent Systems, Bahria University
- 🌸 L'Oréal Brandstorm 2026 Participant
- 🤖 GSoC 2026 Open Source Contributor
- 🔗 [LinkedIn](https://www.linkedin.com/in/aiza-fatima60/)
- 💻 [GitHub](https://github.com/AIZUFA)
- 🌐 [Portfolio](https://AIZUFA.github.io)

---

*Built with 💗 and AI for the Google x Kaggle Agentic AI Intensive Capstone 2026*
