import os
import base64
import gradio as gr
from google import genai
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

# API Setup
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

# ── TOOLS ──────────────────────────────────────────────────────────────────────

def analyze_skin(skin_type: str, concerns: str) -> str:
    """Analyzes skin type and concerns to provide personalized advice."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"As GlowAI skincare expert, analyze {skin_type} skin with concerns: {concerns}. Give ingredient recommendations and routine structure."
    )
    return response.text

def analyze_skin_image(image_path: str) -> str:
    """Analyzes a skin photo and provides personalized skincare advice."""
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{
            "parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": image_data}},
                {"text": """You are GlowAI, an expert AI skincare assistant.
Analyze this skin photo and provide:
1. Skin type assessment
2. Visible skin concerns
3. Skin condition rating (1-10)
4. Top 3 ingredients needed RIGHT NOW
5. One thing to STOP doing immediately
6. Personalized encouragement message
Be warm, professional and specific to what you see."""}
            ]
        }]
    )
    return response.text

def check_ingredient(ingredient: str) -> str:
    """Checks if a skincare ingredient is safe and effective."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"As GlowAI, analyze the skincare ingredient '{ingredient}'. Is it safe? What does it do? Who should use/avoid it?"
    )
    return response.text

def generate_routine(skin_type: str, concerns: str, budget: str) -> str:
    """Generates a complete personalized skincare routine."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"As GlowAI, create a complete {budget} budget skincare routine for {skin_type} skin with {concerns}. Include morning and night steps."
    )
    return response.text

def suggest_loreal_skincare(skin_type: str, concerns: str) -> str:
    """Suggests specific L'Oréal Group skincare products."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""As GlowAI, recommend SPECIFIC L'Oréal Group products for {skin_type} skin with {concerns}.
Include products from: L'Oréal Paris, La Roche-Posay, Kiehl's, Lancôme, CeraVe, Vichy.
For each: product name, price range, key ingredients, why it's perfect, how to use."""
    )
    return response.text

def analyze_makeup_look(image_path: str) -> str:
    """Analyzes face and suggests makeup look with L'Oréal products."""
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{
            "parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": image_data}},
                {"text": """You are GlowAI, an expert AI beauty consultant.
Analyze this face and provide:
1. Face shape and features analysis
2. Recommended makeup look name and vibe
3. Step by step application guide
4. Specific L'Oréal Group product recommendations (L'Oréal Paris, Maybelline, NYX, Lancôme, YSL Beauty)
5. Pro tips for this person's features
Be warm and make them feel beautiful! ✨"""}
            ]
        }]
    )
    return response.text

# ── AGENT ──────────────────────────────────────────────────────────────────────

glow_agent = Agent(
    name="GlowAI",
    model="gemini-2.0-flash",
    description="Your personal AI Beauty Agent — skincare analysis, makeup looks, and L'Oréal product recommendations.",
    instruction="""You are GlowAI, a warm, knowledgeable and glamorous AI Beauty Assistant.

🧴 SKINCARE: Analyze skin from photos using analyze_skin_image, from text using analyze_skin, check ingredients using check_ingredient, generate routines using generate_routine, suggest L'Oréal products using suggest_loreal_skincare.

💄 MAKEUP: Analyze face photos and suggest makeup looks using analyze_makeup_look. Always recommend specific L'Oréal Group products.

ALWAYS be warm, encouraging and make users feel beautiful. Never diagnose medical conditions.""",
    tools=[
        FunctionTool(analyze_skin),
        FunctionTool(analyze_skin_image),
        FunctionTool(check_ingredient),
        FunctionTool(generate_routine),
        FunctionTool(suggest_loreal_skincare),
        FunctionTool(analyze_makeup_look),
    ]
)

# ── SESSION ─────────────────────────────────────────────────────────────────────

session_service = InMemorySessionService()

async def init_session():
    await session_service.create_session(
        app_name="GlowAI",
        user_id="user_001",
        session_id="session_001"
    )
    await session_service.create_session(
        app_name="GlowAI",
        user_id="user_001",
        session_id="session_002"
    )

asyncio.run(init_session())

runner = Runner(
    agent=glow_agent,
    app_name="GlowAI",
    session_service=session_service
)

# ── CHAT FUNCTIONS ──────────────────────────────────────────────────────────────

