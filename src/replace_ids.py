import os
import re
import shutil


def process_json_files(input_folder: str) -> None:
    # Create output folder
    output_folder = os.path.join(input_folder, "output")
    os.makedirs(output_folder, exist_ok=True)

    # Regex to match: "id": "some-uuid"
    id_pattern = re.compile(
        r'("id"\s*:\s*")[^"]+(")'
    )

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".json"):
            continue

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with open(input_path, "r", encoding="utf-8") as infile:
            content = infile.read()

        # Replace UUID part with literal "xxx"
        updated_content = id_pattern.sub(r'\1xxx\2', content)

        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(updated_content)


if __name__ == "__main__":
    folder_path = input("Enter the path to the input folder: ").strip()
    process_json_files(folder_path)