import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
PRIMARY_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")
FALLBACK_MODELS = [
    "meta-llama/Llama-3.3-70B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "google/gemma-2-9b-it"
]
APP_VERSION = "1.1.3-Static-Stability-Patch"

# Fast Static Explanations with Levels (instant load)
STATIC_EXPLANATIONS = {
    "photosynthesis": {
        "beginner": """Definition:
Photosynthesis is how plants use sunlight to make their own food.

Advantage:
It helps plants grow and creates the oxygen we breathe.

Disadvantage:
It cannot happen without sunlight or at night.

Related Terms:
Plant, Food, Sunlight""",
        "intermediate": """Definition:
Photosynthesis is a biochemical process where green plants convert light energy into chemical energy (glucose).

Advantage:
It is the primary source of oxygen for all living beings and provides the energy base for most life.

Disadvantage:
The process is highly dependent on environmental factors like water availability and specific temperature ranges.

Related Terms:
Chlorophyll, Glucose, Carbon Dioxide""",
        "advanced": """Definition:
Photosynthesis is a complex physiological pathway where photoautotrophs convert solar radiation into chemical potential energy stored in organic molecules.

Advantage:
It regulates global carbon cycles and maintain atmospheric oxygen levels through the light-dependent and Calvin cycle reactions.

Disadvantage:
In C3 plants, the efficiency is limited by photorespiration, where oxygen competes with carbon dioxide for the active site of RuBisCO.

Related Terms:
RuBisCO, Thylakoid, Photophosphorylation"""
    },
    "gravity": {
        "beginner": """Definition:
Gravity is an invisible pull that keeps everything on the ground.

Advantage:
It keeps our feet on the floor so we don't float away.

Disadvantage:
It makes it hard to jump very high or lift heavy things.

Related Terms:
Pull, Ground, Earth""",
        "intermediate": """Definition:
Gravity is a fundamental force of nature that attracts objects with mass toward each other.

Advantage:
It governs the motion of planets and keeps the atmosphere attached to Earth.

Disadvantage:
Escaping Earth's gravitational pull requires immense energy and specialized propulsion systems.

Related Terms:
Mass, Attraction, Orbit""",
        "advanced": """Definition:
Gravity is a fundamental interaction that causes mutual attraction between all things with mass or energy, described by General Relativity as spacetime curvature.

Advantage:
It provides the necessary centripetal force for planetary orbits and drives the formation of stars and galaxies from cosmic dust.

Disadvantage:
At cosmic scales, it causes gravitational collapse in massive stars, potentially leading to singularities like black holes.

Related Terms:
Spacetime, Relativity, Singularity"""
    },
    "atom": {
        "beginner": """Definition:
An atom is the smallest building block of everything in the universe.

Advantage:
Everything you see is made of these tiny blocks.

Disadvantage:
They are so small that you can't see them even with a microscope.

Related Terms:
Tiny, Block, Science""",
        "intermediate": """Definition:
An atom is the basic unit of a chemical element, consisting of a nucleus and orbiting electrons.

Advantage:
Atoms combine to form molecules, creating the diverse matter in our universe.

Disadvantage:
Splitting or altering atoms can release hazardous radiation or immense energy.

Related Terms:
Proton, Electron, Nucleus""",
        "advanced": """Definition:
An atom is the smallest constituent unit of ordinary matter that has the properties of a chemical element, defined by its atomic number of protons in the nucleus.

Advantage:
Atomic structure allows for the formation of covalent and ionic bonds, which are the fundamental forces behind chemical reactions and molecular biology.

Disadvantage:
The subatomic behavior of atoms follows quantum mechanics, leading to phenomena like electron-cloud probability and wave-particle duality which are difficult to predict.

Related Terms:
Isotope, Quantum Mechanics, Valency"""
    },
    "genetics": {
        "beginner": """Definition:
Genetics is the study of how traits are passed from parents to children.

Advantage:
It helps us understand why we look like our family.

Disadvantage:
Some genetic traits can cause diseases.

Related Terms:
DNA, Traits, Family""",
        "intermediate": """Definition:
Genetics is the scientific study of heredity and variation in living organisms.

Advantage:
It allows for the understanding and treatment of genetic disorders and the development of improved crops.

Disadvantage:
Ethical concerns arise with genetic engineering and privacy of genetic information.

Related Terms:
Gene, Chromosome, Heredity""",
        "advanced": """Definition:
Genetics is the branch of biology concerned with the study of genes, genetic variation, and heredity in organisms, encompassing molecular, Mendelian, and population genetics.

Advantage:
It provides insights into evolutionary processes, disease susceptibility, and personalized medicine through genomic sequencing and CRISPR technologies.

Disadvantage:
Complex genetic interactions and epigenetic modifications make predicting phenotypes from genotypes challenging, and genetic determinism can be a societal concern.

Related Terms:
Genome, Allele, Phenotype"""
    },
    "condensation": {
        "beginner": """Definition:
Condensation is when gas (like steam) cools down and turns back into water drops.

Advantage:
It creates rain and clouds which give water to the earth.

Disadvantage:
It can make windows foggy and walls wet if it happens inside.

Related Terms:
Wet, Steam, Rain""",
        "intermediate": """Definition:
Condensation is the change of the physical state of matter from gas phase into liquid phase.

Advantage:
It is an essential part of the water cycle and is used in industrial processes like distillation.

Disadvantage:
It can lead to mold growth and structural damage in buildings with poor insulation and high humidity.

Related Terms:
Vapor, Dew Point, Humidity""",
        "advanced": """Definition:
Condensation is a phase transition where a substance passes from the gaseous phase to the liquid phase, releasing latent heat of vaporization.

Advantage:
Atmospheric condensation is critical for global latent heat transport and the development of convective storm systems.

Disadvantage:
In industrial heat exchangers, dropwise condensation can be inhibited by non-condensable gases, reducing thermal efficiency.

Related Terms:
Latent Heat, Nucleation, Surface Tension"""
    },
    "evaporation": {
        "beginner": """Definition:
Evaporation is when water gets warm and turns into steam that goes up into the sky.

Advantage:
It dries your clothes when they are hanging outside in the sun.

Disadvantage:
It can dry up lakes and puddles during a hot day.

Related Terms:
Sun, Steam, Dry""",
        "intermediate": """Definition:
Evaporation is the process by which liquid water is converted into water vapor and enters the atmosphere.

Advantage:
It leaves behind pollutants and minerals, providing a natural way to purify water as it enters the clouds.

Disadvantage:
High rates of evaporation in arid regions can lead to soil salinization, making farming difficult.

Related Terms:
Vapor pressure, Heat, Arid""",
        "advanced": """Definition:
Evaporation is a type of vaporization that occurs on the surface of a liquid as it changes into the gas phase before reaching its boiling point.

Advantage:
Evaporative cooling is a key thermodynamic process used in both biological thermoregulation (sweating) and industrial cooling towers.

Disadvantage:
The rate of evaporation is limited by the partial pressure of the vapor in the surrounding gas and the available surface area.

Related Terms:
Thermodynamics, Partial Pressure, Entrophy"""
    },
    "respiration": {
        "beginner": """Definition:
Respiration is how living things breathe in air and use it to get energy from food.

Advantage:
It gives our bodies the energy to move, think, and grow.

Disadvantage:
If we can't breathe, our bodies can't get energy and will stop working.

Related Terms:
Breathe, Energy, Food""",
        "intermediate": """Definition:
Respiration is the biochemical process in which cells obtain energy by breaking down glucose and other organic molecules.

Advantage:
It provides ATP, the main energy currency of the cell, essential for all metabolic activities.

Disadvantage:
Anaerobic respiration is less efficient and produces byproducts like lactic acid, which can cause muscle fatigue.

Related Terms:
ATP, Glucose, Oxygen""",
        "advanced": """Definition:
Cellular respiration is a set of metabolic reactions and processes that take place in the cells of organisms to convert biochemical energy from nutrients into adenosine triphosphate (ATP), and then release waste products.

Advantage:
Aerobic respiration, particularly oxidative phosphorylation, is highly efficient, yielding a large amount of ATP necessary for complex multicellular life.

Disadvantage:
The process generates reactive oxygen species (ROS) as byproducts, which can cause oxidative stress and cellular damage if not properly managed by antioxidant systems.

Related Terms:
Glycolysis, Krebs Cycle, Electron Transport Chain"""
    },
    "osmosis": {
        "beginner": """Definition:
Osmosis is when water moves through a special skin from where there's a lot of water to where there's less.

Advantage:
It helps plants get water from the soil and keeps our cells healthy.

Disadvantage:
Too much or too little water can make cells swell or shrink too much.

Related Terms:
Water, Skin, Move""",
        "intermediate": """Definition:
Osmosis is the net movement of solvent molecules through a selectively permeable membrane into a region of higher solute concentration, aiming to equalize solute concentrations on the two sides.

Advantage:
It is crucial for maintaining turgor pressure in plant cells and regulating water balance in animal cells.

Disadvantage:
Dysregulation of osmosis can lead to dehydration or overhydration of cells, potentially causing cellular damage or death.

Related Terms:
Solute, Solvent, Membrane""",
        "advanced": """Definition:
Osmosis is a specific type of passive diffusion involving the spontaneous net movement of solvent molecules through a semipermeable membrane from a region of high solvent potential to a region of lower solvent potential.

Advantage:
It is fundamental to physiological processes such as kidney function, nutrient absorption in the gut, and the transport of water in vascular plants via root pressure.

Disadvantage:
In medical contexts, osmotic imbalances can lead to conditions like cerebral edema or hyponatremia, requiring careful management of fluid and electrolyte levels.

Related Terms:
Water Potential, Turgor, Isotonic"""
    },
    "combustion": {
        "beginner": """Definition:
Combustion is when something burns by reacting with oxygen and creating heat and light.

Advantage:
It provides energy for cooking food and heating homes.

Disadvantage:
It can release harmful smoke and gases into the air.

Related Terms:
Fire, Burning, Heat""",
        "intermediate": """Definition:
Combustion is a chemical reaction between a fuel and an oxidant (usually oxygen) that produces heat and light.

Advantage:
Controlled combustion drives car engines and power plants that generate electricity.

Disadvantage:
Incomplete combustion can produce carbon monoxide, which is a poisonous, colorless gas.

Related Terms:
Oxidation, Fuel, Exothermic""",
        "advanced": """Definition:
Combustion is a high-temperature exothermic redox chemical reaction between a fuel and an oxidant, often accompanied by flame and smoke.

Advantage:
The high energy density of combustion reactions is the primary driver of internal combustion engines and thermal power generation.

Disadvantage:
Atmospheric combustion of fossil fuels is the leading contributor to greenhouse gas emissions and environmental air pollution.

Related Terms:
Stoichiometry, Redox, Thermodynamics"""
    },
    "global warming": {
        "beginner": """Definition:
Global warming is when the Earth's air and oceans get warmer over time.

Advantage:
None. Global warming is harmful to life on Earth.

Disadvantage:
It melts ice at the poles, raises sea levels, and causes extreme weather.

Related Terms:
Heat, Earth, Weather""",
        "intermediate": """Definition:
Global warming is the long-term heating of Earth's climate system observed since the pre-industrial period due to human activities.

Advantage:
There are no significant advantages; it is a major environmental threat.

Disadvantage:
It leads to frequent natural disasters, shifts in ecosystems, and threats to food security.

Related Terms:
Greenhouse Effect, Climate Change, CO2""",
        "advanced": """Definition:
Global warming refers to the century-scale rise in the average temperature of the Earth's climate system and its related effects, caused by greenhouse gas emissions.

Advantage:
None. It represents a significant systemic risk to the biosphere and human civilization.

Disadvantage:
It results in ocean acidification, glacial retreat, and a fundamental shift in biodiversity and precipitation patterns.

Related Terms:
Radiative Forcing, Anthropogenic, IPCC"""
    }
}

