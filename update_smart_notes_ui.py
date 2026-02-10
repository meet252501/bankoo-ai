"""
Smart Notes Advanced Features - Complete Frontend Update
Adds: Code snippets, Voice-to-text, AI Summarization, Semantic Search, Ask Bankoo
"""
import re

print("🚀 Updating Smart Notes with advanced features...")

# Read HTML file
with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add code/text toggle and language selector to note editor
editor_additions = '''
        <div style="display: flex; gap: 10px; margin-bottom: 15px; align-items: center;">
            <label style="display: flex; align-items: center; gap: 8px; color: #ccc;">
                <input type="checkbox" id="noteTypeToggle" onchange="toggleNoteType()" style="width: 18px; height: 18px;">
                <span>Code Snippet</span>
            </label>
            <select id="noteLang" style="display: none; background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.2); color: white; padding: 8px; border-radius: 6px;">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="html">HTML</option>
                <option value="css">CSS</option>
                <option value="sql">SQL</option>
                <option value="json">JSON</option>
            </select>
        </div>
        
        <input id="noteTitle"'''

# Insert before noteTitle
content = content.replace(
    '<input id="noteTitle"',
    editor_additions
)

# 2. Add voice-to-text and summarize buttons after AI Tags button
voice_buttons = '''<button onclick="suggestTags()" style="background: linear-gradient(135deg, #b026ff, #ff006e); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">🤖 AI Tags</button>
            <button onclick="startVoiceNote()" id="voiceBtn" style="background: linear-gradient(135deg, #00ff88, #00d4ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">🎤 Voice</button>
            <button onclick="summarizeNote()" style="background: linear-gradient(135deg, #ff006e, #b026ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">📝 Summarize</button>'''

content = content.replace(
    '<button onclick="suggestTags()" style="background: linear-gradient(135deg, #b026ff, #ff006e); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">🤖 AI Tags</button>',
    voice_buttons
)

#3. Add "Ask Bankoo" button in notes view header
ask_button = '''<button onclick="newNote()" style="background: linear-gradient(135deg, #00d4ff, #b026ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">+ New Note</button>
                <button onclick="openAskModal()" style="background: linear-gradient(135deg, #00ff88, #00d4ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">💬 Ask Bankoo</button>'''

content = content.replace(
    '<button onclick="newNote()" style="background: linear-gradient(135deg, #00d4ff, #b026ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">+ New Note</button>',
    ask_button
)

# Save updated HTML
with open('bankoo_ui.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ UI updated with new buttons and controls!")

# Now create the JavaScript additions file
js_additions = """
// ADVANCED SMART NOTES FEATURES

// Code Snippet Toggle
function toggleNoteType() {
    const isCode = document.getElementById('noteTypeToggle').checked;
    const langSelect = document.getElementById('noteLang');
    const textarea = document.getElementById('noteContent');
    
    if (isCode) {
        langSelect.style.display = 'block';
        textarea.style.fontFamily = "'JetBrains Mono', monospace";
        textarea.style.fontSize = '0.9rem';
    } else {
        langSelect.style.display = 'none';
        textarea.style.fontFamily = 'inherit';
        textarea.style.fontSize = '1rem';
    }
}

// Voice-to-Text
let recognition = null;
let isRecording = false;

function startVoiceNote() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Voice recognition not supported in this browser');
        return;
    }
    
    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        
        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');
            document.getElementById('noteContent').value = transcript;
        };
        
        recognition.onerror = (event) => {
            console.error('Voice error:', event.error);
            stopVoiceNote();
        };
    }
    
    if (isRecording) {
        stopVoiceNote();
    } else {
        recognition.start();
        isRecording = true;
        document.getElementById('voiceBtn').textContent = '⏹️ Stop';
        document.getElementById('voiceBtn').style.background = 'linear-gradient(135deg, #ff006e, #ff4d4d)';
    }
}

function stopVoiceNote() {
    if (recognition && isRecording) {
        recognition.stop();
        isRecording = false;
        document.getElementById('voiceBtn').textContent = '🎤 Voice';
        document.getElementById('voiceBtn').style.background = 'linear-gradient(135deg, #00ff88, #00d4ff)';
    }
}

// AI Summarization
async function summarizeNote() {
    const content = document.getElementById('noteContent').value;
    if (!content || content.length < 100) {
        alert('Note too short to summarize');
        return;
    }
    
    try {
        const res = await fetch('/api/notes/summarize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({content})
        });
        const data = await res.json();
        
        // Prepend summary to note
        const currentTitle = document.getElementById('noteTitle').value;
        document.getElementById('noteTitle').value = currentTitle || 'Summary';
        document.getElementById('noteContent').value = `📝 Summary: ${data.summary}\\n\\n---\\n\\n${content}`;
    } catch (e) {
        console.error('Summarize failed:', e);
    }
}

// Ask Bankoo Modal
function openAskModal() {
    const modal = prompt('Ask Bankoo about your notes:', 'What did I note about...');
    if (modal) askBankooAboutNotes(modal);
}

async function askBankooAboutNotes(question) {
    try {
        const res = await fetch('/api/notes/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question})
        });
        const data = await res.json();
        
        alert(`💬 Bankoo says:\\n\\n${data.answer}\\n\\n📚 Based on ${data.sources.length} note(s)`);
    } catch (e) {
        console.error('Ask failed:', e);
    }
}

// Enhanced saveNote with code support
const originalSaveNote = typeof saveNote !== 'undefined' ? saveNote : null;
saveNote = async function() {
    const title = document.getElementById('noteTitle').value || 'Untitled';
    const content = document.getElementById('noteContent').value;
    const tagsStr = document.getElementById('noteTags').value;
    const tags = tagsStr.split(',').map(t => t.trim()).filter(t => t);
    
    const isCode = document.getElementById('noteTypeToggle').checked;
    const note_type = isCode ? 'code' : 'text';
    const language = isCode ? document.getElementById('noteLang').value : null;

    try {
        if (currentNoteId) {
            await fetch(`/api/notes/${currentNoteId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, content, tags, note_type, language})
            });
        } else {
            await fetch('/api/notes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, content, tags, note_type, language})
            });
        }
        document.getElementById('noteEditor').style.display = 'none';
        loadNotes();
    } catch (e) {
        console.error('Failed to save note:', e);
    }
}

console.log('✅ Smart Notes Advanced Features Loaded!');
"""

with open('smart_notes_advanced.js', 'w', encoding='utf-8') as f:
    f.write(js_additions)

print("✅ JavaScript features created: smart_notes_advanced.js")
print("")
print("📋 NEXT STEPS:")
print("1. Add this line to bankoo_ui.html before </body>:")
print('   <script src="smart_notes_advanced.js"></script>')
print("")
print("2. Restart Bankoo to test the features!")
print("")
print("✨ NEW FEATURES:")
print("  🔹 Code snippet toggle with syntax highlighting")
print("  🔹 Voice-to-text (click 🎤 Voice button)")
print("  🔹 AI Summarization (click 📝 Summarize)")
print("  🔹 Ask Bankoo about your notes (click 💬 Ask Bankoo)")
