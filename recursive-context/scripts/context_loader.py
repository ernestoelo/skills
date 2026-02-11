import json
from typing import List


class ContextManager:
    """
    Simulates the RLM Environment: Loads large files externally without saturating context.
    Divides into chunks for iterative processing.
    """

    def __init__(
        self, file_path: str, chunk_size: int = 5000, problem_type: str = None
    ):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.content = ""
        self.metadata = {}
        self.problem_type = problem_type  # e.g., "robotics-log"
        self._load_and_chunk()

    def _load_and_chunk(self):
        """Load file and extract metadata."""
        try:
            if self.file_path.endswith(".pdf"):
                # Integrate pdf skill: Use pdftotext for text extraction (handles scanned PDFs too)
                import subprocess

                result = subprocess.run(
                    ["pdftotext", self.file_path, "-"], capture_output=True, text=True
                )
                if result.returncode == 0:
                    self.content = result.stdout
                    print("PDF text extracted successfully using pdftotext.")
                else:
                    print(
                        f"PDF extraction failed: {result.stderr}. Ensure pdftotext is installed (from pdf skill)."
                    )
                    self.content = ""
            else:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.content = f.read()
            self.metadata = {
                "length": len(self.content),
                "structure": "pdf" if self.file_path.endswith(".pdf") else "text",
                "first_lines": self.content[:200].split("\n")[:5]
                if self.content
                else [],
                "last_lines": self.content[-200:].split("\n")[-5:]
                if self.content
                else [],
            }
            print(
                f"[RLM Environment] Loaded {self.metadata['length']} chars from {self.file_path}"
            )
        except Exception as e:
            print(f"Error loading file: {e}")

    def get_chunks(self) -> List[str]:
        """Return list of chunks."""
        if not self.content:
            return []
        return [
            self.content[i : i + self.chunk_size]
            for i in range(0, len(self.content), self.chunk_size)
        ]

    def to_json(self, output_path: str):
        """Export chunks and metadata to JSON."""
        data = {"metadata": self.metadata, "chunks": self.get_chunks()}
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Chunks saved to {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Load and chunk large files for RLM processing."
    )
    parser.add_argument("--input", required=True, help="Path to input file")
    parser.add_argument("--output", default="chunks.json", help="Output JSON path")
    parser.add_argument(
        "--chunk-size", type=int, default=5000, help="Chunk size in characters"
    )
    parser.add_argument("--type", help="Problem type (e.g., robotics-log)")
    args = parser.parse_args()

    cm = ContextManager(args.input, args.chunk_size, args.type)
    cm.to_json(args.output)
