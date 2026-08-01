import streamlit as st
import requests
from cartesia import Cartesia

st.set_page_config(page_title="Ultra-Max AI Voice Agent", page_icon="🎙️", layout="centered")

st.title("🎙️ Ultra-Max AI Voice Agent")
st.markdown("Generate hyper-realistic, human-quality voiceovers instantly using advanced AI.")

CARTESIA_API_KEY = "sk_car_yUAdKd8b9oyuwMme72oJSm"
GEMINI_API_KEY = "AQ.Ab8RN6LqfXesod6k0J0dXSSd0shit5ub99DsR9QzIUh6uqQ0OQ"

VOICE_PROFILES = {
    "Hyper-Realistic Professional Male": "79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e",
    "Expressive Cinematic Voice": "79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e",
    "Deep Storyteller Tone": "79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e"
}

selected_voice_name = st.selectbox("Select Voice Archetype:", list(VOICE_PROFILES.keys()))
voice_id = VOICE_PROFILES[selected_voice_name]

user_input = st.text_area("Enter your script or text prompt:", height=150, placeholder="Type your text or Hinglish script here...")

if st.button("🚀 Generate Voiceover"):
    if not user_input.strip():
        st.warning("Please enter some text or script first!")
    else:
        with st.spinner("🧠 AI is formatting your script..."):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {'Content-Type': 'application/json'}
            system_prompt = f"Rewrite this text into a deeply emotional, organic spoken script with natural pauses and breathing cues. Return ONLY the raw script text: {user_input}"
            data = {"contents": [{"parts": [{"text": system_prompt}]}]}
            
            final_script = user_input
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    final_script = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            except Exception:
                pass

        st.subheader("📝 Optimized Script:")
        st.write(final_script)

        with st.spinner("🎙️ Synthesizing audio via Cartesia Sonic..."):
            try:
                client = Cartesia(api_key=CARTESIA_API_KEY)
                output = client.tts.generate(
                    model_id="sonic-3",
                    transcript=final_script,
                    voice={"mode": "id", "id": voice_id},
                    output_format={"container": "mp3", "encoding": "mp3", "sample_rate": 44100},
                    language="en"
                )
                
                output_filename = "voiceover_output.mp3"
                output.write_to_file(output_filename)
                
                st.success("✅ Voice Generation Complete!")
                st.audio(output_filename, format="audio/mp3")
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="📥 Download Audio File (MP3)",
                        data=file,
                        file_name="ultramax_voiceover.mp3",
                        mime="audio/mpeg"
                    )
            except Exception as e:
                st.error(f"❌ Generation Error: {e}")
