import json
import random

class TextGenerator:
    def __init__(self, ngram_json_path, n=1, token_type="word"):
        # Load ngram frequencies from json file
        with open(ngram_json_path, "r", encoding="utf-8") as f:
            freq_raw = json.load(f)
        self.n = n
        self.token_type = token_type
        if self.n == 1:
            self.freq_table = freq_raw
            self.ngrams = list(self.freq_table.keys())
        else:
            # Convert keys like "word1||word2" to tuples ("word1", "word2")
            self.freq_table = {tuple(k.split('||')): v for k, v in freq_raw.items()}
            self.ngrams = list(self.freq_table.keys())

    def generate_text(self, length=50):
        random.seed()
        output = []

        if self.n == 1:
            items, counts = zip(*self.freq_table.items())
            total = sum(counts)
            weights = [cnt / total for cnt in counts]
            for _ in range(length):
                output.append(random.choices(items, weights=weights)[0])
        else:
            # Start with a random ngram tuple
            curr = random.choice(self.ngrams)
            output.extend(list(curr))

            for _ in range(length - self.n):
                # Look for n-grams that continue current output
                prev = tuple(output[-(self.n-1):])
                candidates = [ng for ng in self.ngrams if ng[:self.n-1] == prev]
                if candidates:
                    next_ngram = random.choice(candidates)
                    output.append(next_ngram[-1])
                    curr = next_ngram
                else:
                    # Restart with a new random n-gram if no candidate found
                    curr = random.choice(self.ngrams)
                    output.extend(list(curr))

        if self.token_type == "word":
            return " ".join(output[:length])
        else:
            return "".join(output[:length])

# Example usage
if __name__ == "__main__":
    generator = TextGenerator("austen_frequency_tables/word_bigram.json", n=2, token_type="word")
    sample = generator.generate_text(length=20)
    print("Generated Text:\n", sample)
