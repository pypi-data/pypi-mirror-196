import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import random

# Custom data list for rephrasing
data = {
    "dog": ["puppy", "canine", "hound", "mutt", "pooch"],
    "happy": ["joyful", "content", "delighted", "pleased", "satisfied"],
    "running": ["jogging", "sprinting", "dashing", "galloping", "scurrying"],
    "sky": ["heaven", "firmament", "atmosphere", "celestial vault", "aether"],
    "tree": ["oak", "maple", "pine", "cedar", "willow"],
    "blue": ["azure", "sapphire", "turquoise", "cobalt", "indigo"],
    "good": ["great", "excellent", "fantastic", "terrific", "superb"],
    "bad": ["terrible", "horrible", "awful", "dreadful", "atrocious"],
}

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()


# Define function for rephrasing sentence
def rephrase_sentence(sentence):
    tokens = word_tokenize(sentence.lower())
    rephrased_tokens = []
    used_words = set()

    for token in tokens:
        # Get the base form of the word using lemmatization
        base_form = lemmatizer.lemmatize(token)
        # Check if the word is in the data list
        if base_form in data:
            # Get the part of speech of the original word
            pos = nltk.pos_tag([token])[0][1]
            # Choose a random rephrased word that has not been used before and is of the same part of speech
            rephrased_words = []
            for w in data[base_form]:
                w_synsets = wordnet.synsets(w)
                if not w_synsets:
                    continue
                w_pos = w_synsets[0].pos()
                if w_pos == pos and w not in used_words:
                    rephrased_words.append(w)
            if rephrased_words:
                rephrased_token = random.choice(rephrased_words)
                rephrased_tokens.append(rephrased_token)
                used_words.add(rephrased_token)
        else:
            rephrased_tokens.append(token)

    rephrased_sentence = " ".join(rephrased_tokens).capitalize() + "."

    return rephrased_sentence


# Example usage
original_sentence = "bravo , you did it broo"
rephrased_sentence = rephrase_sentence(original_sentence)
print(f"Original sentence: {original_sentence}")
print(f"Rephrased sentence: {rephrased_sentence}")
