import re
import yaml
import semver
import sys
import requests
from bs4 import BeautifulSoup

ADDON = None

if len(sys.argv) > 1:
    # The first argument is at index 1, as index 0 is the script filename
    ADDON = sys.argv[1]
else:
    print("No arguments provided.")
    exit(1)

VERSIONS_YAML_PATH = f"./{ADDON}/versions.yaml"
CONFIG_YAML_PATH = f"./{ADDON}/config.yaml"
CHANGELOG_PATH = f"./{ADDON}/CHANGELOG.md"


# Function to get the stored versions from the versions.yaml file
def get_stored_versions():
    try:
        with open(VERSIONS_YAML_PATH, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading the versions.yaml file: {e}")
        return None


def get_apk_version(package_name, arch, repo):
    url = f"https://pkgs.alpinelinux.org/package/{repo}/{arch}/{package_name}"

    print(f"Fetch: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            version = None
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the specific table cell containing the version number
            version_cell = soup.find("th", string="Version").find_next_sibling("td")
            version = version_cell.find("a").text.strip()

            if version:
                print(f"Latest version of {package_name}: {version}")
                return version
            else:
                print(f"Could not find version information for {package_name}.")
        else:
            print(f"Failed to fetch package info. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching package information: {e}")


# Function to compare versions based on the bump type (major, minor, patch)
def should_update(stored_version, installed_version, bump_type):
    try:
        if semver.VersionInfo.is_valid(stored_version):
            stored_semver = semver.VersionInfo.parse(stored_version)
        else:
            parts = stored_version.split(".")
            stored_semver = semver.VersionInfo(
                **{
                    "major": parts[0] or 0,
                    "minor": parts[1] or 0,
                    "patch": parts[2] or 0,
                }
            )
        if semver.VersionInfo.is_valid(installed_version):
            installed_semver = semver.VersionInfo.parse(installed_version)
        else:
            parts = installed_version.split(".")
            installed_semver = semver.VersionInfo(
                **{
                    "major": parts[0] or 0,
                    "minor": parts[1] or 0,
                    "patch": parts[2] or 0,
                }
            )

        #
        if bump_type == "major" and installed_semver.major > stored_semver.major:
            return True
        elif bump_type == "minor" and (
            installed_semver.major > stored_semver.major
            or installed_semver.minor > stored_semver.minor
        ):
            return True
        elif (
            bump_type == "patch"
            and installed_semver.major > stored_semver.major
            or installed_semver.minor > stored_semver.minor
            or installed_semver.patch > stored_semver.patch
        ):
            return True
        return False
    except ValueError as e:
        print(f"Error parsing versions: {e}")
        return False


# Function to update the version in the versions.yaml file
def update_version_in_yaml(package, new_version, stored_versions):
    try:
        stored_versions[package]["version"] = new_version

        # Write the updated data back to the file
        with open(VERSIONS_YAML_PATH, "w") as file:
            yaml.dump(stored_versions, file, default_flow_style=False)
        print(f"Updated {package} version in versions.yaml to {new_version}")
    except Exception as e:
        print(f"Error updating versions.yaml: {e}")


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
        raise Exception(f"Error updating config.yaml: {e}") from e


# Function to add an entry to the CHANGELOG.md
def update_changelog(new_config_version, apk_versions):
    apk_entries = "\n".join(
        [
            (f"- Update apk package '{apk}' in addon to: {version}")
            for apk, version in apk_versions
        ]
    )
    changelog_entry = f"## {new_config_version}\n\n{apk_entries}\n\n"
    try:
        with open(CHANGELOG_PATH, "r+") as file:
            content = file.read()
            # Insert the new entry at the beginning
            file.seek(0, 0)
            file.write(changelog_entry + content)
        print(f"Added changelog entry for version {new_config_version}")
    except Exception as e:
        raise Exception(f"Error updating CHANGELOG.md: {e}") from e


# Main function to check if the versions need to be bumped
def check_version_bumps():
    # Load the stored versions from the versions.yaml file
    stored_versions = get_stored_versions()
    if stored_versions is None:
        return

    updated_apk_versions = []

    # Loop through each package in the versions.yaml file
    for package, info in stored_versions.items():
        stored_version_line = info.get("version", "")
        apk_name = info.get("apk", "")
        arch = info.get("arch", "x86_64")
        repo = info.get("repo", "edge/community")
        bump_type = info.get("bump", "major").lower()

        # Extract the version number (e.g., 128.0.6613.119 or 1.2.3) from the version string
        stored_version_match = re.search(
            r"(\d+\.\d+\.\d+(?:\.\d+)?)", stored_version_line
        )
        if not stored_version_match:
            print(f"Error: Invalid version format for {package} in versions.yaml.")
            continue

        stored_version = stored_version_match.group(0)

        # Get the latest version of the package
        available_version = get_apk_version(apk_name, arch, repo)
        if available_version is None:
            continue

        print(f"\nChecking {package}:")
        print(f"  Stored version: {stored_version}")
        print(f"  Available version: {available_version}")
        print(f"  Bump type: {bump_type.capitalize()}")

        # Compare versions based on the bump type (major, minor, patch)
        if should_update(stored_version, available_version, bump_type):
            print(f"  {package} needs an update!")
            update_version_in_yaml(package, available_version, stored_versions)
            updated_apk_versions.append([package, available_version])
        else:
            print(f"  {package} is up-to-date.")

    if len(updated_apk_versions) > 0:
        # Increment the config.yaml version and get the new config version
        new_config_version = increment_config_version()

        # Add a new entry to the CHANGELOG.md
        update_changelog(new_config_version, updated_apk_versions)


check_version_bumps()
