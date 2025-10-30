from starter_preprocess import TextPreprocessor, FrequencyAnalyzer
import os
import json

# List of books
books = {
    "austen": "cleanedtext/austen_pride_prejudice.txt",
    "twain": "cleanedtext/twain_tom_sawyer.txt",
    "doyle": "cleanedtext/doyle_sherlock_holmes.txt"
}

def process_book(book_name, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()
    pre = TextPreprocessor()
    clean = pre.clean_gutenberg_text(raw)
    norm = pre.normalize_text(clean, preserve_sentences=True)

    sentences = pre.tokenize_sentences(norm)
    words = pre.tokenize_words(norm)
    chars = pre.tokenize_chars(norm)

    # Sentence statistics
    sentence_lengths = pre.get_sentence_lengths(sentences)
    stats = {
        "total_characters": len(chars),
        "total_words": len(words),
        "total_sentences": len(sentences),
        "avg_sentence_length": sum(sentence_lengths)/max(1, len(sentence_lengths))
    }

    # Analyze ngrams
    analyzer = FrequencyAnalyzer()
    results = {
        "word_unigram": analyzer.calculate_ngrams(words, 1),
        "word_bigram": analyzer.calculate_ngrams(words, 2),
        "word_trigram": analyzer.calculate_ngrams(words, 3),
        "char_unigram": analyzer.calculate_ngrams(chars, 1),
        "char_bigram": analyzer.calculate_ngrams(chars, 2),
        "char_trigram": analyzer.calculate_ngrams(chars, 3),
        "sentence_stats": stats
    }

    # Save frequency tables
    outdir = f"{book_name}_frequency_tables"
    os.makedirs(outdir, exist_ok=True)
    for key in results:
     with open(os.path.join(outdir, f"{key}.json"), "w", encoding="utf-8") as out:
        # If any keys are tuples (as in bigram/trigram dicts), convert them to strings
        if any(isinstance(k, tuple) for k in results[key].keys()):
            converted = {"||".join(k) if isinstance(k, tuple) else k: v for k, v in results[key].items()}
            json.dump(converted, out, ensure_ascii=False, indent=2)
        else:
            json.dump(results[key], out, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    for author, filename in books.items():
        process_book(author, filename)