async def skincare_chat(message, image, history):
    response_text = ""
    try:
        if image is not None:
            result = analyze_skin_image(image)
            response_text = f"📸 **GlowAI Skin Analysis:**\n\n{result}"
        elif message:
            content = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
            async for event in runner.run_async(
                user_id="user_001",
                session_id="session_001",
                new_message=content
            ):
                if event.is_final_response():
                    response_text = event.content.parts[0].text

        history = history + [{"role": "user", "content": message or "📸 Skin photo uploaded"}, {"role": "assistant", "content": response_text}]
        return "", None, history

    except Exception as e:
        history = history + [{"role": "user", "content": message or "📸 Photo"}, {"role": "assistant", "content": "✨ GlowAI is taking a short break. Please try again in a moment! 🌸"}]
        return "", None, history

async def makeup_chat(message, image, history):
    response_text = ""
    try:
        if image is not None:
            result = analyze_makeup_look(image)
            response_text = f"💄 **GlowAI Makeup Analysis:**\n\n{result}"
        elif message:
            content = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
            async for event in runner.run_async(
                user_id="user_001",
                session_id="session_002",
                new_message=content
            ):
                if event.is_final_response():
                    response_text = event.content.parts[0].text

        history = history + [{"role": "user", "content": message or "📸 Face photo uploaded"}, {"role": "assistant", "content": response_text}]
        return "", None, history

    except Exception as e:
        history = history + [{"role": "user", "content": message or "📸 Photo"}, {"role": "assistant", "content": "✨ GlowAI is taking a short break. Please try again in a moment! 🌸"}]
        return "", None, history

# ── CSS ──────────────────────────────────────────────────────────────────────────

css = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500&display=swap');

* { font-family: 'Montserrat', sans-serif !important; }

body, .gradio-container {
    background: linear-gradient(135deg, #1a0a12 0%, #2d1a20 40%, #1a0d18 100%) !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.6; }
    50% { transform: translateY(-20px) rotate(5deg); opacity: 1; }
}
@keyframes float2 {
    0%, 100% { transform: translateY(0px) rotate(-5deg); opacity: 0.4; }
    50% { transform: translateY(-15px) rotate(0deg); opacity: 0.8; }
}
@keyframes float3 {
    0%, 100% { transform: translateY(0px) rotate(10deg); opacity: 0.5; }
    50% { transform: translateY(-25px) rotate(5deg); opacity: 0.9; }
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(255,182,193,0.1); }
    50% { box-shadow: 0 0 40px rgba(255,182,193,0.3); }
}
@keyframes sparkle {
    0%, 100% { opacity: 0; transform: scale(0); }
    50% { opacity: 1; transform: scale(1); }
}

.floating-decor {
    position: fixed;
    pointer-events: none;
    z-index: 0;
    font-size: 2em;
}
.lipstick-1 { top: 10%; left: 3%; animation: float 6s ease-in-out infinite; }
.lipstick-2 { top: 30%; right: 3%; animation: float2 8s ease-in-out infinite; }
.lipstick-3 { bottom: 20%; left: 5%; animation: float3 7s ease-in-out infinite; }
.sparkle-1 { top: 20%; left: 15%; animation: sparkle 3s ease-in-out infinite; font-size: 1em; }
.sparkle-2 { top: 60%; right: 10%; animation: sparkle 4s ease-in-out infinite 1s; font-size: 1.2em; }
.sparkle-3 { bottom: 30%; left: 20%; animation: sparkle 3.5s ease-in-out infinite 0.5s; font-size: 0.8em; }
.flower-1 { top: 5%; right: 15%; animation: float2 9s ease-in-out infinite; font-size: 1.5em; }
.flower-2 { bottom: 10%; right: 20%; animation: float 7s ease-in-out infinite 2s; font-size: 1.2em; }

.main-header {
    text-align: center;
    padding: 60px 20px 40px;
    position: relative;
    z-index: 1;
}

.glow-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 6em !important;
    font-weight: 300 !important;
    letter-spacing: 15px !important;
    background: linear-gradient(135deg, #FFB6C1, #FFD700, #FFB6C1, #F4A460, #FFB6C1) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shimmer 4s linear infinite !important;
    margin: 0 !important;
    text-transform: uppercase !important;
}

.glow-subtitle {
    font-family: 'Montserrat', sans-serif !important;
    color: #C9A0B0 !important;
    font-size: 0.7em !important;
    letter-spacing: 8px !important;
    text-transform: uppercase !important;
    margin: 15px 0 10px !important;
    font-weight: 300 !important;
}

