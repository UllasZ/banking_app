import csv
import json
import os
import shutil
from typing import List, Union

import pandas as pd
from dataclasses import dataclass

from src.banking_app.utils.utils import utils


@dataclass
class FileOperator:
    filepath: str = None
    folder_path: str = None
    data: Union[str, List] = None
    directory: str = None

    def list_files(self) -> List[str]:
        """List all files in the specified directory."""
        if not self.directory:
            raise ValueError("Directory path not provided.")
        try:
            return os.listdir(self.directory)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Directory does not exist: {self.directory}") from e

    def compress_folder(self) -> str:
        """Compress the specified folder into a zip archive."""
        try:
            shutil.make_archive(self.filepath, "zip", self.filepath)
            return f"Folder compressed successfully: {self.filepath}.zip"
        except Exception as e:
            raise IOError(f"Error compressing folder {self.filepath}: {e}") from e

    def create_folder(self) -> str:
        """Create the folder if it doesn't exist."""
        self.folder_path = self.folder_path or os.path.dirname(self.filepath)
        try:
            os.makedirs(self.folder_path, exist_ok=True)
            return f"Directory created successfully: {self.folder_path}"
        except OSError as e:
            raise IOError(f"Error creating directory {self.folder_path}: {e}") from e

    def read(self) -> Union[List[dict], str]:
        """Read contents of the file based on the file type."""
        if not self.filepath:
            raise ValueError("Filepath not provided.")
        if self.filepath.endswith(".json"):
            return self._read_json()
        elif self.filepath.endswith(".csv"):
            return self._read_csv()
        elif self.filepath.endswith(".xlsx"):
            return self._read_xlsx()
        elif self.filepath.endswith(".sql"):
            return self._read_sql()
        else:
            raise ValueError("Unsupported file type.")

    def write(self) -> None:
        """Write data to the file based on the file type."""
        if not self.filepath:
            raise ValueError("Filepath not provided.")
        self.create_folder()

        if self.filepath.endswith(".json"):
            self._write_json()
        elif self.filepath.endswith(".csv"):
            self._write_csv()
        elif self.filepath.endswith(".sql"):
            self._write_sql()
        elif self.filepath.endswith(".xlsx"):
            self._write_xlsx()
        else:
            raise ValueError("Unsupported file type.")

    def _read_json(self) -> List[dict]:
        """Read data from a JSON file."""
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File does not exist: {self.filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in file {self.filepath}: {e}") from e

    def _read_csv(self) -> List[dict]:
        """Read data from a CSV file."""
        try:
            with open(self.filepath, "r") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            raise FileNotFoundError(f"File does not exist: {self.filepath}")

    def _read_sql(self) -> str:
        """Read SQL content from a file."""
        try:
            with open(self.filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File does not exist: {self.filepath}")

    def _read_xlsx(self) -> List[dict]:
        """Read data from an Excel file."""
        try:
            df = pd.read_excel(self.filepath)
            return df.to_dict(orient="records")
        except FileNotFoundError:
            raise FileNotFoundError(f"File does not exist: {self.filepath}")
        except Exception as e:
            raise ValueError(f"Error reading Excel file {self.filepath}: {e}") from e

    def _write_json(self) -> None:
        """Write data to a JSON file, merging with existing data if present."""
        try:
            with open(self.filepath, "r") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        with open(self.filepath, "w") as file:
            all_data = existing_data + (self.data or [])
            json.dump(all_data, file, indent=4)

    def _write_csv(self) -> None:
        """Write data to a CSV file, appending if it exists."""
        try:
            with open(self.filepath, "r", newline="") as file:
                reader = csv.DictReader(file)
                existing_data = list(reader)
        except FileNotFoundError:
            existing_data = []

        if not self.data:
            raise ValueError("No data provided to write to CSV.")

        fieldnames = self.data[0].keys()

        with open(self.filepath, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not existing_data:
                writer.writeheader()
            writer.writerows(existing_data)
            writer.writerows(self.data)

    def _write_sql(self) -> None:
        """Write data to a SQL file, appending SQL statements."""
        with open(self.filepath, "a+") as file:
            if self.data:
                file.write(f"{self.data};\n")
            elif self.data:
                for data in self.data:
                    file.write(f"{data};\n")
            else:
                raise ValueError("No data provided to write to SQL file.")

    def _write_xlsx(self) -> None:
        """Write data to an Excel file, appending if it exists."""
        try:
            existing_data = pd.read_excel(self.filepath)
        except FileNotFoundError:
            existing_data = pd.DataFrame()

        if not self.data:
            raise ValueError("No data provided to write to Excel.")

        cleaned_data = utils.clean_list_of_dicts(self.data)
        new_data = pd.DataFrame(cleaned_data)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        combined_data.to_excel(self.filepath, index=False)