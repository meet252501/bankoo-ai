"""
Smart Notes Advanced Features - ONE-CLICK INSTALLER
Automatically adds all features to bankoo_ui.html
"""
import re

print("🚀 Installing Smart Notes Advanced Features...")
print("="*60)

# Read the HTML file
with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Track what we're adding
features_added = []

# FEATURE 1: Add Code/Text Toggle in Note Editor
if 'noteTypeToggle' not in html:
    print("📝 Adding code/text toggle...")
    
    # Find the note editor title input
    editor_pattern = r'(<h3 style="color: #00d4ff; margin: 0 0 20px;">Edit Note</h3>)'
    
    toggle_html = r'''\1
        
        <div style="display: flex; gap: 15px; margin-bottom: 15px; align-items: center; padding: 10px; background: rgba(0, 0, 0, 0.2); border-radius: 8px;">
            <label style="display: flex; align-items: center; gap: 8px; color: #ccc; cursor: pointer;">
                <input type="checkbox" id="noteTypeToggle" onchange="toggleNoteType()" style="width: 18px; height: 18px; cursor: pointer;">
                <span>💻 Code Snippet</span>
            </label>
            <select id="noteLang" style="display: none; background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(0, 212, 255, 0.3); color: white; padding: 8px 12px; border-radius: 6px; cursor: pointer;">
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="html">HTML</option>
                <option value="css">CSS</option>
                <option value="sql">SQL</option>
                <option value="json">JSON</option>
            </select>
        </div>
        '''
    
    html = re.sub(editor_pattern, toggle_html, html)
    features_added.append("Code/Text Toggle")
else:
    print("✓ Code toggle already exists")

# FEATURE 2: Add Voice & Summarize Buttons
if 'startVoiceNote' not in html:
    print("🎤 Adding voice-to-text and summarize buttons...")
    
    # Find the AI Tags button and add more buttons after it
    ai_tags_pattern = r'(<button onclick="suggestTags\(\)"[^>]+>🤖 AI Tags</button>)'
    
    extra_buttons = r'''\1
            <button onclick="startVoiceNote()" id="voiceBtn" style="background: linear-gradient(135deg, #00ff88, #00d4ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer; transition: all 0.3s;">🎤 Voice</button>
            <button onclick="summarizeNote()" style="background: linear-gradient(135deg, #ff006e, #b026ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">📝 Summarize</button>'''
    
    html = re.sub(ai_tags_pattern, extra_buttons, html)
    features_added.append("Voice & Summarize Buttons")
else:
    print("✓ Voice/Summarize buttons already exist")

# FEATURE 3: Add "Ask Bankoo" Button in Notes View
if 'openAskModal' not in html:
    print("💬 Adding 'Ask Bankoo' feature...")
    
    # Find the New Note button in notes view
    new_note_pattern = r'(<button onclick="newNote\(\)"[^>]+>\+ New Note</button>)'
    
    ask_button = r'''\1
                <button onclick="openAskModal()" style="background: linear-gradient(135deg, #00ff88, #00d4ff); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">💬 Ask Bankoo</button>'''
    
    html = re.sub(new_note_pattern, ask_button, html)
    features_added.append("Ask Bankoo Button")
else:
    print("✓ Ask Bankoo button already exists")

# FEATURE 4: Add JavaScript Functions
if 'function toggleNoteType()' not in html:
    print("⚙️ Adding JavaScript functions...")
    
    # Find the closing </script> tag before </body>
    js_functions = '''
        // SMART NOTES ADVANCED FEATURES
        
        // Code/Text Toggle
        function toggleNoteType() {
            const isCode = document.getElementById('noteTypeToggle').checked;
            const langSelect = document.getElementById('noteLang');
            const textarea = document.getElementById('noteContent');
            
            if (isCode) {
                langSelect.style.display = 'block';
                textarea.style.fontFamily = "'JetBrains Mono', monospace";
                textarea.style.fontSize = '0.9rem';
                textarea.placeholder = 'Paste your code here...';
            } else {
                langSelect.style.display = 'none';
                textarea.style.fontFamily = 'inherit';
                textarea.style.fontSize = '1rem';
                textarea.placeholder = 'Write your note here...';
            }
        }
        
        // Voice-to-Text
        let recognition = null;
        let isRecording = false;
        
        function startVoiceNote() {
            if (!('webkitSpeechRecognition' in window)) {
                alert('⚠️ Voice recognition not supported in this browser.\\nTry Chrome or Edge.');
                return;
            }
            
            if (!recognition) {
                recognition = new webkitSpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                
                recognition.onresult = (event) => {
                    let transcript = '';
                    for (let i = 0; i < event.results.length; i++) {
                        transcript += event.results[i][0].transcript;
                    }
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
                alert('⚠️ Note too short to summarize (minimum 100 characters)');
                return;
            }
            
            try {
                const res = await fetch('/api/notes/summarize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content})
                });
                const data = await res.json();
                
                if (data.summary) {
                    const currentContent = document.getElementById('noteContent').value;
                    document.getElementById('noteContent').value = `📝 AI Summary: ${data.summary}\\n\\n---\\n\\n${currentContent}`;
                    alert('✅ Summary added to top of note!');
                } else {
                    alert('❌ Failed to generate summary');
                }
            } catch (e) {
                console.error('Summarize error:', e);
                alert('❌ Summarization failed. Make sure Bankoo backend is running.');
            }
        }
        
        // Ask Bankoo About Notes
        async function openAskModal() {
            const question = prompt('💬 Ask Bankoo about your notes:', 'What did I note about...');
            if (question) {
                await askBankooAboutNotes(question);
            }
        }
        
        async function askBankooAboutNotes(question) {
            try {
                const res = await fetch('/api/notes/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question})
                });
                const data = await res.json();
                
                if (data.answer) {
                    const sources = data.sources.map(s => s.title).join(', ');
                    alert(`💬 Bankoo says:\\n\\n${data.answer}\\n\\n📚 Sources: ${sources || 'No specific notes found'}`);
                } else {
                    alert('❌ Could not find an answer in your notes');
                }
            } catch (e) {
                console.error('Ask error:', e);
                alert('❌ Ask Bankoo failed. Make sure backend is running.');
            }
        }
        
        console.log('✅ Smart Notes Advanced Features Loaded!');
    </script>'''
    
    # Find the last </script> before </body>
    html = html.replace('</body>', js_functions + '\n</body>')
    features_added.append("JavaScript Functions")
else:
    print("✓ JavaScript functions already exist")

# Write the updated HTML
with open('bankoo_ui.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*60)
print("✅ INSTALLATION COMPLETE!")
print("="*60)

if features_added:
    print("\n📦 Features Added:")
    for feature in features_added:
        print(f"  ✅ {feature}")
else:
    print("\n✓ All features already installed!")

print("\n🎯 NEXT STEPS:")
print("1. RESTART Bankoo (close and relaunch bankoo_main.py)")
print("2. Open: http://127.0.0.1:5001")
print("3. Click: 📱 App Drawer → 📝 Smart Notes")
print("\n✨ NEW FEATURES:")
print("  💻 Code Snippet toggle (checkbox in note editor)")
print("  🎤 Voice-to-text (click Voice button)")
print("  📝 AI Summarize (click Summarize button)")
print("  💬 Ask Bankoo (click Ask Bankoo in notes view)")
print("\nEnjoy! 🚀")