# Hindi Static Explanations with Levels
STATIC_EXPLANATIONS_HI = {}

STATIC_TREES_HI = {}

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
PROMPT_TEMPLATE_QUIZ = """Generate 3 MCQs about "{term}" using the EXPLANATION below.
Return a RAW JSON ARRAY ONLY. NO markdown tags like ```json.

EXPLANATION:
"{explanation}"

JSON FORMAT:
[
  {{
    "question": "A short question based on the text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0
  }},
  ...
]"""

PROMPT_TEMPLATE_QUIZ_HI = """"{explanation}" के आधार पर "{term}" के बारे में 3 MCQs तैयार करें।
केवल RAW JSON सरणी ही लौटाएँ।

प्रारूप:
[
  {{
    "question": "प्रश्न?",
    "options": ["विकल्प ए", "विकल्प बी", "विकल्प सी", "विकल्प डी"],
    "correct_index": 0
  }},
  ...
]"""

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
        "model": PRIMARY_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 600,
        "temperature": 0.5,
        "top_p": 0.9
    }

    # Check Static Fallback first (Instant)
    term_key = term.lower().strip()
    if language == "hi":
        if term_key in STATIC_EXPLANATIONS_HI:
            entry = STATIC_EXPLANATIONS_HI[term_key]
            if isinstance(entry, dict):
                return entry.get(level, entry.get("beginner"))
            return entry
    elif language == "en":
        if term_key in STATIC_EXPLANATIONS:
            entry = STATIC_EXPLANATIONS[term_key]
            if isinstance(entry, dict):
                return entry.get(level, entry.get("beginner"))
            return entry

    models_to_try = [PRIMARY_MODEL] + FALLBACK_MODELS
    
    for current_model in models_to_try:
        payload["model"] = current_model
        for attempt in range(2):  # Auto-retry each model once
            try:
                response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=40)

                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content'].strip()
                        # Clean up common AI pleasantries
                        pleasantries = ["certainly!", "here is", "here's", "sure,", "i can help"]
                        lines = content.split('\n')
                        if lines and any(p in lines[0].lower() for p in pleasantries) and len(lines) > 1:
                            if ":" not in lines[0]: content = '\n'.join(lines[1:]).strip()
                        return content
                    continue # Try next model if format is weird

                # If quota/rate limited, try the next model in the list
                elif response.status_code in [402, 429]:
                    logger.warning(f"Model {current_model} reached quota/rate limit. Trying next model...")
                    break # Break out of attempt loop to try next model

                elif response.status_code == 503:
                    if attempt == 0:
                        import time
                        time.sleep(2)
                        continue
                    break # Try next model if still 503

                else:
                    if attempt == 1: break # Try next model
                    continue

            except Exception as e:
                logger.error(f"Error with {current_model}: {e}")
                if attempt == 1: break
                continue

    return "AI is currently very busy. Please try again after 1 minute."

