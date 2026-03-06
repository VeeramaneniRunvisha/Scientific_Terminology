// Track selected difficulty level
const API_URL = 'https://scientific-backend.onrender.com';
let selectedLevel = 'beginner'; // Default level

// Function to handle level selection
function selectLevel(level) {
    selectedLevel = level;

    // Update UI to show active level
    const cards = document.querySelectorAll('.level-card');
    cards.forEach(card => {
        if (card.dataset.level === level) {
            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    });
}

// Format raw model explanation into styled HTML sections
function formatExplanation(text) {
    if (!text) return '<p>No explanation available.</p>';

    // Section header patterns (English + Hindi)
    const sectionPatterns = [
        { key: 'definition', regex: /(?:definition|परिभाषा):/i },
        { key: 'advantage', regex: /(?:advantages?|लाभ):/i },
        { key: 'disadvantage', regex: /(?:disadvantages?|हानि):/i },
        { key: 'related', regex: /(?:related terms?|संबंधित शब्द):/i },
    ];

    const sectionLabels = {
        definition: { en: 'Definition', hi: 'परिभाषा' },
        advantage: { en: 'Advantage', hi: 'लाभ' },
        disadvantage: { en: 'Disadvantage', hi: 'हानि' },
        related: { en: 'Related Terms', hi: 'संबंधित शब्द' },
    };

    // Detect language
    const isHindi = /[\u0900-\u097F]/.test(text);
    const langKey = isHindi ? 'hi' : 'en';

    // Find all occurrences of all headers
    let matches = [];
    sectionPatterns.forEach(sp => {
        const globalRegex = new RegExp(sp.regex.source, 'gi');
        let match;
        while ((match = globalRegex.exec(text)) !== null) {
            matches.push({
                index: match.index,
                length: match[0].length,
                key: sp.key
            });
        }
    });

    // Sort matches by their position in the text
    matches.sort((a, b) => a.index - b.index);

    // CRITICAL FIX: Filter out matches that are inside other matches 
    // (e.g., 'advantage' being found inside 'disadvantage')
    let filteredMatches = [];
    for (let i = 0; i < matches.length; i++) {
        let isInside = false;
        for (let j = 0; j < matches.length; j++) {
            if (i === j) continue;
            // If match i is entirely contained within match j
            if (matches[i].index >= matches[j].index &&
                (matches[i].index + matches[i].length) <= (matches[j].index + matches[j].length) &&
                matches[i].length < matches[j].length) {
                isInside = true;
                break;
            }
        }
        if (!isInside) filteredMatches.push(matches[i]);
    }
    matches = filteredMatches;

    let sections = [];
    if (matches.length === 0) {
        // No headers found, treat entire text as definition
        sections.push({ key: 'definition', content: text.trim() });
    } else {
        // Handle text before the first match if it exists
        if (matches[0].index > 0) {
            const initialText = text.substring(0, matches[0].index).trim();
            if (initialText) {
                sections.push({ key: 'definition', content: initialText });
            }
        }

        // Extract content between matches
        for (let i = 0; i < matches.length; i++) {
            const start = matches[i].index + matches[i].length;
            const end = (i + 1 < matches.length) ? matches[i + 1].index : text.length;
            const content = text.substring(start, end).trim()
                .replace(/^\*\*/, '').replace(/\*\*$/, '') // Clean up markdown
                .replace(/\n+/g, ' ').trim(); // Flatten content spaces

            if (content) {
                sections.push({ key: matches[i].key, content: content });
            }
        }
    }

    // Build HTML
    let html = '';
    for (let sec of sections) {
        const label = sectionLabels[sec.key]?.[langKey] || sec.key;
        const content = sec.content.replace(/\*\*/g, '');

        if (sec.key === 'related') {
            const tags = content.split(',').map(t => t.trim()).filter(t => t);
            const tagHtml = tags.map(tag =>
                `<span style="display:inline-block; background:rgba(139,92,246,0.15); color:#c4b5fd; border:1px solid rgba(139,92,246,0.3); border-radius:20px; padding:3px 12px; margin:3px 4px 3px 0; font-size:0.85em;">${tag}</span>`
            ).join('');
            html += `
                <div style="margin-bottom: 20px;">
                    <div style="font-weight:700; color:#a78bfa; font-size:0.85em; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:8px;">${label}</div>
                    <div>${tagHtml}</div>
                </div>`;
        } else {
            html += `
                <div style="margin-bottom: 18px; padding: 15px; background: rgba(255,255,255,0.04); border-left: 4px solid rgba(139,92,246,0.5); border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <div style="font-weight:700; color:#a78bfa; font-size:0.85em; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:8px;">${label}</div>
                    <div style="line-height:1.7; color:#e2e8f0; font-size: 0.95rem;">${content}</div>
                </div>`;
        }
    }

    return html;
}

async function explainTerm() {

    const termInput = document.getElementById("termInput");
    const term = termInput.value.trim();
    const outputBox = document.getElementById("outputBox");

    // Input validation
    if (term === "") {
        outputBox.innerHTML = `<span class='error'>${t('enterTerm')}</span>`;
        return;
    }

    // Check for anonymous usage limit
    if (!localStorage.getItem('user')) {
        const today = new Date().toDateString();
        const lastUsageDate = localStorage.getItem('anonymousUsageDate');
        let usageCount = parseInt(localStorage.getItem('anonymousUsageCount'));

        // Reset count if it's a new day
        if (lastUsageDate !== today) {
            usageCount = 0;
            localStorage.setItem('anonymousUsageDate', today);
        }

        if (isNaN(usageCount)) usageCount = 0;

        if (usageCount >= 2) {
            window.location.href = "login.html?reason=limit";
            return;
        }
        localStorage.setItem('anonymousUsageCount', usageCount + 1);
        // Ensure date is set for first time users
        if (!lastUsageDate) localStorage.setItem('anonymousUsageDate', today);
    }

    // Show loading state with spinner
    outputBox.innerHTML = `
        <div class="loader-container">
            <div class="loader"></div>
            <p class="loading-text">${t('generatingExplanation')}<br><span style="font-size:0.8em; opacity:0.7">${t('mayTakeTime')}</span></p>
        </div>
    `;

    try {
        console.log("Sending request to backend for:", term, "at level:", selectedLevel);

        // Get user email from localStorage if logged in
        let userEmail = null;
        let userName = null;
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                const user = JSON.parse(userStr);
                userEmail = user.email;
                userName = user.name || "Guest";
                console.log("User logged in:", userEmail);
            } catch (e) {
                console.log("No user logged in");
            }
        }

        const response = await fetch(`${API_URL}/explain`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                term,
                level: selectedLevel,
                user_email: userEmail,  // Include user email if available
                language: getCurrentLanguage()  // Include selected language
            })
        });

        console.log("Response status:", response.status);
        const data = await response.json();

        if (response.ok) {
            // Parse the explanation to extract definition, advantages, and disadvantages
            const explanation = data.explanation;
            let definition = "";
            let advantages = [];
            let disadvantages = [];
            let relatedTerms = [];

            // Parse the explanation text to extract sections
            const lines = explanation.split('\n');

            let currentSection = "";
            let currentText = "";

            for (let line of lines) {
                const originalLine = line.trim();

                // Check for section headers on ORIGINAL line (before removing asterisks)
                // Definition: or परिभाषा:
                const isDefinition = originalLine.toLowerCase().startsWith('definition:') ||
                    originalLine.startsWith('परिभाषा:') ||
                    originalLine.toLowerCase().startsWith('**definition:**') ||
                    originalLine.startsWith('**परिभाषा:**');

                const isAdvantage = originalLine.toLowerCase().startsWith('advantage') ||
                    originalLine.startsWith('लाभ') ||
                    originalLine.toLowerCase().startsWith('**advantage') ||
                    originalLine.startsWith('**लाभ');

                const isDisadvantage = originalLine.toLowerCase().startsWith('disadvantage') ||
                    originalLine.startsWith('हानि') ||
                    originalLine.toLowerCase().startsWith('**disadvantage') ||
                    originalLine.startsWith('**हानि');

                const isRelatedTerms = originalLine.toLowerCase().startsWith('related terms') ||
                    originalLine.startsWith('संबंधित शब्द') ||
                    originalLine.toLowerCase().startsWith('**related terms') ||
                    originalLine.startsWith('**संबंधित शब्द');

                if (isDefinition) {
                    // Save previous section if exists
                    if (currentSection === "advantages" && currentText) {
                        advantages.push(currentText.trim());
                        currentText = "";
                    } else if (currentSection === "disadvantages" && currentText) {
                        disadvantages.push(currentText.trim());
                        currentText = "";
                    }

                    currentSection = "definition";
                    // Remove headers and asterisks
                    definition = originalLine.replace(/\*\*/g, '')
                        .replace(/^definition:\s*/i, '')
                        .replace(/^परिभाषा:\s*/i, '').trim();

                } else if (isAdvantage) {
                    // Save previous section
                    if (currentSection === "definition" && currentText) {
                        definition += " " + currentText.trim();
                        currentText = "";
                    } else if (currentSection === "disadvantages" && currentText) {
                        disadvantages.push(currentText.trim());
                        currentText = "";
                    }

                    currentSection = "advantages";
                    // Remove headers and asterisks
                    const advantageText = originalLine.replace(/\*\*/g, '')
                        .replace(/^advantages?:\s*/i, '')
                        .replace(/^लाभ:\s*/i, '').trim();
                    if (advantageText) {
                        currentText = advantageText;
                    }

                } else if (isDisadvantage) {
                    // Save previous advantage if exists
                    if (currentSection === "advantages" && currentText) {
                        advantages.push(currentText.trim());
                        currentText = "";
                    }

                    currentSection = "disadvantages";
                    // Remove headers and asterisks
                    const disadvantageText = originalLine.replace(/\*\*/g, '')
                        .replace(/^disadvantages?:\s*/i, '')
                        .replace(/^हानि:\s*/i, '').trim();
                    if (disadvantageText) {
                        currentText = disadvantageText;
                    }

                } else if (isRelatedTerms) {
                    // Save previous disadvantage if exists
                    if (currentSection === "disadvantages" && currentText) {
                        disadvantages.push(currentText.trim());
                        currentText = "";
                    }

                    currentSection = "relatedTerms";
                    // Remove headers and asterisks, then split by comma
                    const termsText = originalLine.replace(/\*\*/g, '')
                        .replace(/^related terms?:\s*/i, '')
                        .replace(/^संबंधित शब्द:\s*/i, '').trim();
                    if (termsText) {
                        relatedTerms = termsText.split(',').map(t => t.trim()).filter(t => t);
                    }

                } else if (originalLine) {
                    // Continue current section - remove asterisks from content
                    const cleanLine = originalLine.replace(/\*\*/g, '');

                    if (currentSection === "definition") {
                        definition += " " + cleanLine;
                    } else if (currentSection === "advantages" || currentSection === "disadvantages") {
                        if (currentText) {
                            currentText += " " + cleanLine;
                        } else {
                            currentText = cleanLine;
                        }
                    } else if (currentSection === "relatedTerms") {
                        // Handle multi-line related terms
                        const newTerms = cleanLine.split(',').map(t => t.trim()).filter(t => t);
                        relatedTerms = [...relatedTerms, ...newTerms];
                    }
                }
            }

            // Save the last section
            if (currentSection === "advantages" && currentText) {
                advantages.push(currentText.trim());
            } else if (currentSection === "disadvantages" && currentText) {
                disadvantages.push(currentText.trim());
            }

            // Clean up definition
            definition = definition.trim();

            // Fallback: if parsing failed, use the whole explanation
            if (!definition && advantages.length === 0 && disadvantages.length === 0) {
                definition = explanation;
            }

            // Create JSON format object
            const jsonData = {
                "term": term,
                "definition": definition || "No definition available",
                "advantages": advantages.length > 0 ? advantages : ["Not specified"],
                "disadvantages": disadvantages.length > 0 ? disadvantages : ["Not specified"],
                "related_terms": relatedTerms.length > 0 ? relatedTerms : ["Not specified"]
            };

            // Determine if user is logged in
            const isLoggedIn = localStorage.getItem('user') !== null;
            const audioControlsHtml = isLoggedIn ? `
                <div class="audio-controls" style="margin-top: 20px; display: flex; gap: 10px;">
                    <button onclick="speakText()" class="icon-btn" data-i18n="listenButton" title="Listen">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
                        ${t('listenButton')}
                    </button>
                    <button onclick="stopText()" class="icon-btn stop-btn" data-i18n="stopButton" title="Stop">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect></svg>
                        ${t('stopButton')}
                    </button>
                </div>` : '';

            // Save history for guest user
            if (!isLoggedIn) {
                const guestHistory = JSON.parse(localStorage.getItem('guestHistory') || '[]');
                const newEntry = {
                    term: term,
                    level: selectedLevel,
                    timestamp: new Date().toISOString()
                };
                // Add to beginning of array
                guestHistory.unshift(newEntry);
                // Limit to 10 items
                if (guestHistory.length > 10) guestHistory.pop();
                localStorage.setItem('guestHistory', JSON.stringify(guestHistory));
            }

            // Video handling with YouTube IFrame API
            const videoContainerId = 'video-player-container';
            let videoContent = '';

            // ONLY generate video and extra buttons if logged in
            if (isLoggedIn) {
                videoContent = `
                    <div class="video-container" style="margin-top: 20px; text-align: center;">
                        <h3 data-i18n="relatedVideos" style="margin-bottom: 10px;">Related Videos</h3>
                        <div id="${videoContainerId}"></div>
                        <div id="video-fallback" style="display: none;">
                            <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(term + ' explanation')}" target="_blank" class="youtube-btn">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                                </svg>
                                ${t('watchOnYouTube')}
                            </a>
                        </div>
                    </div>`;
            }

            let extraButtonsHtml = '';
            if (isLoggedIn) {
                extraButtonsHtml = `
                    <div class="action-buttons-container" style="margin-top: 20px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                        <button class="quiz-btn" onclick="generateQuiz('${term}', this)">
                            ${t('takeQuiz')}
                        </button>
                        <button class="tree-btn" onclick="generateConceptTree('${term}', this)">
                            ${t('conceptTree')}
                        </button>
                    </div>
                    <div id="quiz-container-${term}" class="quiz-container" style="display: none;"></div>
                    <div id="tree-container-${term}" class="tree-container" style="display: none;"></div>
                `;
            } else {
                extraButtonsHtml = `
                    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; min-height: 200px; text-align: center; color: #a0a0a0;">
                        <p style="margin-bottom: 10px; font-size: 1.1rem;">Login Required</p>
                        <p style="font-size: 0.9em;">Access Quiz, Concept Tree,<br>and Videos.</p>
                    </div>
                `;
            }

            outputBox.innerHTML = `
                <div class="explanation-layout">
                    <!-- Left Column: Explanation & Audio & JSON -->
                    <div class="explanation-main">
                        <h3 data-i18n="explanationHeading">${t('explanationHeading')}</h3>
                        <div id="explanationText">${formatExplanation(data.explanation)}</div>
                        ${audioControlsHtml}

                        <!-- JSON Display moved up or kept here -->
                         <div class="json-display">
                            <button id="toggleJsonBtn" onclick="toggleJson()" class="btn-secondary" style="margin-bottom: 15px; width: 100%;">
                                ${t('showJson')}
                            </button>
                            <div id="jsonOutput" style="display: none;">
                                <h3 data-i18n="jsonFormatHeading">${t('jsonFormatHeading')}</h3>
                                <pre class="json-code">${JSON.stringify(jsonData, null, 2)}</pre>
                            </div>
                        </div>
                    </div>

                    <!-- Right Column: Video & Buttons & Tree -->
                    <div class="explanation-sidebar">
                         ${videoContent}
                         ${extraButtonsHtml}
                    </div>
                </div>
            `;

            // Initialize player if videos exist
            if (data.video_ids && data.video_ids.length > 0) {
                initYouTubePlayer(data.video_ids);
            } else {
                document.getElementById('video-fallback').style.display = 'block';
                document.getElementById(videoContainerId).style.display = 'none';
            }

            // Check for Auto-play
            const settingsStr = localStorage.getItem('userSettings');
            if (settingsStr) {
                try {
                    const settings = JSON.parse(settingsStr);
                    if (settings.autoPlay) {
                        // Small delay to ensure text is ready
                        setTimeout(() => speakText(), 500);
                    }
                } catch (e) {
                    console.error("Error auto-playing:", e);
                }
            }
        } else {
            console.error("Backend error:", data);
            const errorMsg = typeof data.detail === 'string' ? data.detail :
                typeof data.detail === 'object' ? JSON.stringify(data.detail) :
                    "Could not get explanation.";
            outputBox.innerHTML = `<span class='error'>Error: ${errorMsg}</span>`;
        }

    } catch (error) {
        console.error("Fetch error:", error);
        const errorDetails = error.message || JSON.stringify(error);
        outputBox.innerHTML = `
            <h3 data-i18n="errorHeading">${t('errorHeading')}</h3>
            <p data-i18n="connectionError">${t('connectionError')}</p> 
            <p style="font-size: 0.9em; color: #666;"><span data-i18n="details">${t('details')}</span> ${errorDetails}</p>
            <p style="font-size: 0.8em;" data-i18n="makeSureRunning">${t('makeSureRunning')}</p>
        `;
    }
}

