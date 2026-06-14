"""
Ultimate memory-level monkey-patch for the Pydantic v1 / ChromaDB type inference bug.
This patch runs completely in memory and does not require write access to the filesystem,
making it 100% compatible with read-only cloud environments like Streamlit Cloud.
"""
import sys

def apply_memory_patch():
    try:
        # Import pydantic v1 typing module where the bug originates
        import pydantic.v1.typing as pydantic_typing
        from pydantic.v1.errors import ConfigError
        
        # Save the original function
        original_resolve_annotations = pydantic_typing.resolve_annotations
        
        # Define our wrapped function that catches the specific ChromaDB crash
        def patched_resolve_annotations(raw_annotations, module_name):
            try:
                return original_resolve_annotations(raw_annotations, module_name)
            except ConfigError as e:
                if "chroma_server_nofile" in str(e):
                    # If it's the exact chroma bug, just remove the problematic annotation 
                    # by returning an empty dict or filtering it out!
                    safe_annotations = {
                        k: v for k, v in raw_annotations.items() if k != "chroma_server_nofile"
                    }
                    return original_resolve_annotations(safe_annotations, module_name)
                raise  # Re-raise if it's a different error
                
        # Override the function in memory
        pydantic_typing.resolve_annotations = patched_resolve_annotations
        print("Memory patch applied successfully!")
    except ImportError:
        # If pydantic.v1 isn't installed yet, or it's a completely different version, skip safely.
        pass

# Run immediately upon import
apply_memory_patch()