.glow-tagline {
    font-family: 'Cormorant Garamond', serif !important;
    background: linear-gradient(135deg, #FFB6C1, #FFD700) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 1.3em !important;
    font-style: italic !important;
    font-weight: 300 !important;
    margin: 5px 0 !important;
}

.divider {
    width: 80px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #FFB6C1, #FFD700, #FFB6C1, transparent);
    margin: 20px auto;
}

.glow-powered {
    color: #6a4050 !important;
    font-size: 0.6em !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-weight: 300 !important;
}

.tab-nav {
    border-bottom: 1px solid rgba(255,182,193,0.2) !important;
    padding: 0 40px !important;
    background: rgba(255,182,193,0.02) !important;
}

.tab-nav button {
    background: transparent !important;
    color: #6a4050 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    font-size: 0.65em !important;
    letter-spacing: 5px !important;
    text-transform: uppercase !important;
    padding: 18px 30px !important;
    font-weight: 400 !important;
    transition: all 0.4s ease !important;
}

.tab-nav button.selected {
    color: #FFB6C1 !important;
    border-bottom: 1px solid #FFD700 !important;
    background: transparent !important;
}

.tab-nav button:hover { color: #FFB6C1 !important; }

.chatbot {
    background: rgba(255,182,193,0.03) !important;
    border: 1px solid rgba(255,182,193,0.15) !important;
    border-radius: 4px !important;
    animation: pulse-glow 4s ease-in-out infinite !important;
}

textarea, input[type="text"] {
    background: rgba(255,182,193,0.05) !important;
    border: 1px solid rgba(255,182,193,0.2) !important;
    border-radius: 4px !important;
    color: #FFD9E4 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.85em !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}

textarea:focus, input[type="text"]:focus {
    border-color: rgba(255,215,0,0.4) !important;
    background: rgba(255,182,193,0.08) !important;
    box-shadow: 0 0 20px rgba(255,182,193,0.1) !important;
}

textarea::placeholder { color: #6a4050 !important; }

button.primary {
    background: linear-gradient(135deg, rgba(255,182,193,0.15), rgba(255,215,0,0.1)) !important;
    border: 1px solid rgba(255,182,193,0.4) !important;
    color: #FFD9E4 !important;
    border-radius: 4px !important;
    font-size: 0.62em !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    padding: 14px 25px !important;
    font-weight: 400 !important;
    transition: all 0.4s ease !important;
    font-family: 'Montserrat', sans-serif !important;
}

button.primary:hover {
    background: linear-gradient(135deg, rgba(255,182,193,0.3), rgba(255,215,0,0.2)) !important;
    border-color: #FFD700 !important;
    box-shadow: 0 0 20px rgba(255,182,193,0.2) !important;
    transform: translateY(-1px) !important;
}

button.secondary {
    background: transparent !important;
    border: 1px solid rgba(255,182,193,0.1) !important;
    color: #4a2535 !important;
    border-radius: 4px !important;
    font-size: 0.58em !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-family: 'Montserrat', sans-serif !important;
    transition: all 0.3s ease !important;
}

button.secondary:hover {
    border-color: rgba(255,182,193,0.3) !important;
    color: #FFB6C1 !important;
}

label {
    color: #6a4050 !important;
    font-size: 0.6em !important;
    letter-spacing: 4px !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
}

[data-testid="image"] {
    background: rgba(255,182,193,0.04) !important;
    border: 1px dashed rgba(255,182,193,0.25) !important;
    border-radius: 4px !important;
    max-height: 180px !important;
}

.tab-description {
    text-align: center;
    color: #6a4050;
    font-size: 0.62em;
    letter-spacing: 4px;
    text-transform: uppercase;
    padding: 25px;
    font-weight: 300;
}

.examples-table button {
    background: rgba(255,182,193,0.05) !important;
    border: 1px solid rgba(255,182,193,0.15) !important;
    color: #C9A0B0 !important;
    border-radius: 20px !important;
    font-size: 0.7em !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}

.examples-table button:hover {
    background: rgba(255,182,193,0.15) !important;
    border-color: #FFB6C1 !important;
    color: #FFD9E4 !important;
}

.footer-text {
    text-align: center;
    color: #3a1525;
    font-size: 0.58em;
    padding: 35px;
    letter-spacing: 4px;
    text-transform: uppercase;
    border-top: 1px solid rgba(255,182,193,0.08);
    margin-top: 20px;
    font-family: 'Montserrat', sans-serif;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d0508; }
::-webkit-scrollbar-thumb { background: rgba(255,182,193,0.2); border-radius: 2px; }
"""

# ── UI ──────────────────────────────────────────────────────────────────────────

with gr.Blocks() as demo:

    gr.HTML("""
    <div class="floating-decor lipstick-1">💄</div>
    <div class="floating-decor lipstick-2">💄</div>
    <div class="floating-decor lipstick-3">💋</div>
    <div class="floating-decor sparkle-1">✨</div>
    <div class="floating-decor sparkle-2">⭐</div>
    <div class="floating-decor sparkle-3">✨</div>
    <div class="floating-decor flower-1">🌸</div>
    <div class="floating-decor flower-2">🌷</div>
    """)

    gr.HTML("""
    <div class="main-header">
        <h1 class="glow-title">GlowAI</h1>
        <div class="divider"></div>
        <p class="glow-subtitle">✦ Personal AI Beauty Agent ✦</p>
        <p class="glow-tagline">Because your skin deserves intelligent care ✨</p>
        <div class="divider"></div>
        <p class="glow-powered">Powered by Google ADK · Gemini 2.5 Flash · L'Oréal Group · Built by Aiza Fatima</p>
    </div>
    """)

    with gr.Tabs():

        with gr.Tab("🧴 Skincare"):
            gr.HTML("<p class='tab-description'>✦ Skin Analysis · Ingredient Intelligence · Personalized Routines ✦</p>")
            skincare_chatbot = gr.Chatbot(label="", height=420, show_label=False)
            with gr.Row():
                skincare_msg = gr.Textbox(
                    placeholder="✦ Ask GlowAI about your skin, ingredients, or routine...",
                    label="", scale=4, show_label=False
                )
                skincare_send = gr.Button("✦ Consult GlowAI", variant="primary", scale=1)
            skincare_image = gr.Image(label="Upload Skin Photo ✦", type="filepath")
            gr.Examples(
                examples=[
                    ["I have oily skin with acne and dark spots, help me!"],
                    ["Is niacinamide safe to use with vitamin C?"],
                    ["Build me an affordable morning routine for sensitive skin"],
                    ["Suggest L'Oréal skincare products for dry skin"],
                ],
                inputs=skincare_msg,
                label="✦ Suggested Consultations"
            )
            skincare_clear = gr.Button("✦ Clear Conversation", variant="secondary")

        with gr.Tab("💄 Makeup"):
            gr.HTML("<p class='tab-description'>✦ Face Analysis · Makeup Looks · L'Oréal Group Products ✦</p>")
            makeup_chatbot = gr.Chatbot(label="", height=420, show_label=False)
            with gr.Row():
                makeup_msg = gr.Textbox(
                    placeholder="✦ Ask GlowAI about makeup looks and L'Oréal products...",
                    label="", scale=4, show_label=False
                )
                makeup_send = gr.Button("✦ Consult GlowAI", variant="primary", scale=1)
            makeup_image = gr.Image(label="Upload Face Photo ✦", type="filepath")
            gr.Examples(
                examples=[
                    ["What makeup look suits me for a job interview?"],
                    ["Suggest a L'Oréal evening glam look"],
                    ["What L'Oréal foundation matches medium skin tone?"],
                    ["Give me a no-makeup makeup look with Maybelline products"],
                ],
                inputs=makeup_msg,
                label="✦ Suggested Consultations"
            )
            makeup_clear = gr.Button("✦ Clear Conversation", variant="secondary")

    gr.HTML("""
    <div class="footer-text">
        ✦ GlowAI · Built by Aiza Fatima · L'Oréal Brandstorm 2026 · Google × Kaggle Agentic AI Intensive 2026 ✦
    </div>
    """)

    skincare_send.click(skincare_chat, inputs=[skincare_msg, skincare_image, skincare_chatbot], outputs=[skincare_msg, skincare_image, skincare_chatbot])
    skincare_msg.submit(skincare_chat, inputs=[skincare_msg, skincare_image, skincare_chatbot], outputs=[skincare_msg, skincare_image, skincare_chatbot])
    skincare_clear.click(lambda: [], outputs=[skincare_chatbot])

    makeup_send.click(makeup_chat, inputs=[makeup_msg, makeup_image, makeup_chatbot], outputs=[makeup_msg, makeup_image, makeup_chatbot])
    makeup_msg.submit(makeup_chat, inputs=[makeup_msg, makeup_image, makeup_chatbot], outputs=[makeup_msg, makeup_image, makeup_chatbot])
    makeup_clear.click(lambda: [], outputs=[makeup_chatbot])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), css=css)