// Voice: Speech-to-Text
function startVoiceSearch() {
    const micBtn = document.getElementById("micBtn");

    if (!('webkitSpeechRecognition' in window)) {
        alert("Web Speech API not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    const currentLang = getCurrentLanguage();
    recognition.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();
    micBtn.classList.add("listening");

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById("termInput").value = transcript;
        micBtn.classList.remove("listening");
        explainTerm(); // Auto-submit
    };

    recognition.onerror = (event) => {
        console.error("Speech error", event.error);
        micBtn.classList.remove("listening");
    };

    recognition.onend = () => {
        micBtn.classList.remove("listening");
    };
}



// Function to load chat history from backend
async function loadChatHistory(userEmail = null, limit = 50) {
    try {
        // If no email provided, try to get from localStorage
        if (!userEmail) {
            const userStr = localStorage.getItem('user');
            if (userStr) {
                try {
                    const user = JSON.parse(userStr);
                    userEmail = user.email;
                } catch (e) {
                    // User not logged in
                }
            }
        }

        // If still no userEmail, assume guest user and return local history
        if (!userEmail) {
            const guestHistory = JSON.parse(localStorage.getItem('guestHistory') || '[]');
            console.log(`Loaded ${guestHistory.length} guest history entries`);
            return guestHistory;
        }

        let url = `${API_URL}/chat/history?limit=${limit}`;
        if (userEmail) {
            url += `&user_email=${encodeURIComponent(userEmail)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {
            console.log(`Loaded ${data.count} chat history entries:`, data.history);
            return data.history;
        } else {
            console.error("Error loading chat history:", data);
            return [];
        }
    } catch (error) {
        console.error("Error fetching chat history:", error);
        return [];
    }
}

// Toggle history modal
function toggleHistory() {
    const modal = document.getElementById('historyModal');
    modal.classList.toggle('active');

    if (modal.classList.contains('active')) {
        loadAndDisplayHistory();
    }
}

// Load and display history in the modal
async function loadAndDisplayHistory() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '<p style="text-align: center; color: #666;">Loading...</p>';

    const history = await loadChatHistory();

    if (history.length === 0) {
        historyList.innerHTML = `
            <div class="history-empty">
                <p style="font-size: 1.2rem; margin-bottom: 10px;">📭</p>
                <p data-i18n="noHistoryYet">${t('noHistoryYet')}</p>
                <p style="font-size: 0.85rem; margin-top: 5px;" data-i18n="startSearching">${t('startSearching')}</p>
            </div>
        `;
        return;
    }

    // Display history items
    historyList.innerHTML = history.map(item => {
        const date = new Date(item.timestamp);
        const formattedDate = date.toLocaleDateString('en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
        const formattedTime = date.toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        });

        return `
            <div class="history-item" onclick="searchFromHistory('${item.term}', '${item.level}')">
                <div class="history-item-term">${item.term}</div>
                <div class="history-item-meta">
                    <span class="history-item-date">
                        📅 ${formattedDate} ${formattedTime}
                    </span>
                    <span class="history-item-level">${item.level}</span>
                </div>
            </div>
        `;
    }).join('');
}

// Search from history item
function searchFromHistory(term, level) {
    // Close the modal
    document.getElementById('historyModal').classList.remove('active');

    // Set the term and level
    document.getElementById('termInput').value = term;
    selectLevel(level);

    // Trigger the search
    explainTerm();
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById('historyModal');
    if (event.target === modal) {
        modal.classList.remove('active');
    }
}

// Text-to-Speech functionality
function speakText() {
    const text = document.getElementById('explanationText').textContent;
    if (!text) return;

    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    // Set language based on current app language
    const currentLang = getCurrentLanguage();
    utterance.lang = currentLang === 'hi' ? 'hi-IN' : 'en-US';

    // Get speed from settings
    let speed = 1.0;
    const settingsStr = localStorage.getItem('userSettings');
    if (settingsStr) {
        try {
            const settings = JSON.parse(settingsStr);
            if (settings.audioSpeed) {
                speed = parseFloat(settings.audioSpeed);
            }
        } catch (e) {
            console.error("Error parsing settings for audio speed:", e);
        }
    }

    // Set voice parameters
    utterance.rate = speed;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    // Try to find a voice that matches the language
    const voices = window.speechSynthesis.getVoices();
    const matchingVoice = voices.find(voice => voice.lang.startsWith(currentLang === 'hi' ? 'hi' : 'en'));
    if (matchingVoice) {
        utterance.voice = matchingVoice;
    }

    window.speechSynthesis.speak(utterance);
}

function stopText() {
    window.speechSynthesis.cancel();
}

// Load voices when they become available
window.speechSynthesis.onvoiceschanged = function () {
    window.speechSynthesis.getVoices();
};

// Profile Menu Functions
let selectedRating = 0;

function toggleProfileMenu() {
    const menu = document.getElementById('profileMenu');
    const isActive = menu.classList.toggle('active');
    console.log('Profile menu toggled:', isActive ? 'OPEN' : 'CLOSED');

    // Update email in dropdown menu
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            document.getElementById('profileMenuEmail').textContent = user.email;
        } catch (e) {
            document.getElementById('profileMenuEmail').textContent = 'Unknown User';
        }
    }
}

// Close profile menu when clicking outside
document.addEventListener('click', function (event) {
    const profileMenu = document.getElementById('profileMenu');
    const userProfile = document.querySelector('.user-profile');

    if (profileMenu && !userProfile.contains(event.target)) {
        profileMenu.classList.remove('active');
    }
});

// Feedback Modal Functions
function openFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.classList.add('active');

    // Close profile menu
    document.getElementById('profileMenu').classList.remove('active');

    // Reset form
    selectedRating = 0;
    document.getElementById('feedbackComment').value = '';
    document.getElementById('charCount').textContent = '0';
    updateStarDisplay();

    // Update placeholder text based on current language
    const currentLang = getCurrentLanguage();
    const placeholder = translations[currentLang].commentsPlaceholder;
    document.getElementById('feedbackComment').placeholder = placeholder;
}

function closeFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.classList.remove('active');
    selectedRating = 0;
    updateStarDisplay();
}

// About Modal Functions
function openAboutModal() {
    const modal = document.getElementById('aboutModal');
    modal.classList.add('active');
    document.getElementById('profileMenu').classList.remove('active');
}

function closeAboutModal() {
    document.getElementById('aboutModal').classList.remove('active');
}

// Contact Modal Functions
function openContactModal() {
    const modal = document.getElementById('contactModal');
    modal.classList.add('active');
    document.getElementById('profileMenu').classList.remove('active');
}

function closeContactModal() {
    document.getElementById('contactModal').classList.remove('active');
}

// Star Rating Interaction
document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');

    stars.forEach(star => {
        // Hover effect
        star.addEventListener('mouseenter', function () {
            const rating = parseInt(this.getAttribute('data-rating'));
            highlightStars(rating);
        });

        // Click to select
        star.addEventListener('click', function () {
            selectedRating = parseInt(this.getAttribute('data-rating'));
            updateStarDisplay();
        });
    });

    // Reset on mouse leave
    const starRating = document.getElementById('starRating');
    if (starRating) {
        starRating.addEventListener('mouseleave', function () {
            updateStarDisplay();
        });
    }

    // Character count for comment
    const commentBox = document.getElementById('feedbackComment');
    if (commentBox) {
        commentBox.addEventListener('input', function () {
            document.getElementById('charCount').textContent = this.value.length;
        });
    }
});

function highlightStars(rating) {
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('highlighted');
        } else {
            star.classList.remove('highlighted');
        }
    });
}

function updateStarDisplay() {
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < selectedRating) {
            star.classList.add('selected');
            star.classList.remove('highlighted');
        } else {
            star.classList.remove('selected', 'highlighted');
        }
    });

    // Update rating text
    const ratingText = document.getElementById('ratingText');
    if (selectedRating > 0) {
        const ratingLabels = {
            1: '⭐ Poor',
            2: '⭐⭐ Fair',
            3: '⭐⭐⭐ Good',
            4: '⭐⭐⭐⭐ Very Good',
            5: '⭐⭐⭐⭐⭐ Excellent'
        };
        ratingText.textContent = ratingLabels[selectedRating];
        ratingText.style.display = 'block';
    } else {
        ratingText.style.display = 'none';
    }
}

// Submit Feedback
async function submitFeedback() {
    const currentLang = getCurrentLanguage();

    // Validation
    if (selectedRating === 0) {
        alert(translations[currentLang].pleaseRate);
        return;
    }

    const comment = document.getElementById('feedbackComment').value.trim();

    // Get user email
    const userStr = localStorage.getItem('user');
    let userEmail = 'guest@example.com';
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            userEmail = user.email;
        } catch (e) {
            console.error('Error parsing user data:', e);
        }
    }

    const feedbackData = {
        user_email: userEmail,
        rating: selectedRating,
        comment: comment || null
    };

    try {
        const response = await fetch(`${API_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(feedbackData)
        });

        const data = await response.json();

        if (response.ok) {
            alert(translations[currentLang].feedbackSuccess + '\n' + translations[currentLang].thankYouFeedback);
            closeFeedbackModal();
        } else {
            alert(translations[currentLang].feedbackError + '\n' + (data.detail || ''));
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);

        try {
            const response = await fetch(`${API_URL}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(feedbackData)
            });

            const data = await response.json();

            if (response.ok) {
                alert(translations[currentLang].feedbackSuccess + '\n' + translations[currentLang].thankYouFeedback);
                closeFeedbackModal();
            } else {
                alert(translations[currentLang].feedbackError + '\n' + (data.detail || ''));
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
            alert(translations[currentLang].feedbackError);
        }
    }
}

// Tree Generation Functions
async function generateTree() {
    const term = document.getElementById('termInput').value;
    if (!term) return;

    // Track Tree Usage
    const user = JSON.parse(localStorage.getItem('user'));
    const userEmail = user ? user.email : 'guest';

    try {
        fetch(`${API_URL}/track/tree`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_email: userEmail, term: term })
        });
    } catch (e) {
        console.error("Tracking error:", e);
    }

    const treeContainer = document.getElementById('treeContainer');
    const treeModal = document.getElementById('treeModal');

    // Show loading
    treeContainer.innerHTML = '<div style="color:white; text-align:center; padding:20px;">Generating Concept Tree...</div>';
    treeModal.style.display = 'flex';
}

// Close modal when clicking outside
window.addEventListener('click', function (event) {
    const feedbackModal = document.getElementById('feedbackModal');
    const aboutModal = document.getElementById('aboutModal');
    const contactModal = document.getElementById('contactModal');

    if (event.target === feedbackModal) {
        closeFeedbackModal();
    }
    if (event.target === aboutModal) {
        closeAboutModal();
    }
    if (event.target === contactModal) {
        closeContactModal();
    }

    const settingsModal = document.getElementById('settingsModal');
    if (event.target === settingsModal) {
        closeSettingsModal();
    }
});

// Quiz Functions
async function generateQuiz(term, btnElement) {
    const currentLang = getCurrentLanguage();
    const container = document.getElementById(`quiz-container-${term}`);
    const button = btnElement;

    // Hide tree container if open
    const treeContainer = document.getElementById(`tree-container-${term}`);
    if (treeContainer) treeContainer.style.display = 'none';

    // Show loading state
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `<span class="spinner"></span> ${t('generatingQuiz')}`;
    container.style.display = 'block';
    container.innerHTML = `<p style="text-align:center; color: #ddd;">${t('generatingQuiz')}</p>`;

    try {
        const response = await fetch(`${API_URL}/quiz`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ term: term, language: currentLang })
        });

        const data = await response.json();

        if (response.ok) {
            let quizData = [];
            try {
                quizData = JSON.parse(data.quiz);
            } catch (e) {
                console.error("Failed to parse quiz JSON", e);
            }

            if (quizData.length > 0) {
                renderQuiz(term, quizData);
                button.disabled = false;
                button.innerHTML = t('takeQuiz');
            } else {
                container.innerHTML = `<p style="text-align:center; color: #ff6b6b;">Failed to generate quiz. Please try again.</p>`;
                button.disabled = false;
                button.innerHTML = t('takeQuiz');
            }
        } else {
            throw new Error(data.detail);
        }
    } catch (error) {
        console.error("Error generating quiz:", error);
        container.innerHTML = `<p style="text-align:center; color: #ff6b6b;">Error: ${error.message}</p>`;
        button.disabled = false;
        button.innerHTML = t('takeQuiz');
    }
}

function renderQuiz(term, questions) {
    const container = document.getElementById(`quiz-container-${term}`);
    const optionLabelLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    const formatOptionText = (optionText, optionIndex) => {
        const label = optionLabelLetters[optionIndex] || `${optionIndex + 1}`;
        // Remove only explicit option prefixes like "A. ", "B) ", "(C) ", "1. "
        const cleanedText = String(optionText)
            .replace(/^\s*(?:\(?[A-Da-d]\)?[\.\):\-]\s+|\(?[1-4]\)?[\.\):\-]\s+)/, '')
            .trim();
        return `${label}. ${cleanedText}`;
    };

    let html = `<h3 style="text-align:center; margin-bottom:20px;">${t('quizHeading')}</h3>`;

    questions.forEach((q, index) => {
        html += `
            <div class="quiz-question" id="q-${index}">
                <div class="question-text">${index + 1}. ${q.question}</div>
                <div class="options-grid">
                    ${q.options.map((opt, optIndex) => `
                        <div class="quiz-option" onclick="checkAnswer(${index}, ${optIndex}, ${q.correct_index}, this)">
                            ${formatOptionText(opt, optIndex)}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });

    html += `<div id="quiz-result-${term}" class="quiz-result" style="display:none;"></div>`;
    container.innerHTML = html;

    // Store quiz state
    window.currentQuiz = {
        term: term,
        total: questions.length,
        answered: 0,
        score: 0
    };
}

function checkAnswer(qIndex, optIndex, correctIndex, element) {
    // Prevent re-answering
    const questionDiv = document.getElementById(`q-${qIndex}`);
    if (questionDiv.classList.contains('answered')) return;
    questionDiv.classList.add('answered');

    const options = questionDiv.querySelectorAll('.quiz-option');
    const correctOption = options[correctIndex];

    if (optIndex === correctIndex) {
        element.classList.add('correct');
        element.innerHTML += ` <span style="float:right;">✓</span>`;
        window.currentQuiz.score++;
    } else {
        element.classList.add('wrong');
        element.innerHTML += ` <span style="float:right;">✗</span>`;
        correctOption.classList.add('correct');
        correctOption.innerHTML += ` <span style="float:right;">✓</span>`;
    }

    window.currentQuiz.answered++;

    // Check if finished
    if (window.currentQuiz.answered === window.currentQuiz.total) {
        showQuizResult(window.currentQuiz);
    }
}

async function showQuizResult(quizState) {
    const resultDiv = document.getElementById(`quiz-result-${quizState.term}`);
    const score = quizState.score;
    const total = quizState.total;
    const percentage = Math.round((score / total) * 100);

    // Track Quiz Result
    let userEmail = 'guest';
    try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            const user = JSON.parse(userStr);
            if (user && user.email) userEmail = user.email;
        }
    } catch (e) {
        console.warn("Error parsing user from localStorage:", e);
    }

    const term = document.getElementById('termInput').value || 'General';

    try {
        console.log("Tracking quiz result...", { userEmail, term, score });
        const response = await fetch(`${API_URL}/track/quiz`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_email: userEmail,
                term: term,
                score: quizState.score
            })
        });

        if (!response.ok) {
            const errText = await response.text();
            console.error("Failed to track quiz:", response.status, errText);
        } else {
            console.log("Quiz result tracked successfully");
        }
    } catch (e) {
        console.error("Tracking error:", e);
    }

    const resultEmoji = percentage >= 80 ? '🏆' : (percentage >= 50 ? '👍' : '📚');
    let remark = t('needsPractice');
    if (percentage === 100) remark = t('excellent');
    else if (percentage >= 60) remark = t('good');

    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <div class="score-display">${t('score')}: ${score}/${total}</div>
        <div class="remark-text">${remark}</div>
    `;

    // Add confetti effect if excellent
    if (percentage === 100) {
        // Simple confetti if we had a library, but text is fine for now
    }
}

function showFallback() {
    const fallback = document.getElementById('video-fallback');
    const container = document.getElementById('video-player-container');
    if (fallback) fallback.style.display = 'block';
    if (container) container.style.display = 'none';
}

function playVideo(videoId) {
    const term = document.getElementById('termInput').value || 'Unknown';

    // Track Video
    const user = JSON.parse(localStorage.getItem('user'));
    const userEmail = user ? user.email : 'guest';

    try {
        fetch(`${API_URL}/track/video`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_email: userEmail,
                term: term,
                video_id: videoId
            })
        });
    } catch (e) {
        console.log("Tracking error:", e);
    }

    createPlayer(videoId);
}

// YouTube IFrame API Support
let player;
let videoIdsQueue = [];

function initYouTubePlayer(videoIds) {
    videoIdsQueue = videoIds;

    // Check if API is already loaded
    if (window.YT && window.YT.Player) {
        createPlayer(videoIdsQueue[0]);
    } else {
        // Load API if not loaded
        if (!document.querySelector('script[src*="youtube.com/iframe_api"]')) {
            const tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            const firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        }
    }
}

// Global callback for YouTube API
window.onYouTubeIframeAPIReady = function () {
    if (videoIdsQueue.length > 0) {
        createPlayer(videoIdsQueue[0]);
    }
};

function createPlayer(videoId) {
    // If player instance exists, destroy it first or load new video
    if (player && typeof player.destroy === 'function') {
        try {
            player.destroy();
        } catch (e) { console.error("Error destroying player:", e); }
        player = null;
    }

    // Clear container content just in case
    const container = document.getElementById('video-player-container');
    if (container) container.innerHTML = '';

    try {
        console.log("Initializing player with ID:", videoId);
        player = new YT.Player('video-player-container', {
            height: '300',
            width: '100%',
            videoId: videoId,
            playerVars: {
                'playsinline': 1,
                'rel': 0,
                'origin': window.location.origin
            },
            events: {
                'onError': onPlayerError,
                'onReady': onPlayerReady
            }
        });
    } catch (e) {
        console.error("Error creating player:", e);
        showFallback();
    }
}

function onPlayerReady(event) {
    // Player ready
    console.log("Player ready");

    // Track Video View when player is ready
    const user = JSON.parse(localStorage.getItem('user'));
    const userEmail = user ? user.email : 'guest';
    const term = document.getElementById('termInput').value || 'Unknown';
    const videoId = videoIdsQueue[0]; // The current video ID

    if (videoId) {
        try {
            fetch(`${API_URL}/track/video`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_email: userEmail,
                    term: term,
                    video_id: videoId
                })
            });
            console.log("Tracked video view for:", videoId);
        } catch (e) {
            console.log("Tracking error:", e);
        }
    }
}

