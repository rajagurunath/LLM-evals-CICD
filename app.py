import streamlit as st
import os
import requests
import json
# import subprocess # No longer needed
import time
import datetime
from dotenv import load_dotenv
# import threading # No longer needed
# import pyautogui # No longer needed
# from PIL import Image # No longer needed
import re
# Define CSS styles
st.set_page_config(layout="wide")

css = """
<style>
.custom-container {
    border: 2px solid white;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 20px;
}
</style>
"""

# Inject CSS into the Streamlit app
st.markdown(css, unsafe_allow_html=True)

# --- Configuration ---
load_dotenv()  # Load environment variables from .env file

IO_NET_API_URL = "https://api.intelligence.io.solutions/api/v1/chat/completions"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

IO_NET_API_KEY = st.secrets["ionet"]["api_key"]
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

# --- Benchmark Prompts Definition ---
BENCHMARK_PROMPTS = {
    "Bouncing Balls (Heptagon)": """Create a single HTML file that displays an animation of 20 numbered balls bouncing inside a spinning heptagon using HTML, CSS, and JavaScript.

Requirements:
- **Single File:** All HTML structure, CSS styles, and JavaScript logic must be contained within a single `.html` file. Do not use external files.
- **Canvas/SVG:** Use HTML Canvas or SVG for the animation.
- **20 Balls:** Display exactly 20 balls.
- **Same Radius:** All balls must have the same radius.
- **Numbered Balls:** Each ball should display a unique number from 1 to 20.
- **Initial State:** All balls should start at the center of the heptagon and fall downwards.
- **Colors:** Use the following distinct colors for the balls (assign one color per ball, cycle if necessary): #f8b862, #f6ad49, #f39800, #f08300, #ec6d51, #ee7948, #ed6d3d, #ec6800, #ec6800, #ee7800, #eb6238, #ea5506, #ea5506, #eb6101, #e49e61, #e45e32, #e17b34, #dd7a56, #db8449, #d66a35
- **Physics:** Implement basic physics:
    - **Gravity:** Balls should accelerate downwards.
    - **Bouncing:** Balls must bounce realistically off the heptagon walls. Implement collision detection between balls and walls.
    - **Ball Collisions:** Implement basic collision detection and response between balls.
    - **Elasticity:** Bouncing should appear somewhat elastic (balls shouldn't stop dead on impact).
- **Spinning Heptagon:**
    - Draw a regular heptagon (7 equal sides).
    - The heptagon must spin continuously around its center at a rate of approximately 360 degrees every 5 seconds.
    - The heptagon should be large enough to comfortably contain the bouncing balls.
- **Ball Rotation (Visual):** The numbers on the balls should visually rotate as the balls move and collide to indicate spin (this can be a visual effect, full physics simulation of rotational friction is optional but preferred).
- **No External Libraries:** Do not use external JavaScript physics libraries (like Matter.js, Box2D) or animation libraries (like GSAP). Implement the logic using plain JavaScript and the Canvas/SVG API.
- **Output:** Provide only the complete HTML code. Start with `<!DOCTYPE html>` and end with `</html>`.
""",
    "Mandelbrot Set (Li Bai Poem)": """Please complete the programming competition, the content of the competition is as follows:
Please use html, css, javascript, to create an animation. The requirements are as follows:
- Use canvas to draw animation
- Please use full screen to display animation
- All codes need to be placed in the same HTML file
- The animation content is the ASCII style Mandelbrot Set. The initial size of the main graphic of the Mandelbrot Set is 50% of the screen. Each frame is enlarged by 0.5% each time it is rendered. A total of 200 renderings are performed. After 200 renderings, the animation loop rendering is reset.
- The candidate characters of the Mandelbrot set use Li Bai's poem "Quiet Night Thoughts" (床前明月光，疑是地上霜。举头望明月，低头思故乡。)
- The poems need to be deduplicated and retain the original character order, and do not contain punctuation marks, and can be reused. The final character set should be: 床前明月光疑是地上霜举头望低思故乡
- Leave the Main cardioid and period bulbs section of the Mandelbrot Set empty (render with a space or transparently).
- The center of the animation should always be the junction of the main cardioid and period bulbs (approximately c = -0.75 + 0i).
- Animation font size 8px, font rendering arrangement is also 8px, no spacing.
- Mandelbrot Set character color candidate set (from light to dark): #eaf4fc, #eaedf7, #e8ecef, #ebf6f7, #bbc8e6, #bbbcde, #8491c3, #867ba9, #68699b, #706caa, #5654a2, #4d4398, #4a488e, #274a78, #2a4073, #223a70, #192f60, #1c305c, #17184b, #0f2350
- The characters start with the darkest color at the outermost edge of the mandelbrot set and then get lighter towards the empty center. Assign colors based on the iteration count before escape.
- In the upper left corner there is an indicator showing the current FPS (FPS), an indicator showing the average FPS (AVG FPS), and an indicator showing the current rendering frame number (CURRENT FRAME: n/200). The average frame rate is calculated and updated after 200 frames are rendered. The font is black and the background uses semi-transparent white rounded corners.
- Please carefully restore each of the above requirements. The degree of restoration of each requirement will be used as a scoring point.
- At the same time, try to optimize rendering performance and increase FPS. The average FPS is 30.
- The operating environment uses the Chrome browser. The CPU is an 8-core CPU, so the maximum number of available threads is 8 (Note: Web workers can be used for optimization if desired, but the core logic should be within the single HTML file).
- **Output:** Provide only the complete HTML code. Start with `<!DOCTYPE html>` and end with `</html>`.
""",
    "Mars Mission (3D Plot)": """Generate code for an animated 3D plot visualizing a spacecraft mission trajectory.

Requirements:
- **Single HTML File:** All necessary HTML, CSS, and JavaScript must be contained within a single `.html` file.
- **3D Visualization:** Use a JavaScript library suitable for 3D plotting that can be included directly or implemented without external file dependencies (e.g., basic WebGL, or potentially a small library like `three.js` if the model can embed its core logic, though plain JS/WebGL is preferred if feasible for the model). If using a library like three.js, prioritize embedding its necessary components or linking via CDN if embedding is not feasible for the LLM.
- **Scenario:**
    1. Show simplified spherical representations of Earth and Mars in orbit around a central point representing the Sun. Use approximate relative sizes and orbital radii (doesn't need to be perfectly to scale, but Mars should be smaller and farther out than Earth).
    2. Animate the planets moving in roughly circular orbits around the Sun. Mars should move slower than Earth.
    3. Show a spacecraft launching from Earth.
    4. Animate the spacecraft following a transfer orbit (e.g., a Hohmann transfer ellipse or similar approximation) to Mars.
    5. Show the spacecraft arriving at Mars (e.g., entering orbit or landing).
    6. Pause briefly at Mars.
    7. Wait for the next optimal launch window (represent this by having Earth and Mars orbit further until they reach a suitable relative position for the return journey).
    8. Show the spacecraft launching from Mars.
    9. Animate the spacecraft following a transfer orbit back to Earth.
    10. Show the spacecraft arriving back at Earth.
    11. The entire sequence should loop or reset after completion.
- **Visuals:**
    - Use distinct colors for Earth, Mars, the Sun, and the spacecraft trajectory.
    - Add labels for the celestial bodies.
    - Optionally, add simple representations of planetary orbits (e.g., faint circles or ellipses).
- **No External Data Files:** The code should generate the animation without needing to load external data files.
- **Output:** Provide only the complete HTML code. Start with `<!DOCTYPE html>` and end with `</html>`.
""",
     "Snake Pit": """You are controlling a snake in a multi-apple game of Snake. The board size is 100x100. The standard X,Y coordinate system is used. The coordinates range from (0,0) in the lower left corner to (99,99) in the upper right corner.
10 apples will appear on the board. After each apple is eaten, a new apple will be generated on the board.
The coordinates evaluated so far are: (9, 6), (0, 2), (5, 9), (1, 7), (9, 7)
Your snake ID: 1 Current position: (5, 1)
Enemy Snake Position:
* Snake #2 is at (7, 1), and its body is []
Board Status:
9 . . . . . A . . . .
8 . . . . . . . . . .
7 . A . . . . . . . A
6 . . . . . . . . . A
5 . . . . . . . . . .
4 . . . . . . . . . .
3 . . . . . . . . . .
2 A . . . . . . . . .
1 . . . . . 1 . 2 . .
0 . . . . . . . . . .
  0 1 2 3 4 5 6 7 8 9
--Your last move information:--
Direction: Left
Reasoning: I noticed that our snake head (6,1) is closest to the apple at (0,2) (Manhattan distance is 7 steps), and is far away from the enemy snake at (7,0). Our immediate options are:
• Up → Move to (6,2)
• Right → Move to (7,1) (Closer to the enemy snake's territory)
• Left → Move to (5,1)
• Down → Move to (6,0)
Moving right or down would bring us closer to the enemy snake at (7,0), and possibly beyond the safe margin. Moving up would work, but moving left would start to lead us toward (0,2). Therefore, I decide to move left.
Strategy for future turns: I will continue to move left, then maneuver upward to reach the apple at (0,2), while keeping an eye on possible enemy moves.
I decided on my next move: left.
--End of previous step movement information--
rule:
1) If you move to the apple, you will become longer and get 1 point.

2) If you hit a wall (outside the listed coordinates), another snake, or yourself (e.g. walking backwards), you will die.
3) The goal is to get the highest score at the end of the game.
Decreasing the x coordinate moves to the left, and increasing the x coordinate moves to the right.
Decreasing the y coordinate moves downward, and increasing the y coordinate moves upward.
You can think first and then answer the direction.
You can also explain how you want to tell yourself the strategy for the next round.
Finish your answer with the next move you decide: UP, DOWN, LEFT, or RIGHT.
""",
    "Solar System Animation": """Create an HTML5 Canvas solar system animation that meets the following specifications:
0. **Requirements**
- All code should be in one HTML file
- Use canvas to draw animation
- Display animation in full screen
1. **Celestial Body Requirements**
- Includes: Sun, 9 planets
- Since the sun is too big, all the planets only need to show their relative sizes, for example, the sun is the largest, followed by Jupiter
- The planets are arranged in order of distance from the sun. From the inside to the outside, they are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto.
- Note that the orbital spacing of each planet should be larger than the diameter of the planet itself to avoid visual overlap
2. Visual Design
- Each planet uses 4 colors to fill pixels, and only fills once
  • Sun: #f2831f, #f15d22, #d94125, #a41d22
  • Mercury: #5a5856, #bfbdbc, #8c8a89, #f4f6f8
  • Venus: #868a8d, #d9b392, #f3dbc3, #414141
  • Earth: #1f386f, #0b1725, #386f61, #dac0a5
  • Mars: #dabd9e, #8c5d4b, #f27c5f, #c36d5c
  • Jupiter: #282411, #c08137, #bfb09c, #a6705b
  • Saturn: #f3cf89, #dab778, #736b59, #c1a480
  • Uranus: #3f575a, #688a8c, #95bbbe, #cfecf0
  • Neptune: #647ba5, #7595bf, #4e5d73, #789ebf
  • Pluto: #d8cbbb, #f4ebdc, #402a16, #a79f97
- Track line: semi-transparent white circle
- Label:
  • Planet text labels that always face the camera
  • Format: [planet name]
3. **Motion Simulation**
- Time compression: 1 second of real time = 10 Earth days, and the Earth orbits the sun once every 365 Earth days
- The planetary orbit can be a circular orbit
- Hierarchy:
  • All planets orbit the sun
4. **Technical Implementation**
- Use requestAnimationFrame to achieve smooth animation
5. **Performance Optimization**
- Offscreen canvas for static elements (track lines)
- Use Web Workers for position calculation (Note: Model should attempt to include worker logic within the single HTML file, perhaps in a separate script block or as a string blob URL, if possible).
6. **Counter**
- Displays the current FPS indicator (FPS) and the average FPS indicator (AVG FPS) in the upper left corner, as well as the current Earth Day count (Earth Day)
- Use black text and a semi-transparent white background with rounded corners
Note, do not omit the code for the planet visual design, I need you to implement all the code.
- **Output:** Provide only the complete HTML code. Start with `<!DOCTYPE html>` and end with `</html>`.
"""
}

