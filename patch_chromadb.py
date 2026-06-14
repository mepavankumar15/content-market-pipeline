"""
Physical source-code patch for chromadb to fix the Pydantic type inference error.
This MUST be imported before crewai or chromadb in main.py.
"""
import os
import sys
import importlib.util

def apply_physical_patch():
    try:
        # Find where chromadb is installed WITHOUT importing it
        spec = importlib.util.find_spec("chromadb")
        if not spec or not spec.submodule_search_locations:
            return
            
        chromadb_path = spec.submodule_search_locations[0]
        config_file_path = os.path.join(chromadb_path, "config.py")
        
        if not os.path.exists(config_file_path):
            return
            
        # Read the source code
        with open(config_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # The bug is that pydantic strict typing throws an error because the validator
        # returns Optional[str] but the field is Optional[int].
        # We physically rewrite the type hint in the source code of the installed package!
        target_str = "chroma_server_nofile: Optional[int] = None"
        replacement_str = "chroma_server_nofile: Optional[str] = None"
        
        if target_str in content:
            new_content = content.replace(target_str, replacement_str)
            with open(config_file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Successfully patched chromadb/config.py source code!")
            
    except Exception as e:
        print(f"Failed to patch chromadb: {e}")

apply_physical_patch()
