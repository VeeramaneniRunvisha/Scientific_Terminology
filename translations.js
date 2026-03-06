// Translations for English and Hindi
const translations = {
    en: {
        // Common
        appTitle: "Concept Clarity",
        appDescription: "Master scientific terms with simple explanations.",

        // User Profile
        loading: "Loading...",
        unknownUser: "Unknown User",
        guest: "Guest",

        // Change Password
        changePassword: "Change Password",
        currentPassword: "Current Password",
        newPassword: "New Password",
        updatePassword: "Update Password",
        passwordUpdated: "Password updated successfully",
        fillAllFields: "Please fill all fields",

        // Learning Levels
        chooseLearningLevel: "Choose Your Learning Level:",
        beginner: "Beginner",
        beginnerDesc: "Simple & clear explanations",
        intermediate: "Intermediate",
        intermediateDesc: "More detailed insights",
        advanced: "Advanced",
        advancedDesc: "Technical & comprehensive",

        // Input Section
        inputPlaceholder: "Enter a term (e.g., gravity)...",
        explainButton: "Explain It",
        speakTitle: "Speak",

        // Buttons
        historyButton: "History",
        logoutButton: "Logout",

        // Output Section
        explanationHeading: "Explanation:",
        jsonFormatHeading: "JSON Format:",
        listenButton: "Listen",
        stopButton: "Stop",

        // History Modal
        searchHistory: "Search History",
        noHistoryYet: "No search history yet",
        startSearching: "Start searching for scientific terms!",

        // Error Messages
        enterTerm: "Please enter a scientific term.",
        generatingExplanation: "Generating explanation...",
        mayTakeTime: "This may take 10-20 seconds.",
        errorHeading: "Error",
        connectionError: "Could not connect to the backend.",
        details: "Details:",
        makeSureRunning: "Make sure 'main.py' is running on port 8000.",

        // Login Page
        welcomeBack: "Welcome Back",
        loginSubtitle: "Login to continue your learning journey.",
        username: "Username",
        enterUsername: "Enter your Username",
        password: "Password",
        enterPassword: "Enter your password",
        rememberMe: "Remember me",
        forgotPassword: "Forgot Password?",
        forgotPasswordAlert: "Forgot Password feature coming soon!",
        loginButton: "Login",
        noAccount: "Don't have an account?",
        signUp: "Sign Up",

        // Register Page
        joinUs: "Join Us",
        registerSubtitle: "Create an account to start exploring.",
        fullName: "Full Name",
        fullNamePlaceholder: "Full Name",
        email: "Email",
        emailPlaceholder: "Email Address",
        createPassword: "Create Password",
        confirmPassword: "Confirm Password",
        confirmPasswordPlaceholder: "Confirm Password",
        registerButton: "Register",
        alreadyHaveAccount: "Already have an account?",
        login: "Login",

        // Password Strength
        weak: "Weak",
        medium: "Medium",
        strong: "Strong",

        // Auth Messages
        registrationSuccess: "Registration successful! Redirecting to login...",
        loginSuccess: "Login successful! Redirecting...",
        invalidCredentials: "Invalid email or password",
        emailAlreadyRegistered: "Email already registered",
        passwordMismatch: "Passwords do not match",
        fillAllFields: "Please fill in all fields",

        // Language Selector
        language: "Language",
        english: "English",
        hindi: "हिंदी",

        // Feedback
        about: "About",
        contact: "Contact",
        aboutUs: "About Us",
        contactUs: "Contact Us",
        aboutContent: "Concept Clarity is an AI-powered educational tool designed to make scientific terms easy to understand for everyone.<br><br>Our Mission:<br>1. Simplify complex scientific concepts.<br>2. Provide multi-level explanations (Beginner, Intermediate, Advanced).<br>3. Enhance learning with visual and audio aids.<br>4. Make education accessible in multiple languages.<br>5. <b>Feedback:</b> We value your input! <a href='#' onclick='openFeedbackModal(); return false;' style='color: #bb86fc;'>Click here</a> to share your thoughts.",
        contactContent: "Have questions or suggestions? Reach out to us at:<br><br>📧 Email: support@conceptclarity.com<br>📞 Phone: +91 98765 43210<br>📍 Location: Mumbai, India",
        feedback: "Feedback",
        giveFeedback: "Give Feedback",
        rateExperience: "Rate Your Experience",
        yourRating: "Your Rating",
        comments: "Comments (Optional)",
        commentsPlaceholder: "Share your thoughts about the app...",
        submitFeedback: "Submit Feedback",
        cancel: "Cancel",
        feedbackSuccess: "Thank you for your feedback!",
        feedbackError: "Failed to submit feedback. Please try again.",
        pleaseRate: "Please select a rating",
        thankYouFeedback: "Your feedback helps us improve!",
        usageLimitReached: "You have reached your daily free usage limit (2 searches). Please login to continue.",
        continueAsGuest: "Continue as Guest",
        relatedVideos: "Related Videos",
        watchOnYouTube: "Watch on YouTube",
        takeQuiz: "Quiz",
        generatingQuiz: "Generating Quiz...",
        quizHeading: "Test Your Knowledge",
        conceptTree: "Concept Family Tree",
        generatingTree: "Generating Tree...",
        submit: "Submit",
        correct: "Correct!",
        wrong: "Wrong!",
        score: "Your Score",
        excellent: "Excellent!",
        good: "Good Job!",
        needsPractice: "Keep Practicing!",
        showJson: "Show JSON Format",
        hideJson: "Hide JSON Format",

        // Settings
        settings: "Settings",
        settings: "Settings",
        account: "Account",
        fullName: "Full Name",
        learningPreferences: "Learning Preferences",
        defaultLevel: "Default Level",
        appearance: "Appearance",
        theme: "Theme",
        darkTheme: "Dark (Default)",
        lightTheme: "Light",
        audio: "Audio",
        audioSpeed: "Audio Speed",
        autoPlay: "Auto-play Audio",
        done: "Done"
    },
    hi: {
        // Common
        appTitle: "अवधारणा स्पष्टता",
        appDescription: "सरल व्याख्याओं के साथ वैज्ञानिक शब्दों में महारत हासिल करें।",

        // User Profile
        loading: "लोड हो रहा है...",
        unknownUser: "अज्ञात उपयोगकर्ता",
        guest: "अतिथि",

        // Change Password
        changePassword: "पासवर्ड बदलें",
        currentPassword: "वर्तमान पासवर्ड",
        newPassword: "नया पासवर्ड",
        updatePassword: "पासवर्ड अपडेट करें",
        passwordUpdated: "पासवर्ड सफलतापूर्वक अपडेट किया गया",
        fillAllFields: "कृपया सभी फ़ील्ड भरें",

        // Learning Levels
        chooseLearningLevel: "अपना सीखने का स्तर चुनें:",
        beginner: "शुरुआती",
        beginnerDesc: "सरल और स्पष्ट व्याख्या",
        intermediate: "मध्यवर्ती",
        intermediateDesc: "अधिक विस्तृत जानकारी",
        advanced: "उन्नत",
        advancedDesc: "तकनीकी और व्यापक",

        // Input Section
        inputPlaceholder: "एक शब्द दर्ज करें (उदा., गुरुत्वाकर्षण)...",
        explainButton: "व्याख्या करें",
        speakTitle: "बोलें",

        // Buttons
        historyButton: "इतिहास",
        logoutButton: "लॉगआउट",

        // Output Section
        explanationHeading: "व्याख्या:",
        jsonFormatHeading: "JSON प्रारूप:",
        listenButton: "सुनें",
        stopButton: "रोकें",

        // History Modal
        searchHistory: "खोज इतिहास",
        noHistoryYet: "अभी तक कोई खोज इतिहास नहीं",
        startSearching: "वैज्ञानिक शब्दों की खोज शुरू करें!",

        // Error Messages
        enterTerm: "कृपया एक वैज्ञानिक शब्द दर्ज करें।",
        generatingExplanation: "व्याख्या तैयार की जा रही है...",
        mayTakeTime: "इसमें 10-20 सेकंड लग सकते हैं।",
        errorHeading: "त्रुटि",
        connectionError: "बैकएंड से कनेक्ट नहीं हो सका।",
        details: "विवरण:",
        makeSureRunning: "सुनिश्चित करें कि 'main.py' पोर्ट 8000 पर चल रहा है।",

        // Login Page
        welcomeBack: "वापसी पर स्वागत है",
        loginSubtitle: "अपनी सीखने की यात्रा जारी रखने के लिए लॉगिन करें।",
        username: "उपयोगकर्ता नाम",
        enterUsername: "अपना उपयोगकर्ता नाम दर्ज करें",
        password: "पासवर्ड",
        enterPassword: "अपना पासवर्ड दर्ज करें",
        rememberMe: "मुझे याद रखें",
        forgotPassword: "पासवर्ड भूल गए?",
        forgotPasswordAlert: "पासवर्ड भूल गए सुविधा जल्द आ रही है!",
        loginButton: "लॉगिन",
        noAccount: "खाता नहीं है?",
        signUp: "साइन अप करें",

        // Register Page
        joinUs: "हमसे जुड़ें",
        registerSubtitle: "खोज शुरू करने के लिए एक खाता बनाएं।",
        fullName: "पूरा नाम",
        fullNamePlaceholder: "पूरा नाम",
        email: "ईमेल",
        emailPlaceholder: "ईमेल पता",
        createPassword: "पासवर्ड बनाएं",
        confirmPassword: "पासवर्ड की पुष्टि करें",
        confirmPasswordPlaceholder: "पासवर्ड की पुष्टि करें",
        registerButton: "रजिस्टर करें",
        alreadyHaveAccount: "पहले से खाता है?",
        login: "लॉगिन",

        // Password Strength
        weak: "कमजोर",
        medium: "मध्यम",
        strong: "मजबूत",

        // Auth Messages
        registrationSuccess: "पंजीकरण सफल! लॉगिन पर रीडायरेक्ट किया जा रहा है...",
        loginSuccess: "लॉगिन सफल! रीडायरेक्ट किया जा रहा है...",
        invalidCredentials: "अमान्य ईमेल या पासवर्ड",
        emailAlreadyRegistered: "ईमेल पहले से पंजीकृत है",
        passwordMismatch: "पासवर्ड मेल नहीं खाते",
        fillAllFields: "कृपया सभी फ़ील्ड भरें",

        // Language Selector
        language: "भाषा",
        english: "English",
        hindi: "हिंदी",

        // Feedback
        about: "हमारे बारे में",
        contact: "संपर्क",
        aboutUs: "हमारे बारे में",
        contactUs: "हमसे संपर्क करें",
        aboutContent: "Concept Clarity एक AI-संचालित शैक्षिक उपकरण है जिसे सभी के लिए वैज्ञानिक शब्दों को समझना आसान बनाने के लिए डिज़ाइन किया गया है।<br><br>हमारा मिशन:<br>1. जटिल वैज्ञानिक अवधारणाओं को सरल बनाना।<br>2. बहु-स्तरीय स्पष्टीकरण प्रदान करना (शुरुआती, मध्यम, उन्नत)।<br>3. दृश्य और श्रव्य सहायता के साथ सीखने को बढ़ाना।<br>4. शिक्षा को कई भाषाओं में सुलभ बनाना।<br>5. <b>प्रतिक्रिया:</b> हम आपके सुझावों को महत्व देते हैं! अपने विचार साझा करने के लिए <a href='#' onclick='openFeedbackModal(); return false;' style='color: #bb86fc;'>यहाँ क्लिक करें</a>।",
        contactContent: "प्रश्न या सुझाव हैं? हमसे संपर्क करें:<br><br>📧 ईमेल: support@conceptclarity.com<br>📞 फोन: +91 98765 43210<br>📍 स्थान: मुंबई, भारत",
        feedback: "प्रतिक्रिया",
        giveFeedback: "प्रतिक्रिया दें",
        rateExperience: "अपने अनुभव को रेट करें",
        yourRating: "आपकी रेटिंग",
        comments: "टिप्पणियाँ (वैकल्पिक)",
        commentsPlaceholder: "ऐप के बारे में अपने विचार साझा करें...",
        submitFeedback: "प्रतिक्रिया सबमिट करें",
        cancel: "रद्द करें",
        feedbackSuccess: "आपकी प्रतिक्रिया के लिए धन्यवाद!",
        feedbackError: "प्रतिक्रिया सबमिट करने में विफल। कृपया पुनः प्रयास करें।",
        pleaseRate: "कृपया एक रेटिंग चुनें",
        thankYouFeedback: "आपकी प्रतिक्रिया हमें बेहतर बनाने में मदद करती है!",
        usageLimitReached: "आप अपनी दैनिक मुफ्त उपयोग सीमा (2 खोज) तक पहुंच गए हैं। कृपया जारी रखने के लिए लॉगिन करें।",
        continueAsGuest: "अतिथि के रूप में जारी रखें",
        relatedVideos: "संबंधित वीडियो",
        watchOnYouTube: "YouTube पर देखें",
        takeQuiz: "प्रश्नोत्तरी",
        generatingQuiz: "प्रश्नोत्तरी बनाई जा रही है...",
        quizHeading: "अपने ज्ञान की परीक्षा लें",
        conceptTree: "अवधारणा वृक्ष",
        generatingTree: "वृक्ष बनाया जा रहा है...",
        submit: "जमा करें",
        correct: "सही!",
        wrong: "गलत!",
        score: "आपका स्कोर",
        excellent: "बहुत बढ़िया!",
        good: "अच्छा काम!",
        needsPractice: "अभ्यास करते रहें!",
        showJson: "JSON प्रारूप दिखाएं",
        hideJson: "JSON प्रारूप छिपाएं",

        // Settings
        settings: "सेटिंग्स",
        settings: "सेटिंग्स",
        account: "खाता",
        fullName: "पूरा नाम",
        learningPreferences: "सीखने की प्राथमिकताएं",
        defaultLevel: "डिफ़ॉल्ट स्तर",
        appearance: "उपस्थिति",
        theme: "थीम",
        darkTheme: "डार्क (डिफ़ॉल्ट)",
        lightTheme: "लाइट",
        audio: "ऑडियो",
        audioSpeed: "ऑडियो गति",
        autoPlay: "ऑटो-प्ले ऑडियो",
        done: "पूर्ण"
    }
};