# Qwen/QwQ-32B
# qwen/qwq-32b:free

# meta-llama/Llama-3.2-90B-Vision-Instruct
# meta-llama/llama-3.2-90b-vision-instruct

# deepseek-ai/DeepSeek-R1
# deepseek/deepseek-r1:free

# deepseek-ai/DeepSeek-R1-Distill-Llama-70B
# deepseek/deepseek-r1-distill-llama-70b:free

# deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
# deepseek/deepseek-r1-distill-qwen-32b:free

# meta-llama/Llama-3.3-70B-Instruct
# meta-llama/llama-3.1-70b-instruct

# google/gemma-3-27b-it:free

# --- Available Models ---
MODELS_TO_COMPARE = {
    "llama-3-70b": {
        "ionet": "meta-llama/Llama-3.3-70B-Instruct",
        "openrouter": "meta-llama/llama-3.3-70b-instruct:free"
    },
     "deepseek-r1": {
        "ionet": "deepseek-ai/DeepSeek-R1",
        "openrouter": "deepseek/deepseek-r1:free"
    },
    "Llama-3.2-90B-Vision-Instruct":{
        "ionet": "meta-llama/Llama-3.2-90B-Vision-Instruct",
        "openrouter": "meta-llama/llama-3.2-90b-vision-instruct:free"
    },
    "DeepSeek-R1-Distill-Llama:70B": {
        "ionet": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "openrouter": "deepseek/deepseek-r1-distill-llama-70b:free"
    },
    "DeepSeek-R1-Distill-Qwen-32B": {   
        "ionet": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",    
        "openrouter": "deepseek/deepseek-r1-distill-qwen-32b:free"
    },        
    "gemma-3-27b-it":{
        "ionet": "google/gemma-3-27b-it",
        "openrouter": "google/gemma-3-27b-it:free"
    }
    # Add more models here
}

