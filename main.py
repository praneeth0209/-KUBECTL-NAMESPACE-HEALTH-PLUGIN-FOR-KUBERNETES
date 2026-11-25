import argparse
import json
import yaml


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

                print("\n--- Kubernetes Resource ---")
                print("Kind:", document.get("kind", "Unknown"))
                print("Name:", metadata.get("name", "Unknown"))
                print("Namespace:", metadata.get("namespace", "Not specified"))
            
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
    
    
