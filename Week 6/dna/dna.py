import csv
import sys


def main():

    if (len(sys.argv) != 3):
        print("Usage: python dna.py xxxx.csv xxxx.txt")
        return 1

    strs_to_search, people = process_database(sys.argv[1])

    sequence = open_sequence(sys.argv[2])

    strs_biggest_sequences = [longest_match(sequence, str) for str in strs_to_search]

    for person in people:
        for i, str in enumerate(strs_biggest_sequences):
            if person["max_str_sequences"][i] != str:
                break
        else:
            print(person["name"])
            break
    else:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def process_database(csvFile):
    with open(csvFile) as database:
        database = database.read().splitlines()
        strs_to_Search = database[0].split(",")[1:]
        people = list(map(format_person, database[1:]))

        return [strs_to_Search, people]


def format_person(person):
    person = person.split(",")
    return {
        "name": person[0],
        "max_str_sequences": list(map(int, person[1:]))
    }


def open_sequence(sequenceFile):
    with open(sequenceFile) as sequence:
        sequence = sequence.read()
        return sequence


main()
