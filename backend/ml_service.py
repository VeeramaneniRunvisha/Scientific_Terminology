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
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.3-70B-Instruct")  # Reverted as requested
APP_VERSION = "1.0.3-Fallback-Trees"

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
                    content = result['choices'][0]['message']['content'].strip()
                    
                    # Clean up common AI pleasantries to ensure "explanation only"
                    pleasantries = [
                        "certainly!", "here is", "here's", "sure,", "i can help", 
                        "according to", "based on", "the following is"
                    ]
                    lines = content.split('\n')
                    if lines and any(p in lines[0].lower() for p in pleasantries) and len(lines) > 1:
                        # If the first line is a pleasantry and there's more content, skip it
                        if ":" not in lines[0]: # Don't skip if it's a header like "Definition:"
                             content = '\n'.join(lines[1:]).strip()

                    return content
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

            elif response.status_code == 402:
                logger.error("AI API Quota reached (Status 402).")
                return "Error: AI Free Quota reached. Please try again tomorrow or switch to a lighter model."
            
            elif response.status_code == 429:
                logger.warning("AI API Rate Limit reached (Status 429).")
                return "Error: Too many people using the AI right now. Please wait 10 seconds and try again."

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

    for attempt in range(3):  # Increased to 3 retries
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=50)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    content = content.replace("```json", "").replace("```", "").strip()
                    json_match = re.search(r'\[.*\]', content, re.DOTALL)
                    if json_match: content = json_match.group(0)
                    try:
                        json.loads(content)
                        return content
                    except: logger.error(f"Invalid JSON: {content}")
                else: logger.error(f"Format error: {result}")
            
            elif response.status_code == 429:
                # Rate limited
                if attempt == 2: return "BUSY"
                import time
                time.sleep(2) # Wait 2 seconds and retry
                continue

            elif response.status_code == 503:
                if attempt == 2: return "LOADING"
                import time
                time.sleep(3) # Wait for model load
                continue

        except Exception as e:
            if attempt == 2: logger.error(f"Quiz Error: {e}")
    
    # Fallback Quiz
    fallback = [
        {"question": f"Is {term} a scientific concept?", "options": ["Yes", "No", "Maybe", "Don't know"], "correct_index": 0},
        {"question": f"The term '{term}' is used in science.", "options": ["True", "False", "Partially", "None"], "correct_index": 0},
        {"question": f"Should we study {term}?", "options": ["Yes", "No", "It's optional", "None"], "correct_index": 0}
    ]
    return json.dumps(fallback)
    
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
- Mark the target term "{term}" with *asterisks* (e.g., *{term}*).
- Keep it small (max 6-8 lines).
- No definitions, just name of concepts.
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

# Static fallback trees for common terms
STATIC_TREES = {
    "photosynthesis": """Biology
├── Botany
│   ├── Plant Physiology
│   │   ├── *Photosynthesis*
│   │   │   ├── Light-dependent Reactions
│   │   │   └── Calvin Cycle
│   │   └── Respiration
│   └── Ecology
└── Biochemistry""",
    "gravity": """Physics
├── Mechanics
│   ├── Classical Mechanics
│   │   ├── *Gravity*
│   │   │   ├── Newton's Laws
│   │   │   └── Orbital Mechanics
│   │   └── Kinetic Energy
│   └── General Relativity
└── Astrophysics""",
    "atom": """Chemistry
├── Atomic Theory
│   ├── Subatomic Particles
│   │   ├── *Atom*
│   │   │   ├── Nucleus (Protons/Neutrons)
│   │   │   └── Electron Cloud
│   │   └── Quantum Mechanics
│   └── Molecular Structure
└── Nuclear Physics""",
    "cell": """Biology (Life)
├── Cell Biology
│   ├── Types of Cells
│   │   ├── *Cell*
│   │   │   ├── Prokaryotic Cells
│   │   │   └── Eukaryotic Cells
│   │   └── Cell Structure
│   └── Molecular Biology
└── Genetics""",
    "energy": """Physics
├── Fundamental Science
│   ├── Physical Quantities
│   │   ├── *Energy*
│   │   │   ├── Potential Energy
│   │   │   └── Kinetic Energy
│   │   └── Work and Power
│   └── Thermodynamics
└── Quantum Physics""",
    "evolution": """Biology
├── Evolutionary Biology
│   ├── Mechanisms
│   │   ├── *Evolution*
│   │   │   ├── Natural Selection
│   │   │   └── Genetic Drift
│   │   └── Speciation
│   └── Paleontology
└── Genetics"""
}

# Static fallback trees for common terms in Hindi
STATIC_TREES_HI = {
    "photosynthesis": """जीव विज्ञान (Biology)
├── वनस्पति विज्ञान (Botany)
│   ├── पादप शरीर क्रिया विज्ञान
│   │   ├── *प्रकाश संश्लेषण* (Photosynthesis)
│   │   │   ├── प्रकाश-निर्भर अभिक्रियाएं
│   │   │   └── केल्विन चक्र
│   │   └── श्वसन
│   └── पारिस्थितिकी
└── जैव रसायन""",
    "gravity": """भौतिक विज्ञान (Physics)
├── यांत्रिकी (Mechanics)
│   ├── चिरसम्मत यांत्रिकी
│   │   ├── *गुरुत्वाकर्षण* (Gravity)
│   │   │   ├── न्यूटन के नियम
│   │   │   └── कक्षीय यांत्रिकी
│   │   └── गतिज ऊर्जा
│   └── सामान्य सापेक्षता
└── खगोल भौतिकी""",
    "atom": """रसायन विज्ञान (Chemistry)
├── परमाणु सिद्धांत
│   ├── उप-परमाणु कण
│   │   ├── *परमाणु* (Atom)
│   │   │   ├── नाभिक (Nucleus)
│   │   │   └── इलेक्ट्रॉन क्लाउड
│   │   └── क्वांटम यांत्रिकी
│   └── आणविक संरचना
└── परमाणु भौतिकी"""
}

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
        "temperature": 0.0,  # Stable and fast
        "top_p": 1.0
    }

    for attempt in range(2):
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=35)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    content = content.replace("```", "").strip()
                    return content
            elif response.status_code == 429:
                if attempt == 1: return "AI is busy. Please try again in 10 seconds."
                import time
                time.sleep(2)
                continue
            elif response.status_code == 503:
                if attempt == 1: return "AI model is still loading. Please try again soon."
                import time
                time.sleep(3)
                continue
            else:
                if attempt == 1:
                    logger.error(f"Tree API Error {response.status_code}: {response.text}")
                    return f"AI Service error (Status {response.status_code})."
                import time
                time.sleep(1)
                continue

        except requests.exceptions.Timeout:
            if attempt == 1: return "AI service taking too long. Please try again later."
            import time
            time.sleep(1)
        except Exception as e:
            if attempt == 1: 
                logger.error(f"Tree Error: {e}")
                return "An internal error occurred."
    
    # If AI fails, use static fallback if available
    term_key = term.lower().strip()
    if language == "hi":
        if term_key in STATIC_TREES_HI:
            return STATIC_TREES_HI[term_key]
    else:
        if term_key in STATIC_TREES:
            return STATIC_TREES[term_key]
    
    return f"Unable to generate tree for {term} at this moment. Please try again." if language == "en" else f"{term} के लिए वृक्ष नहीं बनाया जा सका। कृपया पुनः प्रयास करें।"

# Optional: Quick test
if __name__ == "__main__":
    print(generate_explanation("Photosynthesis"))
    # print(generate_quiz("Photosynthesis"))
