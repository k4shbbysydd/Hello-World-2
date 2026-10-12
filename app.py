import html
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Hello World Motion Lab")
st.caption("A beginner-friendly app for experimenting with text, colors, and animation.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name or message", "Hello World", max_chars=80)

    font_family = st.selectbox(
        "Font type",
        [
            "Arial",
            "Courier New",
            "Georgia",
            "Times New Roman",
            "Verdana",
            "Trebuchet MS",
            "Impact",
            "Comic Sans MS",
        ],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=100, value=52, step=2)

    backgrounds = {
        "Light": ("#ffffff", "#171717"),
        "Dark": ("#101522", "#ffffff"),
        "Ocean": ("#dff6ff", "#073b4c"),
        "Sunset": ("#ffdfc1", "#6b2145"),
        "Forest": ("#173b2b", "#f0ffe8"),
        "Lavender": ("#eee7ff", "#35205f"),
        "Pink": ("#ffe3ef", "#78264d"),
        "Midnight gradient": ("linear-gradient(135deg, #101522, #31205b, #123c50)", "#ffffff"),
    }
    background = st.selectbox("Background", list(backgrounds.keys()))

    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])

    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5)
    particle_count = st.slider("Number of moving pieces", min_value=8, max_value=70, value=32, step=2)

bg_color, text_color = backgrounds[background]
safe_name = html.escape(name.strip() or "Your name here")
safe_font = font_family  # Comes from a fixed list of font choices.
duration = 11 - speed  # Smaller animation duration means faster motion.

effect_symbols = {
    "Rain": ["💧", "💦"],
    "Snow": ["❄️", "❅", "❆"],
    "Hail": ["🧊", "•"],
    "Wind gust": ["〰️", "💨", "🍃"],
    "Confetti": ["🎉", "✨", "🎊", "🟣", "🟡", "🟢"],
    "Tornado": ["🌪️", "〰️"],
}

particles = []
if effect != "None":
    for i in range(particle_count):
        left = random.randint(1, 98)
        delay = round(random.uniform(-duration, 0), 2)
        size = random.randint(12, 28)
        drift = random.randint(-120, 120)
        symbol = random.choice(effect_symbols[effect])
        particles.append(
            f'<span class="particle p{i}" style="left:{left}%;'
            f'animation-delay:{delay}s;animation-duration:{duration * random.uniform(0.75, 1.35):.2f}s;'
            f'font-size:{size}px;--drift:{drift}px;">{symbol}</span>'
        )
particles_html = "\n".join(particles)

if name_mode == "Ticker Tape":
    name_markup = (
        '<div class="marquee"><div class="marquee-track">'
        f'<span>{safe_name}&nbsp;&nbsp; ✨ &nbsp;&nbsp;</span>'
        f'<span aria-hidden="true">{safe_name}&nbsp;&nbsp; ✨ &nbsp;&nbsp;</span>'
        '</div></div>'
    )
elif name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f"<div>{safe_name}</div>" for _ in range(5)
    ) + "</div>"
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

# The animation runs entirely inside the embedded browser component.
# No time.sleep() or repeated st.rerun() is needed.
html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  .stage {{
    position: relative;
    height: 620px;
    width: 100%;
    overflow: hidden;
    border-radius: 18px;
    background: {bg_color};
    color: {text_color};
    font-family: "{safe_font}", sans-serif;
    isolation: isolate;
  }}
  .effects {{
    position: absolute;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 1;
  }}
  .particle {{
    position: absolute;
    top: -45px;
    display: block;
    opacity: .88;
    user-select: none;
    will-change: transform;
    animation-name: fall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
  }}
  @keyframes fall {{
    0% {{ transform: translate3d(0, -50px, 0) rotate(0deg); }}
    100% {{ transform: translate3d(var(--drift), 700px, 0) rotate(540deg); }}
  }}
  .center-name {{
    position: absolute;
    z-index: 3;
    top: 50%;
    left: 5%;
    width: 90%;
    transform: translateY(-50%);
    text-align: center;
    overflow-wrap: anywhere;
    font-size: {font_size}px;
    font-weight: 700;
    text-shadow: 0 2px 12px rgba(0,0,0,.12);
  }}
  .marquee {{
    position: absolute;
    z-index: 3;
    top: 50%;
    left: 0;
    width: 100%;
    overflow: hidden;
    transform: translateY(-50%);
    font-size: {font_size}px;
    font-weight: 700;
    white-space: nowrap;
  }}
  .marquee-track {{
    display: flex;
    width: max-content;
    animation: marquee 12s linear infinite;
  }}
  .marquee-track span {{ padding-right: .3em; }}
  @keyframes marquee {{
    from {{ transform: translateX(0); }}
    to {{ transform: translateX(-50%); }}
  }}
  .repeated {{
    position: absolute;
    z-index: 3;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 20px;
    font-size: {max(18, int(font_size * .72))}px;
    font-weight: 700;
    overflow-wrap: anywhere;
    text-align: center;
  }}
  .repeated div:nth-child(even) {{ opacity: .72; }}
  .hint {{
    position: absolute;
    z-index: 4;
    bottom: 14px;
    left: 0;
    width: 100%;
    text-align: center;
    font-size: 12px;
    opacity: .65;
    font-family: Arial, sans-serif;
  }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, .marquee-track {{ animation-duration: 30s !important; }}
  }}
</style>
</head>
<body>
  <main class="stage">
    <div class="effects" aria-hidden="true">{particles_html}</div>
    {name_markup}
    <div class="hint">Hello World Motion Lab · {html.escape(effect)} effect · Continuous loop</div>
  </main>
</body>
</html>
"""

components.html(html_doc, height=635, scrolling=False)

st.info(
    "Tip: Use the sidebar to change the text, font, size, background, display mode, "
    "and animation. The effects loop inside the preview, so the whole Streamlit page "
    "does not need to refresh repeatedly."
)
