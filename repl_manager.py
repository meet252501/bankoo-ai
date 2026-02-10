"""
Bankoo AI - Python REPL Manager
Provides interactive Python REPL with session persistence
"""

import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
import code
import threading


class PythonREPL:
    """Interactive Python REPL with state persistence"""
    
    def __init__(self, session_id="default"):
        self.session_id = session_id
        self.locals = {}
        self.globals = {"__name__": "__console__", "__doc__": None}
        self.buffer = []
        self.in_multiline = False
        
    def execute_line(self, line):
        """
        Execute a line of Python code
        Returns: dict with output, error, and next prompt
        """
        result = {
            "output": "",
            "error": "",
            "prompt": ">>> ",
            "success": True
        }
        
        # Handle special commands
        if line.strip() in ["exit()", "quit()"]:
            result["output"] = "# Use Ctrl+D or clear REPL to reset session"
            return result
        
        # Check if we're continuing multiline input
        if self.in_multiline or line.strip().endswith(":"):
            self.buffer.append(line)
            # Check if line is empty (end of multiline)
            if line.strip() == "" and self.buffer:
                code_to_execute = "\n".join(self.buffer)
                self.buffer = []
                self.in_multiline = False
                return self._execute_code(code_to_execute)
            else:
                self.in_multiline = True
                result["prompt"] = "... "
                return result
        
        # Single line execution
        return self._execute_code(line)
    
    def _execute_code(self, code_string):
        """Execute Python code and capture output"""
        result = {
            "output": "",
            "error": "",
            "prompt": ">>> ",
            "success": True
        }
        
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            # Try to compile as eval first (for expressions)
            try:
                compiled = compile(code_string, "<console>", "eval")
                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    ret_value = eval(compiled, self.globals, self.locals)
                    if ret_value is not None:
                        print(repr(ret_value))
            except SyntaxError:
                # Not an expression, compile as exec
                compiled = compile(code_string, "<console>", "exec")
                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    exec(compiled, self.globals, self.locals)
            
            # Get captured output
            output = stdout_capture.getvalue()
            errors = stderr_capture.getvalue()
            
            if output:
                result["output"] = output.rstrip()
            if errors:
                result["error"] = errors.rstrip()
                
        except Exception as e:
            # Capture exception
            error_output = io.StringIO()
            traceback.print_exc(file=error_output)
            result["error"] = error_output.getvalue().rstrip()
            result["success"] = False
        
        return result
    
    def reset(self):
        """Reset the REPL session"""
        self.locals = {}
        self.globals = {"__name__": "__console__", "__doc__": None}
        self.buffer = []
        self.in_multiline = False


class REPLSessionManager:
    """Manage multiple REPL sessions"""
    
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
    
    def get_session(self, session_id):
        """Get or create a REPL session"""
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = PythonREPL(session_id)
            return self.sessions[session_id]
    
    def reset_session(self, session_id):
        """Reset a specific session"""
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id].reset()
    
    def delete_session(self, session_id):
        """Delete a session"""
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
    
    def list_sessions(self):
        """List all active sessions"""
        with self.lock:
            return list(self.sessions.keys())


# Global session manager
repl_manager = REPLSessionManager()


if __name__ == "__main__":
    # Test the REPL
    print("Testing Python REPL...")
    repl = PythonREPL("test")
    
    test_commands = [
        "x = 5",
        "y = 10",
        "x + y",
        "def greet(name):",
        "    return f'Hello, {name}!'",
        "",
        "greet('Meet')",
        "import math",
        "math.pi",
    ]
    
    for cmd in test_commands:
        print(f">>> {cmd}")
        result = repl.execute_line(cmd)
        if result["output"]:
            print(result["output"])
        if result["error"]:
            print(f"ERROR: {result['error']}")
