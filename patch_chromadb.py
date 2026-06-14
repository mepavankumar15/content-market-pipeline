"""
Monkey-patch for chromadb Settings to fix Pydantic type inference error.
This MUST be imported before crewai or chromadb.
"""
import importlib
import sys

def patch_chromadb():
    """Patch chromadb Settings to avoid 'unable to infer type for chroma_server_nofile' error."""
    try:
        # Try importing chromadb.config to see if it works
        from chromadb.config import Settings
        # If it works, no patch needed
        return
    except Exception:
        pass

    try:
        # Force-patch by pre-setting the problematic attributes with type hints
        import chromadb.config as config_module
        original_settings = config_module.Settings

        # Create a patched version that handles the missing type
        class PatchedSettings(original_settings):
            chroma_server_nofile: str = ""

        config_module.Settings = PatchedSettings
    except Exception:
        # If chromadb isn't installed at all, skip
        pass

patch_chromadb()
