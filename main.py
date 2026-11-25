import argparse
import json
import yaml
from tabulate import tabulate


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            if file_path.lower().endswith(".json"):
             parsed_data = json.load(file)
             documents = parsed_data if isinstance(parsed_data, list) else [parsed_data]

            elif file_path.lower().endswith((".yaml", ".yml")):
             documents = yaml.safe_load_all(file)

            else:
                print(f"Unsupported file format: {file_path}")
                return
            found_resource = False
            skipped_resources = 0
            table_rows = []

            for document in documents:
                if document is None:
                    continue

                if not isinstance(document, dict):
                    print("Skipping invalid Kubernetes document.")
                    continue


                for field in ("apiVersion", "kind"):
                    if field not in document:
                        print(f"Warning: {field} is missing.")
                    elif document[field] is None:
                        print(f"Warning: {field} is null.")
                    elif not isinstance(document[field], str):
                        print(f"Warning: {field} has an invalid data type.")
                    elif not document[field].strip():
                        print(f"Warning: {field} is empty.")
                kind = document.get("kind")

                if isinstance(kind, str) and kind not in ("Pod", "Namespace"):
                    print(f"Skipping unsupported resource kind: {kind}")
                    skipped_resources += 1
                    continue

                found_resource = True

                if "metadata" not in document:
                    print("Warning: Metadata is missing.")
                    metadata = {}
                else:
                    metadata = document.get("metadata")
                    if metadata is None:
                        print("Warning: Metadata is null.")
                        metadata = {}
                    elif not isinstance(metadata, dict):
                        print("Warning: Invalid metadata format. Expected a dictionary.")
                        metadata = {}
                    elif not metadata:
                        print("Warning: Metadata is empty.")

                if document.get("kind") == "Namespace":
                    table_rows.append([
                        "Namespace",
                        metadata.get("name", "Unknown"),
                        "Namespace",
                        "-",
                        "-",
                        "-",
                        "-",
                        "-"
                    ])


                if document.get("kind") == "Pod":
                    spec = document.get("spec")

                    if not isinstance(spec, dict):
                        print("Warning: Pod spec is missing or invalid. Skipping containers.")
                        containers = []
                    else:
                        containers = spec.get("containers", [])

                    if not isinstance(containers, list):
                        print("Warning: Invalid containers configuration. Skipping containers.")
                        containers = []
                    elif not containers:
                        print("Warning: No containers configured in this Pod.")

                    for container in containers:


                        if not isinstance(container, dict):
                            print("Warning: Invalid container entry. Skipping.")
                            continue


                        resources = container.get("resources", {})

                        if not isinstance(resources, dict):
                            resources = {}

                        requests = resources.get("requests", {})
                        limits = resources.get("limits", {})

                        if not isinstance(requests, dict):
                            requests = {}

                        if not isinstance(limits, dict):
                            limits = {}


                        table_rows.append([
                            "Pod",
                            metadata.get("namespace", "Not specified"),
                            metadata.get("name", "Unknown"),
                            container.get("name", "Unknown"),
                            requests.get("cpu", "[NONE]"),
                            limits.get("cpu", "[NONE]"),
                            requests.get("memory", "[NONE]"),
                            limits.get("memory", "[NONE]")

                        ])
            if table_rows:
                headers = [
                    "Kind",
                    "Namespace",
                    "Resource",
                    "Container",
                    "CPU Request",
                    "CPU Limit",
                    "Memory Request",
                    "Memory Limit"
                ]

                table_rows.sort(key=lambda row: (row[1], row[2]))

                print("\n--- Kubernetes Resource Summary ---")
                print(tabulate(table_rows, headers=headers, tablefmt="grid"))
            if not found_resource:
                print("No Kubernetes resources found in the file.")
            if skipped_resources > 0:
                    print(f"Total unsupported resources skipped: {skipped_resources}")



    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")


    except yaml.YAMLError as error:
        print(f"Invalid YAML: {error}")
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
    except OSError as error:
        print(f"File error: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Kubernetes Configuration Analyzer"
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="Kubernetes YAML files to analyze"
    )

    args = parser.parse_args()

    for file_path in args.files:
        analyze_file(file_path)


if __name__ == "__main__":
    main()