OUTPUT_DIR = "streamlit_outputs"
RESULTS_DIR = "scoring_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# --- Scoring Criteria Definitions ---

BOUNCING_BALLS_SCORING_CRITERIA = [
    {"id": "bb_1", "text": "Single File Output: All HTML, CSS, and JS are contained within the single generated HTML file.", "points": [5, 0]},
    {"id": "bb_2", "text": "No External JS Libraries: Uses only plain JS and Canvas/SVG API, without external libraries (e.g., jQuery, Matter.js, GSAP).", "points": [5, 0]},
    {"id": "bb_3", "text": "Shows 20 Balls: Exactly 20 distinct ball elements are rendered.", "points": [5, 0]},
    {"id": "bb_4", "text": "Uniform Ball Size: All rendered balls appear to have the same radius.", "points": [5, 0]},
    {"id": "bb_5", "text": "Correct Ball Numbering: Numbers 1-20 are clearly displayed on the balls without duplication.", "points": [5, 3, 0]},
    {"id": "bb_6", "text": "Initial Position & Fall: Balls initially appear at the heptagon's center and start moving downwards.", "points": [5, 0]},
    {"id": "bb_7", "text": "Correct Ball Colors: Uses the specified distinct colors for the balls.", "points": [5, 3, 0]},
    {"id": "bb_8", "text": "Wall Collision: Balls visibly bounce off the heptagon walls.", "points": [5, 0]},
    {"id": "bb_9", "text": "Ball-Ball Collision: Balls visibly bounce off each other.", "points": [5, 0]},
    {"id": "bb_10", "text": "Gravity Effect: Balls consistently accelerate downwards realistically.", "points": [5, 3, 0]},
    {"id": "bb_11", "text": "Elasticity: Bounces appear reasonably elastic (balls don't stop dead or pass through walls/balls).", "points": [5, 3, 0]},
    {"id": "bb_12", "text": "Visual Ball Rotation: Numbers on balls visually rotate as balls move/collide.", "points": [5, 3, 0]},
    {"id": "bb_13", "text": "No Overlap: After the initial drop, balls do not significantly overlap during collisions or rest.", "points": [5, 0]},
    {"id": "bb_14", "text": "Containment: Balls remain contained within the boundaries of the spinning heptagon.", "points": [5, 0]},
    {"id": "bb_15", "text": "Rendering Quality: Balls are smooth circles, numbers are clear and centered.", "points": [5, 3, 0]},
    {"id": "bb_16", "text": "Heptagon Shape & Size: A regular heptagon (7 equal sides) is clearly drawn and appropriately sized for the balls.", "points": [5, 3, 0]},
    {"id": "bb_17", "text": "Heptagon Rotation: Heptagon spins smoothly around its center at approximately the correct speed (360deg/5s).", "points": [5, 3, 0]},
    {"id": "bb_18", "text": "Animation Fluency: Overall animation is smooth and runs without significant lag or stuttering.", "points": [5, 3, 0]},
] # Total 90