function onPlayerError(event) {
    console.log("Player error:", event.data);
    // Remove failed ID from queue
    videoIdsQueue.shift();

    if (videoIdsQueue.length > 0) {
        // Try next video
        console.log("Trying next video:", videoIdsQueue[0]);
        setTimeout(() => createPlayer(videoIdsQueue[0]), 100);
    } else {
        // All videos failed, show fallback
        const modal = document.getElementById('videoModal');
        if (modal) modal.style.display = 'flex';
    }
}

// Concept Tree Functions
async function generateConceptTree(term, btnElement) {
    const container = document.getElementById(`tree-container-${term}`);
    const button = btnElement;

    // Track Tree Usage
    const user = JSON.parse(localStorage.getItem('user'));
    const userEmail = user ? user.email : 'guest';

    try {
        fetch(`${API_URL}/track/tree`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_email: userEmail, term: term })
        });
    } catch (e) {
        console.error("Tracking error:", e);
    }

    // Hide quiz container if open
    const quizContainer = document.getElementById(`quiz-container-${term}`);
    if (quizContainer) quizContainer.style.display = 'none';

    // Show loading state
    if (button) {
        button.disabled = true;
        button.innerHTML = `<span class="spinner"></span> ${t('generatingTree')}`;
    }

    container.style.display = 'block';
    container.innerHTML = `<p style="text-align:center; color: #ddd;">${t('generatingTree')}</p>`;

    try {
        const currentLang = getCurrentLanguage();
        const response = await fetch(`${API_URL}/concept_tree`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ term: term, language: currentLang })
        });

        const data = await response.json();

        if (response.ok) {
            container.innerHTML = `<pre class="tree-display">${data.tree}</pre>`;
            if (button) {
                button.disabled = false;
                button.innerHTML = t('conceptTree');
            }
        } else {
            throw new Error(data.detail);
        }
    } catch (error) {
        console.error("Error generating tree:", error);
        container.innerHTML = `<p style="text-align:center; color: #ff6b6b;">Error: ${error.message}</p>`;
        if (button) {
            button.disabled = false;
            button.innerHTML = t('conceptTree');
        }
    }
}

