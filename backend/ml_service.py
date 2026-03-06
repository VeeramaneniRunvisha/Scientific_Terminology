import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration - Using new router endpoint
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.3-70B-Instruct")  # Fast, accurate, great Hindi support

if not HF_API_TOKEN:
    logger.warning("HF_API_TOKEN is not set in environment variables.")

# Prompt templates for different difficulty levels
PROMPT_TEMPLATES = {
    "beginner": """You are an educational assistant. Follow the format EXACTLY.

IMPORTANT: Keep your response SHORT. Maximum 3-4 sentences total.

You MUST use this EXACT format:

Definition:
Write ONE simple sentence here.

Advantage:
Write ONE short benefit here.

Disadvantage:
Write ONE short limitation here.

Related Terms:
Term1, Term2, Term3

EXAMPLE for "Gravity":
Definition:
Gravity is a force that pulls things down to the ground.

Advantage:
It keeps us from floating away into space.

Disadvantage:
It makes it hard to jump very high.

Related Terms:
Weight, Mass, Force

RULES:
- Use simple words a child would understand
- NO long paragraphs
- NO technical terms
- Each section = ONE short sentence only
- Related Terms = exactly 2-3 simple related words, comma-separated""",

    "intermediate": """You are an educational assistant. Follow the format EXACTLY.

IMPORTANT: Keep your response CONCISE. Maximum 4-5 sentences total.

You MUST use this EXACT format:

Definition:
Write ONE clear sentence with basic scientific terms.

Advantage:
Write ONE detailed benefit (1-2 sentences max).

Disadvantage:
Write ONE limitation or challenge (1-2 sentences max).

Related Terms:
Term1, Term2, Term3

EXAMPLE for "Photosynthesis":
Definition:
Photosynthesis is the biochemical process where plants convert light energy into chemical energy stored in glucose.

Advantage:
It produces oxygen as a byproduct, which is essential for most life on Earth.

Disadvantage:
It requires specific conditions like adequate sunlight and water, limiting where plants can thrive.

Related Terms:
Chlorophyll, Glucose, Carbon Dioxide

RULES:
- Use scientific terms but keep them brief
- NO long paragraphs or multiple points
- Each section = 1-2 sentences maximum
- MUST include all four sections: Definition, Advantage, Disadvantage, Related Terms
- Related Terms = exactly 2-3 scientific terms, comma-separated""",

    "advanced": """You are an educational assistant. Follow the format EXACTLY.

IMPORTANT: Keep your response FOCUSED. Maximum 5-6 sentences total.

You MUST use this EXACT format:

Definition:
Write ONE technical definition.

Advantage:
Write ONE key benefit with technical detail (2 sentences max).

Disadvantage:
Write ONE limitation with technical detail (2 sentences max).

Related Terms:
Term1, Term2, Term3

EXAMPLE for "Photosynthesis":
Definition:
Photosynthesis is the light-dependent and light-independent biochemical process by which photoautotrophs convert electromagnetic radiation into chemical energy stored in glucose molecules.

Advantage:
It exhibits remarkable energy conversion efficiency of 3-6% for C3 plants, producing ATP and NADPH through the electron transport chain while releasing molecular oxygen.

Disadvantage:
The process is limited by photorespiration in C3 plants, where RuBisCO catalyzes an oxygenation reaction that reduces carbon fixation efficiency by up to 50%.

Related Terms:
Chloroplast, Calvin Cycle, RuBisCO

RULES:
- Use proper scientific terminology
- NO lengthy explanations or multiple paragraphs
- Each section = 1-2 sentences maximum
- MUST include all four sections: Definition, Advantage, Disadvantage, Related Terms - no exceptions
- Focus on ONE key point per section
- Related Terms = exactly 2-3 technical/scientific terms, comma-separated"""
}

# Hindi prompt templates
PROMPT_TEMPLATES_HI = {
    "beginner": """You are an educational assistant. Respond ONLY in Hindi.

Use this EXACT format:

परिभाषा:
(one simple sentence in Hindi)

लाभ:
(one short benefit in Hindi)

हानि:
(one short limitation in Hindi)

संबंधित शब्द:
(2-3 related words in Hindi, comma-separated)

RULES: Simple words, no technical terms, each section = 1 sentence only. Hindi ONLY.""",

    "intermediate": """You are an educational assistant. Respond ONLY in Hindi.

Use this EXACT format:

परिभाषा:
(one clear scientific sentence in Hindi)

लाभ:
(1-2 sentences on benefit in Hindi)

हानि:
(1-2 sentences on limitation in Hindi)

संबंधित शब्द:
(2-3 scientific terms in Hindi, comma-separated)

RULES: Use scientific terms, keep concise, all 4 sections required. Hindi ONLY.""",

    "advanced": """You are an educational assistant. Respond ONLY in Hindi.

Use this EXACT format:

परिभाषा:
(one technical definition in Hindi)

लाभ:
(1-2 sentences with technical detail in Hindi)

हानि:
(1-2 sentences with technical limitation in Hindi)

संबंधित शब्द:
(2-3 technical/scientific terms, comma-separated)

RULES: Proper scientific terminology, all 4 sections required, focused. Hindi ONLY."""
}