MANDELBROT_SCORING_CRITERIA = [
    {"id": "mb_1", "text": "Use canvas to draw animation", "points": [5, 0]},
    {"id": "mb_2", "text": "Full screen animation", "points": [5, 0]},
    {"id": "mb_3", "text": "All codes are placed in the same HTML file", "points": [5, 0]},
    {"id": "mb_4", "text": "Correctness/Beauty of Mandelbrot graphic (1pt each: aspect ratio, main cardioid, p-2 bulb, p-3 bulb, p-4 bulb visible)", "points": [5, 4, 3, 2, 1, 0]},
    {"id": "mb_5", "text": "Initial size of main figure (~50% screen) (5=~50%/p4 vis, 4=large/p3 vis, 3=large/p2 vis, 2=large/partial p2 vis, 1=partial cardioid)", "points": [5, 4, 3, 2, 1, 0]},
    {"id": "mb_6", "text": "Enlarged by 0.5% each render (5=yes, 3=enlarges but not 0.5%)", "points": [5, 3, 0]},
    {"id": "mb_7", "text": "200 total renderings", "points": [5, 0]},
    {"id": "mb_8", "text": "Reset and loop after 200 renderings (5=both, 3=reset OR loop only)", "points": [5, 3, 0]},
    {"id": "mb_9", "text": "Li Bai's poem text correct (5=correct, 3=incomplete, 1=title only)", "points": [5, 3, 1, 0]},
    {"id": "mb_10", "text": "Processing of Li Bai's poem (5=all: dedupe, order, no punct, reuse; -1pt per missing)", "points": [5, 4, 3, 2, 1, 0]},
    {"id": "mb_11", "text": "Main cardioid and period bulbs left blank (5=all blank, 3=partially blank)", "points": [5, 3, 0]},
    {"id": "mb_12", "text": "Center of animation at junction of main cardioid and period bulbs", "points": [5, 0]},
    {"id": "mb_13", "text": "Font size 8px, rendering arrangement 8px, no spacing (5=all 3, 3=2 items, 2=1 item)", "points": [5, 3, 2, 0]},
    {"id": "mb_14", "text": "Character colors: dark->light from outer edge (5=correct order/all used, 3=wrong order OR not all used)", "points": [5, 3, 0]},
    {"id": "mb_15", "text": "Upper left indicator calculations/display correct (FPS, AVG FPS, FRAME) (5=calc+display ok, 3=calc ok/display wrong)", "points": [5, 3, 0]},
    {"id": "mb_16", "text": "Indicator Style (black text, semi-transparent white bg, rounded) (5=all styles met, 3=style incorrect)", "points": [5, 3, 0]},
    {"id": "mb_17", "text": "Average FPS level (Max 30pts). Enter final score: Score = ROUNDUP(AVG_FPS) if AVG_FPS < 30, else 30. Deductions: -25 if outermost not text; -10 if graphic too large (p2 visible); -15 if graphic too large (p2 not visible)", "points": [30], "input_type": "number"}, # Max 30 points
] # Total 110


SOLAR_SYSTEM_SCORING_CRITERIA = [
    {"id": "ss_1", "text": "Use canvas to draw animation", "points": [5, 0]},
    {"id": "ss_2", "text": "Full screen animation (5=perfect, 3=partially exceeds)", "points": [5, 3, 0]},
    {"id": "ss_3", "text": "All codes are placed in the same HTML file", "points": [5, 0]},
    {"id": "ss_4", "text": "Sun size and display (5=correct size/pos, 3=wrong size/pos, 0=not shown)", "points": [5, 3, 0]},
    {"id": "ss_5", "text": "Nine planets displayed (5=all, 3=incomplete, 0=none)", "points": [5, 3, 0]},
    {"id": "ss_6", "text": "The sizes of the nine planets (5=ratio true, 3=partially wrong, 0=completely wrong)", "points": [5, 3, 0]},
    {"id": "ss_7", "text": "The nine planets are arranged correctly (by distance)", "points": [5, 0]},
    {"id": "ss_8", "text": "Nine planets revolving around the sun (5=all, 3=incomplete, 0=none)", "points": [5, 3, 0]},
    {"id": "ss_9", "text": "Nine planetary motion tracks (5=all correct, 3=incomplete/partially wrong)", "points": [5, 3, 0]},
    {"id": "ss_10", "text": "The orbits of the nine planets do not overlap (5=no overlap, 3=partial, 0=mess)", "points": [5, 3, 0]},
    {"id": "ss_11", "text": "Color rendering of the nine planets (5=all colors used, 3=some used)", "points": [5, 3, 0]},
    {"id": "ss_12", "text": "Color rendering aesthetics of the nine planets (5=concentric/random, 3=simple arrangement)", "points": [5, 3, 0]},
    {"id": "ss_13", "text": "Nine planet name labels (5=all correct/clear, 4=part blocked/unclear, 3=part displayed/wrong)", "points": [5, 4, 3, 0]},
    {"id": "ss_14", "text": "Earth Movement Time (1 cycle ≈ 36.5s) (5=dev<10%, 3=dev<50%)", "points": [5, 3, 0]},
    {"id": "ss_15", "text": "Other planetary motion times (relative to Earth) (5=avg dev<10%, 3=avg dev<50%, 2=part dev<50%)", "points": [5, 3, 2, 0]},
    {"id": "ss_16", "text": "Indicator calculations are correct (FPS, AVG FPS, Earth Day)", "points": [5, 0]},
    {"id": "ss_17", "text": "Correct indicator style (black text, semi-transparent white bg, rounded)", "points": [5, 3, 0]},
    {"id": "ss_18", "text": "Animation Fluency (5=smooth, 3=too fast/slow)", "points": [5, 3, 0]},
] # Total 90

