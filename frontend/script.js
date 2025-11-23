const API_URL = "http://localhost:8000";
let currentMode = 'chat';

function setMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.mode-switch button').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`mode-${mode}`).classList.add('active');
    
    const title = document.getElementById('chat-title');
    const badge = document.getElementById('source-badge');
    
    if (mode === 'chat') {
        title.innerText = "General Knowledge Agent";
        badge.innerText = "LangGraph + AstraDB";
    } else {
        title.innerText = "Code Assistant";
        badge.innerText = "CodeLlama (Ollama)";
    }
    
    addMessage("system", `Switched to ${mode === 'chat' ? 'General Knowledge' : 'Code Assistant'} mode.`);
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    addMessage("user", message);
    input.value = "";

    const endpoint = currentMode === 'chat' ? '/chat' : '/code';
    const payload = currentMode === 'chat' ? { message: message } : { prompt: message };

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        if (response.ok) {
            addMessage("assistant", data.response);
        } else {
            addMessage("system", `Error: ${data.detail}`);
        }
    } catch (error) {
        addMessage("system", `Connection Error: ${error.message}`);
    }
}

function addMessage(role, text) {
    const history = document.getElementById('chat-history');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    msgDiv.innerHTML = `<div class="content">${text.replace(/\n/g, '<br>')}</div>`;
    history.appendChild(msgDiv);
    history.scrollTop = history.scrollHeight;
}

async function ingestUrl() {
    const url = document.getElementById('url-input').value;
    const status = document.getElementById('status-msg');
    
    if (!url) return;
    
    status.innerText = "Processing URL...";
    status.style.color = "#fbbf24";

    try {
        const response = await fetch(`${API_URL}/ingest/url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        if (response.ok) {
            status.innerText = "Success! Summary: " + data.data.summary.substring(0, 50) + "...";
            status.style.color = "#34d399";
        } else {
            status.innerText = "Error: " + data.detail;
            status.style.color = "#f87171";
        }
    } catch (error) {
        status.innerText = "Error: " + error.message;
        status.style.color = "#f87171";
    }
}

async function ingestPdf() {
    const fileInput = document.getElementById('pdf-input');
    const file = fileInput.files[0];
    const status = document.getElementById('status-msg');

    if (!file) return;

    status.innerText = "Uploading PDF...";
    status.style.color = "#fbbf24";

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/ingest/pdf`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            status.innerText = `Success! Ingested ${data.chunks} chunks.`;
            status.style.color = "#34d399";
        } else {
            status.innerText = "Error: " + data.detail;
            status.style.color = "#f87171";
        }
    } catch (error) {
        status.innerText = "Error: " + error.message;
        status.style.color = "#f87171";
    }
}
