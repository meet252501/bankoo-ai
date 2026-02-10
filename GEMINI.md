# Gemini CLI Rules for Antigravity Workspace

You are running inside the **Antigravity AI Environment**. 
Your goal is to cooperate with the Antigravity agent to provide autonomous fixes.

## Fix Protocol
When a user asks for a "fix" or when a command fails:
1.  **Analyze the error**: Use the current terminal output or logs.
2.  **Proposed Code**: Provide the full corrected content of the file.
3.  **Format**: Wrap your code in standard markdown blocks with the language and target file path.
    Example:
    ```powershell:C:/path/to/file.ps1
    # corrected code here
    ```
4.  **No Chattyness**: Keep explanations brief if a fix is being requested. Focus on the code.

## Available Tools
If the `agy` command is available, you can use it to signal the IDE, but primarily rely on your standard file-writing capabilities or provide the code for the `fix` shell function to apply.
