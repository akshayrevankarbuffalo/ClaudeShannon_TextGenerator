import argparse
from generator import TextGenerator

author_dirs = {
    "austen": "austen_frequency_tables",
    "twain": "twain_frequency_tables",
    "doyle": "doyle_frequency_tables"
}

ngram_files = {
    "word1": "word_unigram.json",
    "word2": "word_bigram.json",
    "word3": "word_trigram.json",
    "char1": "char_unigram.json",
    "char2": "char_bigram.json",
    "char3": "char_trigram.json"
}

def main():
    parser = argparse.ArgumentParser(description="Shannon English Generator (Assignment 3)")
    parser.add_argument("--author", type=str, choices=["austen","twain","doyle"], required=True, help="Author/model to use")
    parser.add_argument("--type", type=str, choices=["word","char"], default="word", help="Word or character based model")
    parser.add_argument("--order", type=int, choices=[1,2,3], default=2, help="N-gram order (1=unigram, 2=bigram, 3=trigram)")
    parser.add_argument("--length", type=int, default=50, help="Length of output (words/chars)")
    parser.add_argument("--outfile", type=str, default="", help="Output file (optional)")

    args = parser.parse_args()
    author_dir = author_dirs[args.author]
    ngram_key = f"{args.type}{args.order}"
    ngram_path = f"{author_dir}/{ngram_files[ngram_key]}"

    generator = TextGenerator(ngram_path, n=args.order, token_type=args.type)
    sample = generator.generate_text(length=args.length)

    print(f"\n=== Generated Text ({args.author}, {args.type}-{args.order}) ===\n")
    print(sample)

    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            f.write(sample)
        print(f"\nOutput saved to {args.outfile}")

if __name__ == "__main__":
    main()
