import requests
import re
import semver
import yaml
import sys

ADDON = None

if len(sys.argv) > 1:
    # The first argument is at index 1, as index 0 is the script filename
    ADDON = sys.argv[1]
else:
    print("No arguments provided.")
    exit(1)

BASE_YAML_PATH = f"./{ADDON}/base_image.yaml"
BUILD_YAML_PATH = f"./{ADDON}/build.yaml"
CONFIG_YAML_PATH = f"./{ADDON}/config.yaml"
CHANGELOG_PATH = f"./{ADDON}/CHANGELOG.md"

with open(BASE_YAML_PATH, "r") as file:
    yaml_data = yaml.safe_load(file)
    ARCH = yaml_data["arch"]
    FILTER = yaml_data["filter"]
    REPO = yaml_data["repo"]


# Function to get the current tag from build.yaml using PyYAML
def get_current_tag():
    try:
        with open(BUILD_YAML_PATH, "r") as file:
            yaml_data = yaml.safe_load(file)
            # Navigate to the key and extract the version
            image_tag = yaml_data.get("build_from", {}).get(ARCH[0], "")
            tag = image_tag.split(":")[-1]  # Extract the version after ':'
            return tag
    except Exception as e:
        raise Exception(f"Error reading the YAML file: {e}") from e


# Function to update the build.yaml file with the new image version
def update_build_yaml(repo_name, new_tag):
    try:
        with open(BUILD_YAML_PATH, "r") as file:
            yaml_data = yaml.safe_load(file)
        # Update the aarch64 image tag with the new version
        for _a in ARCH:
            yaml_data["build_from"][_a] = f"{repo_name}:{new_tag}"

        # Write the updated data back to the file
        with open(BUILD_YAML_PATH, "w") as file:
            yaml.dump(yaml_data, file, default_flow_style=False)
        print(f"Updated build.yaml to version {repo_name}:{new_tag}")
    except Exception as e:
        raise Exception(f"Error updating build.yaml: {e}") from e


# Function to get all tags from Docker Hub
def get_docker_tags(repo_name):
    url = f"https://hub.docker.com/v2/repositories/{repo_name}/tags"
    tags = []
    page = 1

    while True:
        response = requests.get(url, params={"page_size": 100, "page": page})
        if response.status_code != 200:
            print(f"Failed to get tags from Docker Hub: {response.status_code}")
            break

        data = response.json()
        new_tags = [tag["name"] for tag in data["results"]]
        print(f"Batch {page}: {new_tags}")
        tags.extend(new_tags)

        if not data["next"]:
            break
        page += 1

    return tags


# Function to get and increment the version in config.yaml
def increment_config_version():
    try:
        with open(CONFIG_YAML_PATH, "r") as file:
            yaml_data = yaml.safe_load(file)

        # Extract the current version and increment the patch version
        current_config_version = yaml_data.get("version", "1.0.0")
        new_config_version = semver.VersionInfo.parse(
            current_config_version
        ).bump_minor()

        # Update the version in config.yaml
        yaml_data["version"] = str(new_config_version)

        # Write the updated config.yaml
        with open(CONFIG_YAML_PATH, "w") as file:
            yaml.dump(yaml_data, file, default_flow_style=False)

        print(f"Updated config.yaml to version {new_config_version}")
        return str(new_config_version)
    except Exception as e:
        print(f"Error updating config.yaml: {e}")
        return None


# Function to add an entry to the CHANGELOG.md
def update_changelog(new_config_version, repo_name, new_tag):
    changelog_entry = f"## {new_config_version}\n\n- Updated base image of addon to {repo_name}:{new_tag}\n\n"
    try:
        with open(CHANGELOG_PATH, "r+") as file:
            content = file.read()
            # Insert the new entry at the beginning
            file.seek(0, 0)
            file.write(changelog_entry + content)
        print(f"Added changelog entry for version {new_config_version}")
    except Exception as e:
        print(f"Error updating CHANGELOG.md: {e}")


# Function to filter tags that start with {regex} and extract semver version
def filter_and_extract_versions(tags):
    version_pattern = re.compile(FILTER)
    versions = []

    for tag in tags:
        match = version_pattern.match(tag)
        if match:
            versions.append(match.group(1))  # Extract the semver part after 'v'

    return versions


# Main function
def main():
    # Get the current version from build.yaml
    current_tag = get_current_tag()
    if not current_tag:
        print("Could not determine the current tag.")
        return

    [current_version] = filter_and_extract_versions([current_tag])

    print(f"Current tag and version: {current_tag} / {current_version}")

    # Get all tags from Docker Hub
    tags = get_docker_tags(REPO)

    # Filter tags and extract the semver versions
    versions = filter_and_extract_versions(tags)

    # Sort the extracted versions by semver
    sorted_versions = sorted(versions, key=semver.VersionInfo.parse, reverse=True)

    print(f"Available versions: {sorted_versions}")

    # Compare the current version with the latest version in Docker Hub
    if semver.compare(current_version, sorted_versions[0]) < 0:
        print(
            f"Update available! Current version: {current_version}, Latest version: {sorted_versions[0]}"
        )

        # Update build.yaml with the new version
        update_build_yaml(
            REPO, current_tag.replace(current_version, sorted_versions[0])
        )

        # Increment the config.yaml version and get the new config version
        new_config_version = increment_config_version()

        # Add a new entry to the CHANGELOG.md
        if new_config_version:
            update_changelog(new_config_version, REPO, sorted_versions[0])
    else:
        print(f"You are using the latest version: {current_version}")


main()