MARS_MISSION_SCORING_CRITERIA = [
    {"id": "mm_1", "text": "Show the sun", "points": [5, 0]},
    {"id": "mm_2", "text": "Show Earth, Mars, and a spacecraft", "points": [5, 0]},
    {"id": "mm_3", "text": "Show the Earth and Mars revolving around the Sun (5=both shown, 3=incomplete)", "points": [5, 3, 0]},
    {"id": "mm_4", "text": "Display the trajectory of the Earth, Mars, and the spacecraft (5=all displayed, 3=incomplete)", "points": [5, 3, 0]},
    {"id": "mm_5", "text": "Spacecraft launched from Earth, lands on Mars (elliptical orbit) (5=full, 3=incomplete, 0=error)", "points": [5, 3, 0]},
    {"id": "mm_6", "text": "Spacecraft returns from Mars, lands on Earth (elliptical orbit) (5=full, 3=incomplete, 0=error)", "points": [5, 3, 0]},
    {"id": "mm_7", "text": "Orbital ratio (Earth ≈ 1AU, Mars ≈ 1.5AU) (5=exact pos, 3=relative size/ratio ok)", "points": [5, 3, 0]},
    {"id": "mm_8", "text": "Launch period (≈ 259 days) (5=dev<10%, 3=dev<50%)", "points": [5, 3, 0]},
    {"id": "mm_9", "text": "Return Window (wait ≈ 450 days after launch) (5=dev<10%, 3=dev<50%)", "points": [5, 3, 0]},
    {"id": "mm_10", "text": "Three-dimensional spatial representation (change in track inclination/Z-axis)", "points": [5, 0]},
    {"id": "mm_11", "text": "Scale (5=AU scale shown, 3=scale only shown)", "points": [5, 3, 0]},
    {"id": "mm_12", "text": "Legend (Earth, Mars, Spacecraft, Sun) (5=all included, 3=incomplete)", "points": [5, 3, 0]},
    {"id": "mm_13", "text": "Animation Fluency (5=smooth, 3=too fast/slow)", "points": [5, 3, 0]},
] # Total 65

# --- Master Dictionary for Scoring Criteria ---
BENCHMARK_SCORING_CRITERIA = {
    "Bouncing Balls (Heptagon)": BOUNCING_BALLS_SCORING_CRITERIA,
    "Mandelbrot Set (Li Bai Poem)": MANDELBROT_SCORING_CRITERIA, # Added!
    "Mars Mission (3D Plot)": MARS_MISSION_SCORING_CRITERIA,
    "Snake Pit": None, # NO valid scoring provided
    "Solar System Animation": SOLAR_SYSTEM_SCORING_CRITERIA,
}


# --- Helper Functions ---

def extract_html_code(response_text: str) -> str | None:
    """
    Extracts HTML code blocks from a Markdown string or the entire string if it looks like HTML.
    """
    if not response_text:
        return None
    response_text = response_text.strip()

    # 1. Try to find ```html blocks
    pattern_html = r"```(?:html)\s*\n(.*?)\n```"
    html_blocks = re.findall(pattern_html, response_text, re.DOTALL)
    if html_blocks:
        print("Extracted HTML using ```html block.")
        return html_blocks[0].strip()

    # 2. If no ```html block, check if the *entire* response looks like HTML
    if (response_text.lower().startswith("<!doctype html>") or response_text.lower().startswith("<html")) \
       and response_text.lower().endswith("</html>"):
         print("Extracted HTML based on start/end tags.")
         return response_text

    # 3. Fallback: No reliable HTML block found. Return None.
    print("Could not reliably extract HTML code block.")
    return None

def extract_code_or_text(response_text: str) -> tuple[str | None, str | None]:
    """
    Attempts to extract HTML code. If successful, returns (html_code, None).
    If unsuccessful, returns (None, original_text).
    Handles None input.
    """
    if not response_text:
        return None, None

    html_code = extract_html_code(response_text)
    if html_code:
        return html_code, None # Return HTML, no raw text needed
    else:
        # No HTML block found, return the original text assuming it's the intended output (e.g., for Snake Pit)
        print("Returning raw text as HTML extraction failed.")
        return None, response_text.strip()


def call_chat_completion(api_url, api_key, model_name, prompt, platform_name):
    """
    Calls a chat completion API. Returns a tuple: (extracted_html, raw_text).
    One of the elements will be None.
    """
    st.write(f"--- Calling {platform_name} API for model: {model_name} ---")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if platform_name.lower() == "openrouter":
        headers["HTTP-Referer"] = "http://localhost"
        headers["X-Title"] = "Streamlit Model Comparison"

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 4000,
    }

    try:
        # Increased timeout slightly for potentially complex generations
        response = requests.post(api_url, headers=headers, json=payload, timeout=360) # 6 min timeout
        response.raise_for_status()
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0].get("message", {}).get("content", "")
            st.write(f"--- Successfully received response from {platform_name} for {model_name} ---")
            # Use the new extraction function returning a tuple
            return extract_code_or_text(content)
        else:
            st.warning(f"Warning: No choices found in response from {platform_name} for {model_name}.")
            st.json(result)
            return None, None # Return None for both

    except requests.exceptions.Timeout:
         st.error(f"Error: Request timed out calling {platform_name} API for model {model_name} after 360 seconds.")
         return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling {platform_name} API for model {model_name}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                st.error(f"Response status code: {e.response.status_code}")
                st.error(f"Response text: {e.response.text}")
            except Exception as inner_e:
                 st.error(f"Could not parse error response details: {inner_e}")
        return None, None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response from {platform_name} for model {model_name}: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
             st.text(f"Raw response text (start): {response.text[:500]}...")
        return None, None


