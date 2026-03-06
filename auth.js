const API_URL = 'https://scientific-backend.onrender.com';

// Global Toggle Password Function
function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

function validatePasswordRules(password) {
    return {
        hasMinLength: password.length >= 8,
        hasUppercase: /[A-Z]/.test(password),
        hasLowercase: /[a-z]/.test(password),
        hasDigit: /[0-9]/.test(password),
        hasSpecial: /[^A-Za-z0-9]/.test(password)
    };
}

function isPasswordValid(password) {
    const checks = validatePasswordRules(password);
    return checks.hasMinLength && checks.hasUppercase && checks.hasLowercase && checks.hasDigit && checks.hasSpecial;
}

function getMissingPasswordRequirements(password) {
    const checks = validatePasswordRules(password);
    const missing = [];

    if (!checks.hasMinLength) missing.push("Minimum 8 characters required.");
    if (!checks.hasUppercase) missing.push("Uppercase letter is missing.");
    if (!checks.hasLowercase) missing.push("Lowercase letter is missing.");
    if (!checks.hasDigit) missing.push("Number is missing.");
    if (!checks.hasSpecial) missing.push("Special character is missing.");

    return missing;
}

function getPasswordFeedbackHtml(password) {
    if (!password) {
        return "";
    }

    const missing = getMissingPasswordRequirements(password);
    if (missing.length === 0) {
        return `<span style="color:#55efc4; font-size:0.8rem;">Password meets all requirements.</span>`;
    }

    return `<span style="color:#ff7675; font-size:0.8rem;">${missing.join("<br>")}</span>`;
}

// REGISTER (Frontend only)
async function register() {
    const name = document.getElementById("regName").value.trim();
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPassword").value.trim();
    const confirmPassword = document.getElementById("regConfirmPassword").value.trim();
    const msg = document.getElementById("registerMsg");

    // Clear previous messages
    msg.innerHTML = "";
    msg.className = "";

    // 1. Required Field Check
    if (name === "" && email === "" && password === "" && confirmPassword === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }
    if (name === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }
    if (email === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }
    if (password === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }
    if (confirmPassword === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }

    // 2. Email Format Validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }

    // 3. Password Match Check
    if (password !== confirmPassword) {
        msg.innerHTML = `<p class='error'>${t('passwordMismatch')}</p>`;
        return;
    }

    // 4. Password Rules Validation
    if (!isPasswordValid(password)) {
        msg.innerHTML = `<p class='error'>${getMissingPasswordRequirements(password).join(" ")}</p>`;
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            msg.innerHTML = `<p class='success'>${t('registrationSuccess')}</p>`;
            // Optional: Redirect after delay
            setTimeout(() => window.location.href = "login.html", 1500);
        } else {
            const errorMsg = data.detail === "Email already registered" ? t('emailAlreadyRegistered') : data.detail;
            msg.innerHTML = `<p class='error'>${errorMsg || t('fillAllFields')}</p>`;
        }
    } catch (error) {
        console.error("Register Error:", error);
        msg.innerHTML = `<p class='error'>Connection Error: ${error.message}</p>`;
    }
}

// Password Strength Meter
function checkStrength() {
    const password = document.getElementById("regPassword").value;
    const strengthMeter = document.getElementById("passwordStrength");

    if (!strengthMeter) {
        return;
    }

    strengthMeter.innerHTML = getPasswordFeedbackHtml(password);
}


// LOGIN (Frontend only)
async function login() {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();
    const msg = document.getElementById("loginMsg");
    const rememberMe = document.getElementById("rememberMe").checked;

    if (email === "" && password === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }
    if (email === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }
    if (password === "") {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Store user info
            localStorage.setItem("user", JSON.stringify(data.user));
            if (data.access_token) localStorage.setItem("token", data.access_token);

            if (rememberMe) {
                localStorage.setItem("rememberedEmail", email);
            } else {
                localStorage.removeItem("rememberedEmail");
            }

            // Check for Admin Role
            if (data.user.role === 'admin') {
                msg.innerHTML = `<p class='success'>Admin Login Successful!</p>`;
                setTimeout(() => window.location.href = "admin.html", 1000);
            } else {
                msg.innerHTML = `<p class='success'>${t('loginSuccess')}</p>`;
                setTimeout(() => {
                    window.location.href = "index.html";
                }, 1000);
            }
        } else {
            msg.innerHTML = `<p class='error'>${data.detail || t('invalidCredentials')}</p>`;
        }
    } catch (error) {
        console.error("Login Error:", error);
        msg.innerHTML = `<p class='error'>Connection Error: ${error.message}</p>`;
    }
}

// FORGOT PASSWORD
async function handleForgotPassword() {
    const email = document.getElementById("forgotEmail").value.trim();
    const msg = document.getElementById("forgotMsg");

    if (!email) {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }

    try {
        const response = await fetch(`${API_URL}/forgot-password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (response.ok) {
            msg.innerHTML = `<p class='success'>User verified. Redirecting...</p>`;
            // In a real app, you'd send an email. For this demo, we redirect to reset page with email in URL.
            setTimeout(() => {
                window.location.href = `reset_password.html?email=${encodeURIComponent(email)}`;
            }, 1500);
        } else {
            msg.innerHTML = `<p class='error'>${data.detail || "User not found"}</p>`;
        }
    } catch (error) {
        console.error("Forgot Password Error:", error);
        msg.innerHTML = `<p class='error'>Connection Error: ${error.message}</p>`;
    }
}

// RESET PASSWORD
async function handleResetPassword() {
    const email = document.getElementById("resetEmail").value;
    const newPassword = document.getElementById("newPassword").value.trim();
    const confirmPassword = document.getElementById("confirmPassword").value.trim();
    const msg = document.getElementById("resetMsg");

    if (!newPassword || !confirmPassword) {
        msg.innerHTML = `<p class='error'>${t('fillAllFields')}</p>`;
        return;
    }

    if (!isPasswordValid(newPassword)) {
        msg.innerHTML = `<p class='error'>${getMissingPasswordRequirements(newPassword).join(" ")}</p>`;
        return;
    }

    if (newPassword !== confirmPassword) {
        msg.innerHTML = `<p class='error'>${t('passwordMismatch')}</p>`;
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reset-password`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, new_password: newPassword })
        });

        const data = await response.json();

        if (response.ok) {
            msg.innerHTML = `<p class='success'>${t('passwordUpdated')}</p>`;
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);
        } else {
            msg.innerHTML = `<p class='error'>${data.detail || "Error updating password"}</p>`;
        }
    } catch (error) {
        console.error("Reset Password Error:", error);
        msg.innerHTML = `<p class='error'>Connection Error: ${error.message}</p>`;
    }
}

function setupPasswordValidationFeedback() {
    const registerPasswordInput = document.getElementById("regPassword");
    if (registerPasswordInput) {
        registerPasswordInput.addEventListener("input", checkStrength);
        checkStrength();
    }

    const resetPasswordInput = document.getElementById("newPassword");
    const resetPasswordFeedback = document.getElementById("resetPasswordFeedback");
    if (resetPasswordInput && resetPasswordFeedback) {
        resetPasswordInput.addEventListener("input", function () {
            resetPasswordFeedback.innerHTML = getPasswordFeedbackHtml(resetPasswordInput.value);
        });
        resetPasswordFeedback.innerHTML = getPasswordFeedbackHtml(resetPasswordInput.value);
    }
}

document.addEventListener("DOMContentLoaded", setupPasswordValidationFeedback);

