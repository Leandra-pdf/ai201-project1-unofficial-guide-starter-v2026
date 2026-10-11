"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into semantically coherent chunks.

    This strategy improves upon the default fixed-size fallback by respecting 
    natural paragraph boundaries (`\n\n`) and enforcing a minimum character 
    length threshold. 

    Algorithm:
      1. Splits each document into distinct paragraph blocks.
      2. Accumulates paragraphs sequentially, merging short text blocks 
         (such as standalone headings or single-sentence intros) with subsequent 
         paragraphs until the minimum length threshold (~150 characters) is met.
      3. Handles edge cases where trailing fragments are appended to the prior 
         chunk to maintain sentence and thought integrity.
      4. Tags every generated chunk with 'chunker.py::split_documents'.

    Args:
        documents (list[Document]): The raw loaded documents from the corpus.

    Returns:
        list[Chunk]: A filtered and structured list of Chunk objects ready for embedding.
    """
    chunks: list[Chunk] = []
    min_length = 150  # Matches my criteria target

    for doc in documents:
        # Split document into paragraphs
        raw_paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
        
        if not raw_paragraphs:
            continue

        index = 0
        current_chunk_text = ""

        for para in raw_paragraphs:
            # If current accumulation is empty, start with this paragraph
            if not current_chunk_text:
                current_chunk_text = para
            else:
                # If adding this paragraph keeps it reasonable, or if the current chunk is too short, combine them
                if len(current_chunk_text) < min_length:
                    current_chunk_text += "\n\n" + para
                else:
                    # Current chunk is long enough, save it and start a new one
                    chunks.append(
                        Chunk(
                            text=current_chunk_text,
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                    current_chunk_text = para

        if current_chunk_text:
            # If the very last chunk is a tiny fragment and we have previous chunks, append it to the last chunk
            if len(current_chunk_text) < min_length and chunks and chunks[-1].source == doc.source:
                chunks[-1].text += "\n\n" + current_chunk_text
            else:
                chunks.append(
                    Chunk(
                        text=current_chunk_text,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