import json
import re

# Static fallback quizzes for common terms
STATIC_QUIZZES = {
    "photosynthesis": [
        {"question": "What is the primary source of energy for photosynthesis?", "options": ["Water", "Soil", "Sunlight", "Oxygen"], "correct_index": 2},
        {"question": "Which gas do plants absorb from the atmosphere for photosynthesis?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "correct_index": 1},
        {"question": "What is the green pigment in plants that absorbs light?", "options": ["Hemoglobin", "Chlorophyll", "Melanin", "Carotene"], "correct_index": 1}
    ],
    "gravity": [
        {"question": "Who is famous for the law of universal gravitation?", "options": ["Einstein", "Newton", "Tesla", "Galileo"], "correct_index": 1},
        {"question": "Gravity is a force that ____ objects toward each other.", "options": ["Pushes", "Rotates", "Pulls", "Repels"], "correct_index": 2},
        {"question": "What happens to gravity as the distance between two objects increases?", "options": ["Increases", "Decreases", "Stays the same", "Disappears"], "correct_index": 1}
    ],
    "atom": [
        {"question": "What is the center of an atom called?", "options": ["Proton", "Neutron", "Nucleus", "Electron"], "correct_index": 2},
        {"question": "Which particle in an atom has a negative charge?", "options": ["Proton", "Neutron", "Electron", "Photon"], "correct_index": 2},
        {"question": "Which particles are found inside the nucleus?", "options": ["Electrons and Protons", "Protons and Neutrons", "Electrons and Neutrons", "Only Electrons"], "correct_index": 1}
    ]
}

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
        "model": PRIMARY_MODEL,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1000,  # Increased token limit
        "temperature": 0.5,   # Lower temperature for structure
        "top_p": 0.95
    }

    models_to_try = [PRIMARY_MODEL] + FALLBACK_MODELS
    
    for current_model in models_to_try:
        payload["model"] = current_model
        for attempt in range(2):
            try:
                response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=45)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content'].strip()
                        content = content.replace("```json", "").replace("```", "").strip()
                        start = content.find("[")
                        end = content.rfind("]")
                        if start != -1 and end != -1:
                            content = content[start:end+1]
                        try:
                            json.loads(content)
                            return content
                        except: logger.error(f"Invalid Quiz JSON: {content}")
                    continue

                elif response.status_code in [402, 429]:
                    logger.warning(f"Quiz: Model {current_model} busy. Trying next...")
                    break 

                elif response.status_code == 503:
                    if attempt == 0:
                        import time
                        time.sleep(2)
                        continue
                    break

                else:
                    if attempt == 1: break
                    continue

            except Exception as e:
                logger.error(f"Quiz Error with {current_model}: {e}")
                if attempt == 1: break
                continue

    # Final Fallback if all AI fail
    term_key = term.lower().strip()
    if term_key in STATIC_QUIZZES and language == "en":
        return json.dumps(STATIC_QUIZZES[term_key])
    
    # Generic Relevant Quiz Fallback
    generic_quiz = [
        {"question": f"Which of the following describes '{term}'?", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_index": 0},
        {"question": f"True or False: The concept of '{term}' is fundamental to science.", "options": ["True", "False"], "correct_index": 0}
    ]
    return json.dumps(generic_quiz)
    

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
└── Genetics""",
    "genetics": """Biology
├── Genetics
│   ├── Molecular Genetics
│   │   ├── *Genetics*
│   │   │   ├── DNA Structure
│   │   │   └── Gene Expression
│   │   └── Genomics
│   └── Heredity
└── Evolutionary Biology""",
    "condensation": """Physics/Meteorology
├── Phase Changes
│   ├── Phase Transitions
│   │   ├── *Condensation*
│   │   │   ├── Cloud Formation
│   │   │   └── Precipitation
│   │   └── Evaporation
│   └── State of Matter
└── Thermal Physics""",
    "evaporation": """Physics/Chemistry
├── Phase Changes
│   ├── Phase Transitions
│   │   ├── *Evaporation*
│   │   │   ├── Boiling Point
│   │   │   └── Vapor Pressure
│   │   └── Condensation
│   └── Hydrology
└── Thermodynamics""",
    "respiration": """Biology
├── Cell Biology
│   ├── Metabolism
│   │   ├── *Respiration*
│   │   │   ├── Aerobic Respiration
│   │   │   └── Anaerobic Respiration
│   │   └── ATP Production
│   └── Physiology
└── Biochemistry""",
    "combustion": """Chemistry/Physics
├── Chemical Reactions
│   ├── Oxidation
│   │   ├── *Combustion*
│   │   │   ├── Exothermic Process
│   │   │   └── Fuel/Oxidant
│   │   └── Redox Reactions
│   └── Thermodynamics
└── Energy Production""",
    "global warming": """Environmental Science
├── Climate Change
│   ├── Atmosphere
│   │   ├── *Global Warming*
│   │   │   ├── Greenhouse Effect
│   │   │   └── Carbon Emissions
│   │   └── Meteorology
│   └── Ecology
└── Sustainability"""
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
└── परमाणु भौतिकी""",
    "genetics": """जीव विज्ञान (Biology)
├── आनुवंशिकी (Genetics)
│   ├── आणविक आनुवंशिकी
│   │   ├── *आनुवंशिकी* (Genetics)
│   │   │   ├── डीएनऐ संरचना
│   │   │   └── जीन अभिव्यक्ति
│   │   └── जीनोमिक्स
│   └── आनुवंशिकता
└── विकासात्मक जीवविज्ञान"""
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
        "model": PRIMARY_MODEL,
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 400,
        "temperature": 0.0,
        "top_p": 1.0
    }

    models_to_try = [PRIMARY_MODEL] + FALLBACK_MODELS
    
    for current_model in models_to_try:
        payload["model"] = current_model
        for attempt in range(2):
            try:
                response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=35)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content']
                        content = content.replace("```", "").strip()
                        return content
                    continue

                elif response.status_code in [402, 429]:
                    logger.warning(f"Tree: Model {current_model} busy. Trying next...")
                    break 

                elif response.status_code == 503:
                    if attempt == 0:
                        import time
                        time.sleep(3)
                        continue
                    break

                else:
                    if attempt == 1: break
                    continue

            except Exception as e:
                logger.error(f"Tree Error with {current_model}: {e}")
                if attempt == 1: break
                continue

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
