import json
import re
from typing import List, Dict, Any
import spacy  # Assumes spaCy is installed with en_core_web_sm


class TopicExtractor:
    """
    Extracts valuable topics from chunks using NLP and RegEx.
    Provides evidence and recommendations for focus.
    """

    def __init__(self, chunks_path: str, context_window: int = 4096):
        self.chunks_path = chunks_path
        self.context_window = context_window
        self.chunks = []
        self.topics = []
        self._load_chunks()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"Warning: spaCy model not loaded: {e}. Using RegEx only.")
            self.nlp = None

    def _load_chunks(self):
        """Load chunks from JSON."""
        try:
            with open(self.chunks_path, "r") as f:
                data = json.load(f)
            self.chunks = data.get("chunks", [])
            print(f"Loaded {len(self.chunks)} chunks")
        except Exception as e:
            print(f"Error loading chunks: {e}")

    def extract_topics(self) -> List[Dict[str, Any]]:
        """Extract topics with evidence."""
        topics = []
        for i, chunk in enumerate(self.chunks):
            # Simple keyword extraction (RegEx for robotics)
            keywords = re.findall(
                r"\b(error|variance|odometry|depth|timestamp)\b", chunk, re.IGNORECASE
            )
            if self.nlp:
                doc = self.nlp(chunk)
                entities = [
                    ent.text
                    for ent in doc.ents
                    if ent.label_ in ["ORG", "PRODUCT", "EVENT"]
                ]
                topics.append(
                    {
                        "chunk_id": i,
                        "keywords": list(set(keywords)),
                        "entities": entities,
                        "evidence": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                        "recommendation": f"Focus on chunk {i} for {', '.join(set(keywords))}"
                        if keywords
                        else "General review",
                    }
                )
            else:
                topics.append(
                    {
                        "chunk_id": i,
                        "keywords": list(set(keywords)),
                        "evidence": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                        "recommendation": f"Focus on chunk {i} for {', '.join(set(keywords))}"
                        if keywords
                        else "General review",
                    }
                )
        self.topics = topics
        return topics

    def report(self) -> str:
        """Generate report with transparency."""
        report = f"Context Window: {self.context_window} tokens\n"
        report += f"Total Chunks: {len(self.chunks)}\n"
        report += f"Topics Extracted: {len(self.topics)}\n\n"
        for topic in self.topics[:5]:  # Limit for brevity
            report += f"Chunk {topic['chunk_id']}: {topic['recommendation']}\nEvidence: {topic['evidence']}\n\n"
        if len(self.topics) > 5:
            report += f"... and {len(self.topics) - 5} more topics.\n"
        report += "Full coverage evidenced by chunk-by-chunk processing."
        return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract topics from chunks with transparency."
    )
    parser.add_argument("--chunks", required=True, help="Path to chunks JSON")
    parser.add_argument("--window", type=int, default=4096, help="Context window size")
    parser.add_argument(
        "--output", default="topics_report.txt", help="Output report path"
    )
    args = parser.parse_args()

    extractor = TopicExtractor(args.chunks, args.window)
    topics = extractor.extract_topics()
    report = extractor.report()
    with open(args.output, "w") as f:
        f.write(report)
    print(report)
