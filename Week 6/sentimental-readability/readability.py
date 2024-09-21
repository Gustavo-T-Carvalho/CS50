from cs50 import get_string


def main():
    text = get_string("Text: ")

    letters = countLetters(text)
    words = countWords(text)
    sentences = countSentences(text)
    index = calculateIndex(letters, words, sentences)
    if index > 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


def countLetters(text):
    return sum(c.isalpha() for c in text)


def countWords(text):
    return sum(c.isspace() for c in text) + 1


def countSentences(text):
    return len(list(filter(isSentencePontuation, text)))


def isSentencePontuation(c):
    return True if (c == '.' or c == '!' or c == '?') else False


def calculateIndex(letters, words, sentences):
    l = 100 * letters / words
    s = 100 * sentences / words
    return round(0.0588 * l - 0.296 * s - 15.8)


main()