# Quiz Prompt Templates
PROMPT_TEMPLATE_QUIZ = """You are a quiz generator.
Create 3 multiple-choice questions (MCQs) about "{term}", based on the following explanation:

EXPLANATION:
"{explanation}"

OUTPUT FORMAT:
Return a raw JSON array. No markdown.
[
  {{
    "question": "Question based on the explanation?",
    "options": ["A", "B", "C", "D"],
    "correct_index": 0
  }},
  {{
    "question": "Another question from the text?",
    "options": ["X", "Y", "Z", "W"],
    "correct_index": 1
  }},
  {{
    "question": "Final question?",
    "options": ["1", "2", "3", "4"],
    "correct_index": 2
  }}
]

RULES:
- "correct_index" is 0-3.
- Questions MUST be relevant to the provided EXPLANATION.
- Keep questions short.
- JSON only.
"""

PROMPT_TEMPLATE_QUIZ_HI = """आप एक प्रश्नोत्तरी जनरेटर हैं।
"{term}" के बारे में 3 बहुविकल्पीय प्रश्न (MCQ) बनाएं, जो निम्नलिखित स्पष्टीकरण पर आधारित हों:

स्पष्टीकरण (EXPLANATION):
"{explanation}"

आउटपुट प्रारूप (OUTPUT FORMAT):
केवल JSON सरणी लौटाएं। कोई मार्कडाउन नहीं।
[
  {{
    "question": "स्पष्टीकरण पर आधारित प्रश्न?",
    "options": ["A", "B", "C", "D"],
    "correct_index": 0
  }},
  {{
    "question": "पाठ से एक और प्रश्न?",
    "options": ["X", "Y", "Z", "W"],
    "correct_index": 1
  }},
  {{
    "question": "अंतिम प्रश्न?",
    "options": ["1", "2", "3", "4"],
    "correct_index": 2
  }}
]

नियम:
- "correct_index" 0-3 है।
- प्रश्न प्रदान किए गए स्पष्टीकरण (EXPLANATION) के लिए प्रासंगिक होने चाहिए।
- प्रश्न छोटे रखें।
- केवल JSON।
"""

def generate_explanation(term: str, level: str = "beginner", language: str = "en") -> str:
    """
    Generate an explanation for a scientific term using Hugging Face Inference API.
    Uses the new router.huggingface.co endpoint with chat completions format.
    
    Args:
        term: The scientific term to explain
        level: Difficulty level - "beginner", "intermediate", or "advanced"
        language: Language for the explanation - "en" for English, "hi" for Hindi
    """
    # Validate level
    if level not in PROMPT_TEMPLATES:
        logger.warning(f"Invalid level '{level}', defaulting to 'beginner'")
        level = "beginner"
    
    if not HF_API_TOKEN:
        return "Error: AI API Token is missing. Please configure the backend."

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Select appropriate prompt template based on level and language
    if language == "hi":
        if level not in PROMPT_TEMPLATES_HI:
            logger.warning(f"Invalid level '{level}' for Hindi, defaulting to 'beginner'")
            level = "beginner"
        system_prompt = PROMPT_TEMPLATES_HI[level]
    else:
        system_prompt = PROMPT_TEMPLATES[level]

    user_prompt = f'Explain "{term}"'

    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 600,  # Increased to 600 to prevent cutoff in advanced level responses
        "temperature": 0.5,  # Lower temperature for more focused output
        "top_p": 0.9
    }

    for attempt in range(2):  # Auto-retry once on timeout
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=45)

            if response.status_code == 200:
                result = response.json()
                # Extract content from chat completion format
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    return content.strip()
                else:
                    logger.error(f"Unexpected API response format: {result}")
                    return "Error: Unexpected response format from AI service."

            # Handle model loading (503 Service Unavailable is common for cold starts)
            elif response.status_code == 503:
                try:
                    error_data = response.json()
                    estimated_time = error_data.get("estimated_time", 20)
                    logger.info(f"Model is loading. Estimated time: {estimated_time}s")
                    return f"Model is currently loading (approx {estimated_time:.0f}s). Please try again shortly."
                except:
                    return "Model is currently loading. Please try again shortly."

            else:
                logger.error(f"API Error {response.status_code}: {response.text}")
                return f"Error: Failed to generate explanation (Status {response.status_code})."

        except requests.exceptions.Timeout:
            if attempt == 0:
                logger.warning("API Request timed out on attempt 1, retrying...")
                continue  # Retry once
            logger.error("API Request timed out after retry")
            return "Error: Request timed out. The AI service is slow right now."
        except Exception as e:
            logger.error(f"Exception during API call: {e}")
            return f"Error: An internal error occurred ({str(e)})."

import json
import re

