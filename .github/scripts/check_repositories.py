import requests
import json
from urllib.parse import urlparse
import sys


def get_latest_release(repo_url):
    """Get the latest release tag from a GitHub repository."""
    try:
        # Extract owner and repo name from the URL
        path = urlparse(repo_url).path.strip("/")
        owner, repo = path.split("/")[-2:]

        # Make the GET request to the GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data["tag_name"]
        else:
            print(f"Failed to fetch data for {repo_url}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching the latest release for {repo_url}: {e}")
        sys.exit(1)


def check_releases(json_file):
    """Check the release tags for a list of repositories."""
    try:
        with open(json_file, "r") as file:
            repos = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file '{json_file}': {e}")
        sys.exit(1)

    outdated_repos = []

    for repo in repos:
        repo_url = repo.get("repository")
        current_tag = repo.get("tag")

        if not repo_url or not current_tag:
            print(f"Invalid repository entry: {repo}")
            continue

        latest_tag = get_latest_release(repo_url)

        if latest_tag and latest_tag != current_tag:
            outdated_repos.append(
                {
                    "repository": repo_url,
                    "current_tag": current_tag,
                    "latest_tag": latest_tag,
                }
            )

    return outdated_repos


def main(json_file):
    """Main function to check releases and generate an output file."""
    try:
        outdated_repos = check_releases(json_file)

        # Output results in a format suitable for GitHub Actions
        output = {
            "outdated_repos": outdated_repos,
            "outdated_count": len(outdated_repos),
        }

        # Write the output to a JSON file
        with open("outdated_repositories.json", "w") as f:
            json.dump(output, f, indent=2)

        # Print the output for GitHub Actions
        print(json.dumps(output))

    except Exception as e:
        print(f"Error in main execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main("repositories.json")
