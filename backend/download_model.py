from huggingface_hub import snapshot_download
import os

# Define the local directory
model_path = os.path.join(os.path.dirname(__file__), "model")

# Define expected files and minimum sizes (approximate bytes)
# The .data file is large (~2.5GB), checking for > 1GB to be safe and avoid partial LFS pointers
EXPECTED_FILES = {
    "phi3-mini-4k-instruct-cpu-int4-rtn-block-32.onnx": 100 * 1024, # > 100KB
    "phi3-mini-4k-instruct-cpu-int4-rtn-block-32.onnx.data": 1 * 1024 * 1024 * 1024, # > 1GB
}

def verify_existing_model(path):
    """Check if model files exist and are large enough (not just LFS pointers)."""
    full_path = os.path.join(path, "cpu_and_mobile", "cpu-int4-rtn-block-32")
    if not os.path.exists(full_path):
        return False
        
    for filename, min_size in EXPECTED_FILES.items():
        file_path = os.path.join(full_path, filename)
        if not os.path.exists(file_path):
            print(f"Missing file: {filename}")
            return False
        
        file_size = os.path.getsize(file_path)
        if file_size < min_size:
            print(f"File too small (likely LFS pointer): {filename} ({file_size} bytes)")
            return False
            
    print("Valid model files found locally.")
    return True

if verify_existing_model(model_path):
    print(f"Model already fully downloaded in {model_path}")
else:
    print(f"Downloading/Verifying ONNX model to {model_path}...")
    try:
        snapshot_download(
            repo_id="microsoft/Phi-3-mini-4k-instruct-onnx",
            allow_patterns=["cpu_and_mobile/cpu-int4-rtn-block-32/*"],
            local_dir=model_path,
            local_dir_use_symlinks=False,
            # Force download if files were missing/bad, ensuring LFS
            resume_download=True 
        )
        print("Download complete!")
    except Exception as e:
        print(f"Download failed: {e}")