def generate_quiz(term: str, language: str = "en", explanation: str = "") -> str:
    """
    Generate 3 MCQs for a term using Hugging Face Inference API.
    Returns a JSON string.
    """
    if not HF_API_TOKEN:
        return "[]"

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    if language == "hi":
        user_prompt = PROMPT_TEMPLATE_QUIZ_HI.format(term=term, explanation=explanation)
    else:
        user_prompt = PROMPT_TEMPLATE_QUIZ.format(term=term, explanation=explanation)

    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1000,  # Increased token limit
        "temperature": 0.5,   # Lower temperature for structure
        "top_p": 0.95
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # Cleanup content
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Try to extract JSON array using regex if there's extra text
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)
                
                # Validate JSON
                try:
                    json.loads(content)
                    return content
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON generated: {content}")
                    # Fallback or retry logic could go here
            else:
                logger.error(f"Unexpected API response format: {result}")
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
    
    # Fallback Quiz (if API fails)
    fallback_quiz = [
        {
            "question": f"What is the main concept of {term}?",
            "options": ["It is a key scientific principle.", "It is a type of food.", "It is a planet.", "It is a historical event."],
            "correct_index": 0
        },
        {
            "question": f"Which field of science studies {term}?",
            "options": ["Physics/Chemistry/Biology", "Literature", "History", "Arts"],
            "correct_index": 0
        },
         {
            "question": f"Is {term} important?",
            "options": ["Yes, very important.", "No, not at all.", "Maybe.", "I don't know."],
            "correct_index": 0
        }
    ]
    
    return json.dumps(fallback_quiz)

# Concept Tree Prompt Templates
PROMPT_TEMPLATE_TREE = """You are an educational assistant.
Generate a hierarchical "Concept Family Tree" for the term "{term}".

OUTPUT FORMAT:
Return a clean text-based tree using lines and indentation. NO markdown code blocks.
Structure:
- Top level: Broader field (Parent)
- Second level: The term "{term}" (verify it fits here)
- Third level: Key sub-concepts or related types (Children)

Example for "Gravity":
Physics
├── Mechanics
│   ├── Forces
│   │   ├── *Gravity* (Target)
│   │   │   ├── Universal Gravitation
│   │   │   └── General Relativity
│   │   └── Electromagnetism
│   └── Kinematics
└── Thermodynamics

RULES:
- Use standard tree characters: ├──, └──, │
- Mark the target term "{term}" with *asterisks*.
- Keep it concise (max 10-12 lines).
- Use academic/scientific terms.
- No definitions, just terms.
"""

PROMPT_TEMPLATE_TREE_HI = """आप एक शैक्षिक सहायक हैं।
शब्द "{term}" के लिए एक पदानुक्रमित "अवधारणा परिवार वृक्ष" (Concept Family Tree) बनाएं।

आउटपुट प्रारूप:
लाइनों और इंडेंटेशन का उपयोग करके एक साफ टेक्स्ट-आधारित पेड़ लौटाएं। कोई मार्कडाउन कोड ब्लॉक नहीं।
संरचना:
- शीर्ष स्तर: व्यापक क्षेत्र (Parent)
- दूसरा स्तर: शब्द "{term}"
- तीसरा स्तर: प्रमुख उप-अवधारणाएं (Children)

उदाहरण "गुरुत्वाकर्षण" के लिए:
भौतिक विज्ञान (Physics)
├── यांत्रिकी (Mechanics)
│   ├── बल (Forces)
│   │   ├── *गुरुत्वाकर्षण* (Target)
│   │   │   ├── गुरुत्वाकर्षण का नियम
│   │   │   └── सामान्य सापेक्षता
│   │   └── विद्युत चुंबकत्व
│   └── शुद्ध गतिविज्ञान
└── ऊष्मप्रवैगिकी

नियम:
- मानक वृक्ष वर्णों का उपयोग करें: ├──, └──, │
- लक्ष्य शब्द "{term}" को *तारांकन* के साथ चिह्नित करें।
- इसे संक्षिप्त रखें (अधिकतम 10-12 पंक्तियां)।
- अकादमिक/वैज्ञानिक शब्दों का उपयोग करें।
- कोई परिभाषा नहीं, केवल शब्द।
"""

def generate_concept_tree(term: str, language: str = "en") -> str:
    """
    Generate a concept hierarchy tree for a term.
    """
    if not HF_API_TOKEN:
        return "Error: AI API Token missing."

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    if language == "hi":
        user_prompt = PROMPT_TEMPLATE_TREE_HI.format(term=term)
    else:
        user_prompt = PROMPT_TEMPLATE_TREE.format(term=term)

    payload = {
        "model": HF_MODEL,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 400,
        "temperature": 0.4,
        "top_p": 0.9
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                # Cleanup
                content = content.replace("```text", "").replace("```", "").strip()
                return content
    except Exception as e:
        logger.error(f"Error generating concept tree: {e}")
    
    return f"Could not generate tree for {term}."

# Optional: Quick test
if __name__ == "__main__":
    print(generate_explanation("Photosynthesis"))
    # print(generate_quiz("Photosynthesis"))
