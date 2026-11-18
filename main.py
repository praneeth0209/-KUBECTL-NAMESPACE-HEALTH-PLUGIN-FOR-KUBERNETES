import argparse
import yaml


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            documents = yaml.safe_load_all(file)

            for document in documents:
                if document is None:
                    continue

                if not isinstance(document, dict):
                    print("Skipping invalid Kubernetes document.")
                    continue

                metadata = document.get("metadata") or {}

                print("\n--- Kubernetes Resource ---")
                print("Kind:", document.get("kind", "Unknown"))
                print("Name:", metadata.get("name", "Unknown"))
                print("Namespace:", metadata.get("namespace", "Not specified"))

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")

    except yaml.YAMLError as error:
        print(f"Invalid YAML: {error}")

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
    
    
