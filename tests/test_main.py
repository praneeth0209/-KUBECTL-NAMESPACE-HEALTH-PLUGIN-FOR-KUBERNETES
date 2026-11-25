import unittest
import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import analyze_file


class TestKubernetesAnalyzer(unittest.TestCase):

    @patch("builtins.print")
    def test_valid_pod_yaml(self, mock_print):
        analyze_file("samples/valid_pod.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Pod", output)
        self.assertIn("test-pod", output)
        self.assertIn("testing", output)
    @patch("builtins.print")
    def test_valid_pod_json(self, mock_print):
        analyze_file("samples/valid_pod.json")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Pod", output)
        self.assertIn("test-pod", output)
        self.assertIn("testing", output)

    @patch("builtins.print")
    def test_multiple_containers(self, mock_print):
        analyze_file("samples_2/04_multiple_containers.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("frontend", output)
        self.assertIn("backend", output)

    @patch("builtins.print")
    def test_missing_resources(self, mock_print):
        analyze_file("samples_2/02_missing_resources.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("[NONE]", output)

    @patch("builtins.print")
    def test_zero_resources(self, mock_print):
        analyze_file("samples_2/03_zero_resources.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("CPU Request", output)
        self.assertIn("CPU Limit", output)
        self.assertIn("Memory Request", output)
        self.assertIn("Memory Limit", output)
        self.assertNotIn("[NONE]", output)
        self.assertIn("0", output)

    @patch("builtins.print")
    def test_missing_limits(self, mock_print):
        analyze_file("samples_2/05_missing_limits.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("CPU Request", output)
        self.assertIn("Memory Request", output)
        self.assertIn("[NONE]", output)

    @patch("builtins.print")
    def test_valid_namespace(self, mock_print):
        analyze_file("samples_2/07_valid_namespace.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Namespace", output)
        self.assertIn("production", output)

    @patch("builtins.print")
    def test_invalid_pod_spec(self, mock_print):
        analyze_file("samples_2/08_invalid_pod.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Warning", output)
        self.assertIn("invalid", output.lower())


    @patch("builtins.print")
    def test_missing_pod_spec(self, mock_print):
        analyze_file("samples_2/09_missing_spec.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Pod spec is missing or invalid", output)
        self.assertIn("Warning", output)
        self.assertIn("Pod spec is missing or invalid", output)


    @patch("builtins.print")
    def test_multiple_resources(self, mock_print):
        analyze_file("samples_2/10_multiple_resources.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("first-pod", output)
        self.assertIn("second-pod", output)
        self.assertIn("Namespace", output)
        self.assertIn("development", output)
        self.assertIn("nginx", output)
        self.assertIn("redis", output)


    @patch("builtins.print")
    def test_file_not_found(self, mock_print):
        analyze_file("samples_2/does_not_exist.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Error: File not found", output)

    @patch("builtins.print")
    def test_unsupported_file_format(self, mock_print):
        analyze_file("README.md")


        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Unsupported file format", output)

    @patch("builtins.print")
    def test_malformed_yaml(self, mock_print):
        analyze_file("samples_2/11_malformed_yaml.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Invalid YAML", output)

    @patch("builtins.print")
    def test_invalid_json(self, mock_print):
        analyze_file("samples_2/12_invalid_json.json")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Invalid JSON", output)

    @patch("builtins.print")
    def test_permission_error(self, mock_print):
        with patch(
            "builtins.open",
            side_effect=PermissionError("Permission denied")
        ):
            analyze_file("samples_2/01_valid_pod.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("File error", output)
        self.assertIn("Permission denied", output)


    @patch("builtins.print")
    def test_invalid_documents(self, mock_print):
        analyze_file("samples_2/13_invalid_documents.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Skipping invalid Kubernetes document", output)

    @patch("builtins.print")
    def test_missing_apiversion(self, mock_print):
        analyze_file("samples_2/14_missing_apiversion.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("apiVersion is missing", output)

    @patch("builtins.print")
    def test_null_apiversion(self, mock_print):
        analyze_file("samples_2/15_null_apiversion.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("apiVersion is null", output)

    @patch("builtins.print")
    def test_invalid_apiversion_type(self, mock_print):
        analyze_file("samples_2/16_invalid_apiversion_type.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("apiVersion has an invalid data type", output)

    @patch("builtins.print")
    def test_empty_apiversion(self, mock_print):
        analyze_file("samples_2/17_empty_apiversion.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("apiVersion is empty", output)


    @patch("builtins.print")
    def test_missing_metadata(self, mock_print):
        analyze_file("samples_2/18_missing_metadata.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Metadata is missing", output)


    @patch("builtins.print")
    def test_unsupported_resource_kind(self, mock_print):
        analyze_file("samples_2/19_unsupported_kind.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Service", output)

    @patch("builtins.print")
    def test_null_metadata(self, mock_print):
        analyze_file("samples_2/20_null_metadata.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Metadata", output)

    @patch("builtins.print")
    def test_invalid_metadata_format(self, mock_print):
        analyze_file("samples_2/21_invalid_metadata.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Invalid metadata format", output)

    @patch("builtins.print")
    def test_empty_metadata(self, mock_print):
        analyze_file("samples_2/22_empty_metadata.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Metadata is empty", output)

    @patch("builtins.print")
    def test_invalid_containers_configuration(self, mock_print):
        analyze_file("samples_2/23_invalid_containers.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Invalid containers configuration", output)

    @patch("builtins.print")
    def test_invalid_container_entry(self, mock_print):
        analyze_file("samples_2/24_invalid_container_entry.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("Invalid container entry", output)



    @patch("builtins.print")
    def test_invalid_resource_sections(self, mock_print):
        analyze_file("samples_2/25_invalid_resource_sections.yaml")

        output = " ".join(
            str(call) for call in mock_print.call_args_list
        )

        self.assertIn("invalid-resource-sections", output)
        self.assertIn("invalid-resources", output)
        self.assertIn("invalid-requests", output)
        self.assertIn("invalid-limits", output)








if __name__ == "__main__":
    unittest.main()