// Toggle JSON Display
function toggleJson() {
    const jsonOutput = document.getElementById('jsonOutput');
    const btn = document.getElementById('toggleJsonBtn');

    if (jsonOutput.style.display === 'none') {
        jsonOutput.style.display = 'block';
        btn.innerHTML = t('hideJson');
    } else {
        jsonOutput.style.display = 'none';
        btn.innerHTML = t('showJson');
    }
}

// Settings Modal Functions
function openSettingsModal() {
    const profileMenu = document.getElementById('profileMenu');
    if (profileMenu) profileMenu.classList.remove('active');

    const modal = document.getElementById('settingsModal');
    if (modal) {
        modal.style.display = 'flex';
        loadSettings();
    }
}

function closeSettingsModal() {
    const modal = document.getElementById('settingsModal');
    if (modal) modal.style.display = 'none';
}

function saveSettings() {
    const settings = {
        defaultLevel: document.getElementById('defaultLevelSelect').value,
        audioSpeed: document.getElementById('audioSpeedRange').value,
        autoPlay: document.getElementById('autoPlayCheckbox').checked,
        language: document.getElementById('settingsLanguageSelect').value
    };

    localStorage.setItem('userSettings', JSON.stringify(settings));
    applySettings(settings);

    // Provide feedback
    const btn = document.querySelector('#settingsModal .btn-primary');
    if (btn) {
        const originalText = btn.getAttribute('data-original-text') || t('done');
        // Store original text if not already stored
        if (!btn.getAttribute('data-original-text')) {
            btn.setAttribute('data-original-text', btn.innerText);
        }

        btn.innerText = t('saved') || 'Saved!';
        setTimeout(() => {
            btn.innerText = originalText;
            // distinct change: do NOT close modal here
        }, 800);
    }
}

