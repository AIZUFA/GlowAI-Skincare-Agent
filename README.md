# ✨ GlowAI — Multimodal AI Beauty Agent

> *"Because your skin deserves intelligent care."*

🚀 **[Live Demo → huggingface.co/spaces/jungkookswife/glowAI](https://huggingface.co/spaces/jungkookswife/glowAI)**

---

## 🌟 The Problem

The global skincare industry is worth over $500 billion — yet most people are completely overwhelmed by it. Thousands of products, conflicting advice, and ingredient lists that read like chemistry textbooks make finding the right routine feel impossible.

**GlowAI solves this** with an intelligent, multimodal AI beauty agent that sees, thinks, and responds like a luxury beauty consultant.

---

## ✨ What GlowAI Does

| Tab | Capability |
|-----|-----------|
| 🧴 **Skincare** | Text-based skin analysis, ingredient decoding, routine building, L'Oréal recommendations |
| 💄 **Makeup** | Face photo analysis, look tutorials, L'Oréal Group product matching |

---

## 🔧 6 Specialized Agent Tools

| # | Tool | Description |
|---|------|-------------|
| 1 | `analyze_skin` | Text-based skin profile assessment |
| 2 | `analyze_skin_image` | Gemini Vision skin photo analysis |
| 3 | `check_ingredient` | Ingredient safety & efficacy decoder |
| 4 | `generate_routine` | Personalized AM/PM routine builder |
| 5 | `suggest_loreal_skincare` | L'Oréal Paris product matching |
| 6 | `analyze_makeup_look` | Image/text makeup tutorial generator |

---

## 🏗️ Architecture

```
User Input (Text or Image)
         │
         ▼
┌─────────────────────────────────────┐
│         GlowAI Orchestrator         │
│        (Google ADK 2.0 Agent)       │
│       Model: Gemini 2.5 Flash       │
└─────────────────────────────────────┘
     │        │        │        │
     ▼        ▼        ▼        ▼
┌────────┐ ┌──────┐ ┌───────┐ ┌────────┐
│  Skin  │ │Ingre-│ │Routine│ │Makeup  │
│Analyzer│ │dient │ │Builder│ │Analyst │
│+ Vision│ │Check │ │+Loreal│ │+ Vision│
└────────┘ └──────┘ └───────┘ └────────┘
                    │
                    ▼
      Personalized Beauty Response
```

---

## 🧠 Key Concepts Demonstrated

| Concept | Implementation |
|---------|---------------|
| **Agentic AI (Google ADK)** | GlowAI orchestrator reasons and selects tools intelligently |
| **Agent Skills (6 Tools)** | analyze_skin, analyze_skin_image, check_ingredient, generate_routine, suggest_loreal_skincare, analyze_makeup_look |
| **Multimodal AI** | Gemini Vision for skin photo and makeup look analysis |
| **Memory** | InMemorySessionService for session context |
| **Security** | API keys via environment variables, never hardcoded |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Agent Framework | Google ADK 2.0 |
| Language Model | Gemini 2.5 Flash |
| Vision | Gemini Multimodal |
| UI | Gradio 4.x + Custom Luxury CSS |
| Deployment | HuggingFace Spaces |
| Language | Python 3.12 |

---

## 🚀 Run Locally

```bash
git clone https://github.com/AIZUFA/GlowAI-Skincare-Agent.git
cd GlowAI-Skincare-Agent
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

python app.py
# Open http://localhost:7860
```

Get your free API key at [aistudio.google.com](https://aistudio.google.com/app/apikey)

---

## 📁 Project Structure

```
GlowAI-Skincare-Agent/
├── app.py              # Main app — 6 tools + Gradio UI
├── requirements.txt    # Dependencies
├── Procfile            # Deployment config
├── railway.toml        # Railway config
└── README.md
```

---

## 💡 Why I Built This

I'm **Aiza Fatima**, a Robotics & Intelligent Systems student at Bahria University, Pakistan.

Earlier in 2026, I participated in **L'Oréal Brandstorm 2026** — a global innovation competition where I developed the *Affective Fragrance Synthesis* framework, an AI system that detects emotions through ocular biometrics to personalize fragrance experiences.

That experience revealed something powerful: **AI and beauty are not separate worlds.**

GlowAI is the natural next step — taking that intersection further by building an agent that doesn't just recommend products, but truly understands skin, sees it through computer vision, and personalizes every recommendation.

---

## 🎯 Track

**Freestyle** — Beauty AI at the intersection of dermatology, personalization, multimodal vision, and intelligent agent systems.

---

## 👩‍💻 Built By

**Aiza Fatima**
- 🎓 BS Robotics & Intelligent Systems, Bahria University Islamabad
- 🌸 L'Oréal Brandstorm 2026 Participant
- 🤖 GSoC 2026 Open Source Contributor
- 🔗 [LinkedIn](https://www.linkedin.com/in/aiza-fatima60/)
- 💻 [GitHub](https://github.com/AIZUFA)
- 🌐 [Portfolio](https://AIZUFA.github.io)

---

*Built with 💗 for the Google × Kaggle 5-Day Agentic AI Intensive Capstone 2026*
