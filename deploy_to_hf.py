import os
import re
import subprocess
from huggingface_hub import HfApi

def get_token_and_repo():
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "space"], text=True).strip()
        # Pattern: https://git:TOKEN@huggingface.co/spaces/REPO
        match = re.search(r"https://git:(.*?)@huggingface\.co/spaces/(.*)", url)
        if match:
            return match.group(1), match.group(2)
    except:
        pass
    return None, None

def deploy():
    token, repo_id = get_token_and_repo()
    if not token or not repo_id:
        print("Error: Could not find HF Token or Repo in git remote 'space'")
        return

    print(f"Deploying to HF Space: {repo_id}")
    api = HfApi()
    
    # Upload everything in the current directory, ignoring unnecessary folders
    try:
        api.upload_folder(
            folder_path=".",
            repo_id=repo_id,
            repo_type="space",
            token=token,
            ignore_patterns=[
                "**/node_modules/**",
                "**/.next/**",
                "**/__pycache__/**",
                "backend/__pycache__/**",
                "frontend/node_modules/**",
                "frontend/.next/**",
                "*.pyc",
                ".git/**",
                "frontend/out/**"
            ]
        )
        print("✅ Deployment Successful via HfApi!")
    except Exception as e:
        print(f"❌ Deployment Failed: {e}")

if __name__ == "__main__":
    deploy()
