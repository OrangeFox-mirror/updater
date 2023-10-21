import subprocess as sp
import json
import os
from loguru import logger

with open("repos.json", "r", encoding="utf-8") as repos_file:
    repos = json.load(repos_file)
    logger.info("Imported repo list")

print("\n")

for repo in repos:
    print("======================")
    source_repo = repo["source"]
    destination_repo = repo["destination"]
    repo_dir = destination_repo.split("/"
                                        )[-1].replace(
                                                ".git/", ".git"
                                            ).replace(
                                                ".git", ""
                                            )
    logger.info(f"Clonning {source_repo} to {repo_dir}...")
    clone_cmd = sp.run(["git", "clone", "--mirror",
                        destination_repo, repo_dir],
                        capture_output=True,
                        text=True)
    if clone_cmd.returncode == 0:
        logger.success(f"Successfully cloned {source_repo} to {repo_dir}")
    else:
        logger.error(f"Error while cloning {source_repo} to {repo_dir}, status code: {str(clone_cmd.returncode)}:\n" +
                     f"- stdout:\n{clone_cmd.stdout}\n- stderr:\n{clone_cmd.stderr}")
        print("======================\n")
        continue

    logger.info(f"Pushing {destination_repo} ({repo_dir}) to {destination_repo}...")
    push_cmd = sp.run(["git", "--git-dir", repo_dir, "push", "--mirror", destination_repo], capture_output=True, text=True)
    if push_cmd.returncode == 0:
        logger.success(f"Successfully pushed {source_repo} to {destination_repo}")
    else:
        logger.error(f"Error while pushing {source_repo} to {destination_repo}, status code: {str(push_cmd.returncode)}:\n"+
                     f"- stdout:\n{push_cmd.stdout}\n- stderr:\n{push_cmd.stderr}")
        print("======================\n")
        continue

    print("======================\n")
