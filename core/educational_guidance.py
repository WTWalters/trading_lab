# core/educational_guidance.py
"""
Core module for providing educational guidance using Google's Gemini API.
# ... (rest of docstring) ...
"""

import os
import logging
from dotenv import load_dotenv
# --- MOVE IMPORT HERE ---
try:
    import google.generativeai as genai
    GENAI_INSTALLED = True
except ImportError:
    genai = None # Define genai as None if not installed
    GENAI_INSTALLED = False
# ------------------------

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if API key exists (can check GENAI_INSTALLED as well)
if not GEMINI_API_KEY:
    logger.warning("Gemini API key is not configured in .env file")
if not GENAI_INSTALLED:
     logger.warning("google.generativeai library not installed. Educational features disabled.")


# Define prompt dictionary for different trading topics
EDUCATIONAL_PROMPTS = {
    'volume_confirmation': """
        Explain volume confirmation for breakouts in simple terms for a beginner swing trader
        focusing on the Classic Breakout strategy. Include why volume increases during breakouts,
        what the 1.5x average volume threshold signifies, and how it helps avoid false breakouts.
    """,

    'atr_stop': """
        Explain how an ATR-based stop loss works using ATR(14) * 2.0 for a beginner swing trader.
        Include what ATR measures, why it's useful for setting stops in the Classic Breakout strategy,
        and how the multiplier (2.0) affects the stop distance. Give a simple example.
    """,

    'chandelier_exit': """
        Explain the Chandelier Exit trailing stop technique for a beginner swing trader using the
        Classic Breakout strategy. Include how it's calculated using ATR(14) * 3.0 subtracted from
        the highest high since entry, why it's effective for letting profits run, and how it differs
        from a fixed stop loss.
    """,

    'consolidation': """
        Explain what a price consolidation pattern is in the context of the Classic Breakout strategy.
        Include how to identify consolidation, typical duration, why stocks consolidate, and why breakouts
        from consolidation are significant trading opportunities.
    """,

    'rr_ratio': """
        Explain the Risk:Reward ratio in trading for a beginner focusing on the Classic Breakout strategy.
        Include how it's calculated, why a minimum R:R of 2:1 is often recommended, and how it affects
        long-term profitability even with a lower win rate.
    """,

    'position_sizing': """
        Explain position sizing based on risk percentage for a beginner using the Classic Breakout strategy.
        Include how to calculate position size using account capital, risk percentage, entry price, and
        stop loss price. Explain why proper position sizing is crucial for risk management.
    """,

    'default': """
        Provide a brief explanation of the Classic Breakout trading strategy for a beginner.
        Include the key components: identifying consolidation, confirming breakouts with volume,
        entry and exit criteria, and the importance of proper risk management.
    """
}


def initialize_gemini_client():
    """
    Initialize and return a Google Gemini API client.
    # ... (rest of docstring) ...
    """
    # Check if library is installed first
    if not GENAI_INSTALLED:
         logger.error("google.generativeai not installed. Cannot initialize client.")
         return None

    if not GEMINI_API_KEY:
        logger.error("Gemini API key is missing. Cannot initialize client.")
        return None

    try:
        # import google.generativeai as genai # --- REMOVE IMPORT FROM HERE ---
        genai.configure(api_key=GEMINI_API_KEY)
        return genai # Return the imported module object
    # except ImportError: # --- REMOVE This specific except block ---
    #     logger.error("Failed to import google.generativeai...")
    #     return None
    except Exception as e:
        logger.error(f"Error initializing Gemini client: {str(e)}")
        return None



def get_educational_context(topic):
    """
    Get educational context for a specific trading topic using the Gemini API.
    # ... (rest of docstring and function body remains the same) ...
    """
    # Normalize topic
    normalized_topic = topic.lower().strip() if topic else 'default'

    # Get prompt for topic (use default if topic not found)
    prompt = EDUCATIONAL_PROMPTS.get(normalized_topic, EDUCATIONAL_PROMPTS['default'])

    # Initialize Gemini client
    local_genai_client = initialize_gemini_client() # Get the configured module/mock
    if not local_genai_client:
        return "Could not initialize the educational service. Please check the API key configuration or library installation."

    try:
        # Select the model (Access GenerativeModel via the returned client object)
        model = local_genai_client.GenerativeModel('gemini-pro')

        # Generate content
        response = model.generate_content(prompt)

        # Check for safety/content filtering blocks
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
            feedback = response.prompt_feedback
            if hasattr(feedback, 'block_reason') and feedback.block_reason:
                logger.warning(f"Content blocked. Reason: {feedback.block_reason}")
                return f"Sorry, I couldn't generate educational content for this topic due to content restrictions."

        # Extract and return text content
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'parts') and response.parts:
            # Alternative way to access text in some versions
            return response.parts[0].text
        else:
            logger.error("Unknown response format from Gemini API")
            # Return the specific error message the test expects now
            return "Sorry, there was an issue with the educational content format."

    except Exception as e:
        logger.error(f"Error getting educational content from Gemini: {str(e)}")
        return f"Sorry, there was an error while fetching educational content: {str(e)}"