// Get current language from localStorage or default to English
function getCurrentLanguage() {
    return localStorage.getItem('language') || 'en';
}

// Set language in localStorage
function setLanguage(lang) {
    localStorage.setItem('language', lang);
}

// Get translation for a key
function t(key) {
    const lang = getCurrentLanguage();
    return translations[lang][key] || translations['en'][key] || key;
}

// Update all elements with data-i18n attribute
function updatePageLanguage() {
    const lang = getCurrentLanguage();
    document.documentElement.lang = lang;

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = translations[lang][key];

        // Skip elements that have dynamic content (like user email)
        if (element.id === 'userEmail' || element.classList.contains('user-email')) {
            return; // Don't translate user email
        }

        if (translation) {
            // Check if it's a placeholder
            if (element.hasAttribute('placeholder')) {
                element.placeholder = translation;
            } else if (key === 'aboutContent' || key === 'contactContent') {
                element.innerHTML = translation;
            } else {
                element.textContent = translation;
            }
        }
    });

    // Update language selector to show current language
    const languageSelector = document.getElementById('languageSelector');
    if (languageSelector) {
        languageSelector.value = lang;
    }
}

// Change language
function changeLanguage(lang) {
    setLanguage(lang);
    updatePageLanguage();

    // Trigger custom event for other scripts to react to language change
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function () {
    updatePageLanguage();
});