def save_results(data, filename):
    """Saves the scoring data to a JSON file."""
    filepath = os.path.join(RESULTS_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        st.success(f"Results saved successfully to: {filepath}")
    except IOError as e:
        st.error(f"Error saving results to {filepath}: {e}")

def calculate_total_points(criteria_list):
    """Calculates the maximum possible score from a criteria list."""
    if not criteria_list:
        return 0
    # Sum the first (maximum) point value for each criterion
    return sum(criterion["points"][0] for criterion in criteria_list if criterion.get("points"))


# --- Streamlit UI ---

col1, col2 = st.columns(2)
col1.image("https://io.net/_next/static/media/brandLogoLeft.29930dac.svg")
st.title("LLM Model Comparison - Coding capabilties using Kcores")
st.markdown("""


Most existing large model evaluations are multiple-choice questions, which makes it very easy to optimize the test, resulting in distorted results.

Therefore, this test focuses on real-world scenarios and uses manual scoring and benchmarking to evaluate the model, striving to restore the performance of the large model in the real world.

All prompts and benchmarks are taken from [Github Link](https://github.com/KCORES/kcores-llm-arena/tree/main)

!! This is streamlit app for all the scripts and evaluation of the models using browser friendly interface.
""")
# --- Sidebar for Benchmark Selection Only ---
st.sidebar.image("https://io.net/_next/static/media/brandLogoRight.fd489776.svg")

st.sidebar.title("Configuration")
st.sidebar.header("1. Select Benchmark")

benchmark_options = list(BENCHMARK_PROMPTS.keys())
selected_benchmark_key = st.sidebar.radio(
    "Choose a benchmark task:",
    benchmark_options,
    index=0, # Default to the first benchmark
    key="benchmark_select",
    # label_visibility="collapsed"
)

# Get the active prompt based on selection
active_prompt = BENCHMARK_PROMPTS[selected_benchmark_key]
active_scoring_criteria = BENCHMARK_SCORING_CRITERIA.get(selected_benchmark_key) # Get criteria or None
total_possible_points = calculate_total_points(active_scoring_criteria)

# --- Sidebar Instructions ---
st.sidebar.header("Instructions")
st.sidebar.info(f"""
1.  **Select Benchmark:** Choose task title above.
2.  **View Description:** See details in main panel.
3.  **Select Models:** Choose models in main panel.
4.  **Run Comparison:** Click '🚀 Run Comparison...'
5.  **Wait:** Allow time for API responses.
6.  **View Results:** Examine output (HTML/text) & code.
7.  **Score (If Applicable):** If scoring exists, fill form. Use number input for FPS score in Mandelbrot.
8.  **Submit Scores (If Applicable):** Save evaluation.

**Note:** API keys in `.env` or script. Needs `streamlit`, `requests`, `python-dotenv`.
""")


# --- Main Panel ---

# --- 1. Benchmark Description ---
st.header("1. Benchmark Description")
with st.expander(f"Show/Hide Description for '{selected_benchmark_key}'", expanded=True):
    st.markdown(active_prompt, unsafe_allow_html=True) # Use markdown

# --- 2. Model Selection ---
st.header("2. Select Models")
model_options = list(MODELS_TO_COMPARE.keys())

col1, col2 = st.columns(2)
with col1:
    selected_ionet_logical_name = st.selectbox(
        "Select io.net Model:",
        options=model_options,
        index=0,
        key="ionet_model_select"
    )
    ionet_model_id = MODELS_TO_COMPARE[selected_ionet_logical_name].get("ionet")
    if not ionet_model_id:
        st.warning(f"No io.net model ID defined for '{selected_ionet_logical_name}'. Cannot run.")
    else:
        st.caption(f"Using io.net ID: `{ionet_model_id}`")

with col2:
    selected_openrouter_logical_name = st.selectbox(
        "Select OpenRouter Model:",
        options=model_options,
        index=0,
        key="openrouter_model_select"
    )
    openrouter_model_id = MODELS_TO_COMPARE[selected_openrouter_logical_name].get("openrouter")
    if not openrouter_model_id:
        st.warning(f"No OpenRouter model ID defined for '{selected_openrouter_logical_name}'. Cannot run.")
    else:
        st.caption(f"Using OpenRouter ID: `{openrouter_model_id}`")

# --- 3. Run Button ---
st.header("3. Run")
run_button = st.button(f"🚀 Run Comparison for '{selected_benchmark_key}'", disabled=(not ionet_model_id or not openrouter_model_id))

# --- 4. Results Display Area ---
st.header("4. Results")
results_placeholder = st.empty() # Placeholder for results columns

# --- 5. Scoring Area ---
st.header("5. Scoring (K-Score)")
scoring_placeholder = st.empty() # Placeholder for scoring form

# --- Main Logic ---
if run_button:
    # Clear previous results relevant to display/scoring
    results_placeholder.empty()
    scoring_placeholder.empty()
    st.session_state.ionet_html = None
    st.session_state.openrouter_html = None
    st.session_state.ionet_text = None
    st.session_state.openrouter_text = None
    st.session_state.show_scoring = False # Reset scoring display flag

    # Sanitize benchmark key for filename
    safe_benchmark_key = re.sub(r'[^\w\-]+', '_', selected_benchmark_key).lower()

    ionet_html, ionet_text = None, None
    openrouter_html, openrouter_text = None, None

    with st.spinner(f"Running benchmark '{selected_benchmark_key}' on selected models..."):
        ionet_html, ionet_text = call_chat_completion(IO_NET_API_URL, IO_NET_API_KEY, ionet_model_id, active_prompt, "io.net")
        openrouter_html, openrouter_text = call_chat_completion(OPENROUTER_API_URL, OPENROUTER_API_KEY, openrouter_model_id, active_prompt, "OpenRouter")

    # Assign results to session state
    st.session_state.ionet_html = ionet_html
    st.session_state.openrouter_html = openrouter_html
    st.session_state.ionet_text = ionet_text
    st.session_state.openrouter_text = openrouter_text

    # Determine primary content and extension for saving
    ionet_output_content = ionet_html if ionet_html else ionet_text
    openrouter_output_content = openrouter_html if openrouter_html else openrouter_text
    ionet_ext = ".html" if ionet_html else ".txt"
    openrouter_ext = ".html" if openrouter_html else ".txt"

    # Save outputs
    if ionet_output_content:
        try:
            ionet_output_path = os.path.join(OUTPUT_DIR, f"output_ionet_{selected_ionet_logical_name.replace('/','_')}_{safe_benchmark_key}{ionet_ext}")
            with open(ionet_output_path, "w", encoding='utf-8') as f:
                f.write(ionet_output_content)
            st.write(f"Saved io.net output to: {ionet_output_path}")
        except IOError as e:
            st.error(f"Error saving io.net output file: {e}")
    else:
         st.warning(f"io.net ({selected_ionet_logical_name}) did not return valid content for this benchmark.")

    if openrouter_output_content:
        try:
            openrouter_output_path = os.path.join(OUTPUT_DIR, f"output_openrouter_{selected_openrouter_logical_name.replace('/','_')}_{safe_benchmark_key}{openrouter_ext}")
            with open(openrouter_output_path, "w", encoding='utf-8') as f:
                f.write(openrouter_output_content)
            st.write(f"Saved OpenRouter output to: {openrouter_output_path}")
        except IOError as e:
            st.error(f"Error saving OpenRouter output file: {e}")
    else:
        st.warning(f"OpenRouter ({selected_openrouter_logical_name}) did not return valid content for this benchmark.")

    # Decide whether to show scoring based on criteria existence
    if not ionet_output_content and not openrouter_output_content:
        st.error("Failed to retrieve valid content from both APIs for this benchmark. Cannot proceed.")
    else:
        # Use the active_scoring_criteria determined when the benchmark was selected
        if active_scoring_criteria:
            st.session_state.show_scoring = True
        else:
            st.session_state.show_scoring = False

    # Save context for display persistence
    st.session_state.last_run_ionet_name = selected_ionet_logical_name
    st.session_state.last_run_openrouter_name = selected_openrouter_logical_name
    st.session_state.last_run_benchmark_key = selected_benchmark_key

    st.rerun() # Rerun to update display sections


# --- Display Results ---
ionet_html_output = st.session_state.get('ionet_html')
openrouter_html_output = st.session_state.get('openrouter_html')
ionet_text_output = st.session_state.get('ionet_text')
openrouter_text_output = st.session_state.get('openrouter_text')

display_ionet_name = st.session_state.get('last_run_ionet_name', selected_ionet_logical_name)
display_openrouter_name = st.session_state.get('last_run_openrouter_name', selected_openrouter_logical_name)
display_benchmark_key = st.session_state.get('last_run_benchmark_key', selected_benchmark_key)

if ionet_html_output or openrouter_html_output or ionet_text_output or openrouter_text_output:
     with results_placeholder.container():
        st.subheader(f"Benchmark: {display_benchmark_key}")
        res_col1, res_col2 = st.columns(2)

        with res_col1: # io.net Column
            st.subheader(f"io.net ({display_ionet_name}) Output")
            if ionet_html_output:
                st.components.v1.html(ionet_html_output, height=600, scrolling=True)
                with st.expander("Show io.net HTML Code"):
                    st.code(ionet_html_output, language="html")
            elif ionet_text_output:
                st.text_area("io.net Text Output", ionet_text_output, height=600)
            else:
                 st.info("No valid output generated by io.net for the last run.")

        with res_col2: # OpenRouter Column
            st.subheader(f"OpenRouter ({display_openrouter_name}) Output")
            if openrouter_html_output:
                st.components.v1.html(openrouter_html_output, height=600, scrolling=True)
                with st.expander("Show OpenRouter HTML Code"):
                    st.code(openrouter_html_output, language="html")
            elif openrouter_text_output:
                 st.text_area("OpenRouter Text Output", openrouter_text_output, height=600)
            else:
                 st.info("No valid output generated by OpenRouter for the last run.")


# --- Display Scoring Form ---
if st.session_state.get('show_scoring', False):
    # Retrieve criteria and total points based on the *last run's* benchmark key
    # Use display_benchmark_key which reflects the last run
    scoring_criteria_to_display = BENCHMARK_SCORING_CRITERIA.get(display_benchmark_key)
    total_points_to_display = calculate_total_points(scoring_criteria_to_display)

    if scoring_criteria_to_display: # Ensure criteria exist for the benchmark displayed
        with scoring_placeholder.container():
            st.info(f"Evaluate the '{display_benchmark_key}' outputs based on the criteria below (Total Points: {total_points_to_display}).")
            # Use benchmark key in form key for uniqueness
            with st.form(key=f"scoring_form_{display_benchmark_key.replace(' ', '_')}"):
                scores = {"ionet": {}, "openrouter": {}}
                total_ionet_score = 0
                total_openrouter_score = 0

                # --- io.net Scoring ---
                st.subheader(f"io.net ({display_ionet_name}) Scoring")
                ionet_has_output = bool(ionet_html_output or ionet_text_output)
                for criterion in scoring_criteria_to_display:
                    criterion_id = criterion['id']
                    criterion_text = criterion['text']
                    criterion_points = criterion['points']
                    input_type = criterion.get('input_type', 'radio') # Default to radio

                    if input_type == 'number':
                        max_points = criterion_points[0]
                        # Use number input
                        score = st.number_input(
                            label=f"**{criterion_id}. {criterion_text}** (Enter 0-{max_points})",
                            min_value=0,
                            max_value=max_points,
                            value=0 if not ionet_has_output else 0, # Default to 0
                            step=1,
                            key=f"ionet_num_{criterion_id}"
                        )
                    else: # Default to radio buttons
                        options = [f"{p} points" for p in criterion_points]
                        default_index = len(options) - 1 if not ionet_has_output else 0
                        selected_option = st.radio(
                            f"**{criterion_id}. {criterion_text}**",
                            options=options,
                            key=f"ionet_radio_{criterion_id}",
                            horizontal=True,
                            index=default_index
                        )
                        score = int(selected_option.split()[0])

                    scores["ionet"][criterion_id] = score
                    total_ionet_score += score
                st.metric("Total io.net Score", f"{total_ionet_score} / {total_points_to_display}")

                st.divider()

                # --- OpenRouter Scoring ---
                st.subheader(f"OpenRouter ({display_openrouter_name}) Scoring")
                openrouter_has_output = bool(openrouter_html_output or openrouter_text_output)
                for criterion in scoring_criteria_to_display:
                    criterion_id = criterion['id']
                    criterion_text = criterion['text']
                    criterion_points = criterion['points']
                    input_type = criterion.get('input_type', 'radio')

                    if input_type == 'number':
                        max_points = criterion_points[0]
                        score = st.number_input(
                            label=f"**{criterion_id}. {criterion_text}** (Enter 0-{max_points})",
                            min_value=0,
                            max_value=max_points,
                            value=0 if not openrouter_has_output else 0, # Default to 0
                            step=1,
                            key=f"openrouter_num_{criterion_id}"
                        )
                    else:
                        options = [f"{p} points" for p in criterion_points]
                        default_index = len(options) - 1 if not openrouter_has_output else 0
                        selected_option = st.radio(
                            f"**{criterion_id}. {criterion_text}**",
                            options=options,
                            key=f"openrouter_radio_{criterion_id}",
                            horizontal=True,
                            index=default_index
                        )
                        score = int(selected_option.split()[0])

                    scores["openrouter"][criterion_id] = score
                    total_openrouter_score += score
                st.metric("Total OpenRouter Score", f"{total_openrouter_score} / {total_points_to_display}")

                # --- Submit Button ---
                submitted = st.form_submit_button(f"💾 Submit Scores for '{display_benchmark_key}'")
                if submitted:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    run_ionet_id = MODELS_TO_COMPARE[display_ionet_name].get("ionet")
                    run_openrouter_id = MODELS_TO_COMPARE[display_openrouter_name].get("openrouter")
                    safe_benchmark_key_for_save = re.sub(r'[^\w\-]+', '_', display_benchmark_key).lower()

                    result_data = {
                        "timestamp": timestamp,
                        "benchmark": display_benchmark_key,
                        "ionet_model_logical": display_ionet_name,
                        "ionet_model_id": run_ionet_id,
                        "openrouter_model_logical": display_openrouter_name,
                        "openrouter_model_id": run_openrouter_id,
                        "scoring_criteria_version": "1.1", # Increment version if criteria changed
                        "total_possible_points": total_points_to_display,
                        "scores": scores,
                        "total_scores": {
                            "ionet": total_ionet_score,
                            "openrouter": total_openrouter_score
                        },
                        "output_content": {
                            "ionet_html": ionet_html_output,
                            "ionet_text": ionet_text_output,
                            "openrouter_html": openrouter_html_output,
                            "openrouter_text": openrouter_text_output,
                        }
                    }
                    filename = f"scoring_{display_ionet_name.replace('/','_')}_vs_{display_openrouter_name.replace('/','_')}_{safe_benchmark_key_for_save}_{timestamp}.json"
                    save_results(result_data, filename)
                    st.balloons()
                    st.session_state.show_scoring = False # Hide form
                    scoring_placeholder.empty() # Clear placeholder
                    st.success("Scores submitted successfully!")
                    time.sleep(2)
                    st.rerun() # Rerun to reflect state change
    # else: # This case implies show_scoring was true but criteria became None (shouldn't happen with current logic)
        # with scoring_placeholder.container():
            # st.warning("Scoring criteria not found for the displayed benchmark results.")

# If not showing scoring form, display appropriate message
elif 'last_run_benchmark_key' in st.session_state: # Only show info if a run has happened
    with scoring_placeholder.container():
        # Check if scoring *should* exist for the last run benchmark
        if not BENCHMARK_SCORING_CRITERIA.get(display_benchmark_key):
             st.info(f"No specific scoring criteria defined for the '{display_benchmark_key}' benchmark.")
        # Else: Placeholder remains empty (form was successfully submitted or never shown)