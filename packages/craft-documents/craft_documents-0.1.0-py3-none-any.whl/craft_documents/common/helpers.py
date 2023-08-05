from typing import Any, Dict, List

import requests
from rich import print


def combine_dictionaries(
    dict1: Dict[Any, Any], dict2: Dict[Any, Any]
) -> Dict[Any, Any]:
    result = dict1
    for key, value in dict2.items():
        if key not in dict1:
            result[key] = value
        else:
            # if both are lists, combine the lists
            if isinstance(value, list) and isinstance(dict1[key], list):
                result[key] = dict1[key] + value
            # if both are dictionaries, combine them
            elif isinstance(value, dict) and isinstance(dict1[key], dict):
                result[key] = combine_dictionaries(dict1[key], value)
    return result


def create_list(input: Any | List[Any]) -> List[Any]:
    if isinstance(input, list):
        return input
    else:
        return [input]


def fetch_github_directory(
    owner: str, repo: str, path: str, verbose: bool = False
) -> dict[str, str] | None:
    """
    Fetch all files in a directory hosted on GitHub.

    Attribution to ChatGPT.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            documents = {}
            for item in data:
                if "type" in item and item["type"] == "file" and "download_url" in item:
                    document_url = item["download_url"]
                    document_response = requests.get(document_url)
                    if document_response.status_code == 200:
                        if verbose:
                            print(
                                "Fetching [bold white]%s[/bold white]..." % item["name"]
                            )
                        documents[item["name"]] = document_response.content.decode()
                    else:
                        print(
                            "[red]Failed to fetch document: "
                            + f"[bold white]{document_url}[/bold white][/red]"
                        )
            return documents
    elif response.status_code == 404:
        print("[red]Directory not found.[/red]")
        # raise Abort()
        return None
    else:
        print("[red]Failed to fetch directory.[/red]")
        # raise Abort()
