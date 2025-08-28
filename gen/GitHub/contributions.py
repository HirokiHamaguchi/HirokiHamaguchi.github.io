import csv
import os

import requests
from dotenv import load_dotenv

# .env 読み込み
load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

if not USERNAME or not TOKEN:
    raise ValueError(".env に GITHUB_USERNAME および GITHUB_TOKEN を設定してください。")

# GraphQL クエリ （複数カテゴリ対応）
query = """
query($username: String!) {
  user(login: $username) {
    contributionsCollection {
      commitContributionsByRepository(maxRepositories: 100) {
        repository {
          nameWithOwner
          isPrivate
          owner { login }
        }
      }
      pullRequestContributionsByRepository(maxRepositories: 100) {
        repository {
          nameWithOwner
          isPrivate
          owner { login }
        }
      }
      issueContributionsByRepository(maxRepositories: 100) {
        repository {
          nameWithOwner
          isPrivate
          owner { login }
        }
      }
      pullRequestReviewContributionsByRepository(maxRepositories: 100) {
        repository {
          nameWithOwner
          isPrivate
          owner { login }
        }
      }
    }
  }
}
"""


def fetch_contributed_repos(username):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    response = requests.post(
        url, json={"query": query, "variables": {"username": username}}, headers=headers
    )
    if response.status_code != 200:
        raise Exception(f"Query failed (HTTP {response.status_code}): {response.text}")

    result = response.json()
    if "errors" in result:
        raise Exception(f"GraphQL エラー: {result['errors']}")

    data = result["data"]["user"]["contributionsCollection"]
    repos = set()

    def extract(reps):
        for item in reps or []:
            repo = item["repository"]
            if repo["owner"]["login"].lower() != username.lower():
                repos.add(
                    (repo["nameWithOwner"], repo["owner"]["login"], repo["isPrivate"])
                )

    extract(data.get("commitContributionsByRepository"))
    extract(data.get("pullRequestContributionsByRepository"))
    extract(data.get("issueContributionsByRepository"))
    extract(data.get("pullRequestReviewContributionsByRepository"))

    return sorted(repos)


def save_to_csv(repos, filename="contributed_repos.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Repository", "Owner", "Private?"])
        for name, owner, is_private in repos:
            writer.writerow([name, owner, is_private])
    print(f"{filename} に出力されました。")


if __name__ == "__main__":
    repos = fetch_contributed_repos(USERNAME)
    save_to_csv(repos)