function toggleChangePassword() {
    const form = document.getElementById('changePasswordForm');
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

async function updatePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;

    if (!currentPassword || !newPassword) {
        alert(t('fillAllFields') || "Please fill all fields");
        return;
    }

    // Get user email
    let userEmail = null;
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            userEmail = user.email;
        } catch (e) {
            console.error(e);
        }
    }

    if (!userEmail) {
        alert("You must be logged in to change password.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/change-password`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: userEmail,
                old_password: currentPassword,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert(t('passwordUpdated') || "Password updated successfully");
            // clear fields and hide form
            document.getElementById('currentPassword').value = '';
            document.getElementById('newPassword').value = '';
            toggleChangePassword();
        } else {
            alert(data.detail || "Failed to update password");
        }
    } catch (error) {
        console.error("Error updating password:", error);
        alert("An error occurred. Please try again.");
    }
}

function loadSettings() {
    // Display User Info
    const userStr = localStorage.getItem('user');
    const emailField = document.getElementById('settingsEmail');
    const nameField = document.getElementById('settingsName');

    if (userStr) {
        try {
            const user = JSON.parse(userStr);
            if (emailField) emailField.value = user.email;
            if (nameField) nameField.value = user.name || t('guest');
        } catch (e) {
            if (emailField) emailField.value = "Guest";
            if (nameField) nameField.value = t('guest');
        }
    } else {
        if (emailField) emailField.value = "Guest";
        if (nameField) nameField.value = t('guest');
    }

    const settingsStr = localStorage.getItem('userSettings');
    if (settingsStr) {
        try {
            const settings = JSON.parse(settingsStr);

            if (settings.defaultLevel && document.getElementById('defaultLevelSelect'))
                document.getElementById('defaultLevelSelect').value = settings.defaultLevel;

            if (settings.audioSpeed && document.getElementById('audioSpeedRange')) {
                document.getElementById('audioSpeedRange').value = settings.audioSpeed;
                document.getElementById('audioSpeedValue').innerText = settings.audioSpeed + 'x';
            }

            if (settings.autoPlay !== undefined && document.getElementById('autoPlayCheckbox'))
                document.getElementById('autoPlayCheckbox').checked = settings.autoPlay;

            if (settings.language && document.getElementById('settingsLanguageSelect'))
                document.getElementById('settingsLanguageSelect').value = settings.language;
        } catch (e) {
            console.error("Error loading settings:", e);
        }
    } else {
        // Set defaults based on current state
        if (document.getElementById('settingsLanguageSelect'))
            document.getElementById('settingsLanguageSelect').value = getCurrentLanguage();
    }
}

function applySettings(settings) {
    if (!settings) return;

    if (settings.defaultLevel) {
        selectLevel(settings.defaultLevel);
    }

    if (settings.language && settings.language !== getCurrentLanguage()) {
        changeLanguage(settings.language);
    }
}

// Initialize settings on load
window.addEventListener('DOMContentLoaded', () => {
    const settingsStr = localStorage.getItem('userSettings');
    if (settingsStr) {
        try {
            applySettings(JSON.parse(settingsStr));
        } catch (e) {
            console.error(e);
        }
    }

    // Toggle Login/Logout Buttons
    const user = localStorage.getItem('user');
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    if (user) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }
});
