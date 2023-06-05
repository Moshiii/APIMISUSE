from difflib import SequenceMatcher

import json

path = "C:/@code/APIMISUSE/data/misuse_jsons/manual/merged_split_hunk_AST_filter_manual_deduplica_reduced_category.json"


with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())


def diff_substring_wrapper(string1, string2):

    longest_match = diff_substring(string1, string2)
    if longest_match == None:
        return "", ""

    string1_1 = string1.replace(longest_match, "")
    string2_1 = string2.replace(longest_match, "")
    longest_match = diff_substring(string1_1, string2_1)
    if longest_match == None:
        return string1_1, string2_1

    string1_2 = string1_1.replace(longest_match, "")
    string2_2 = string2_1.replace(longest_match, "")

    return string1_2, string2_2


def diff_substring(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    diff = matcher.find_longest_match(0, len(str1), 0, len(str2))

    if diff.size == 0:
        return None
    longest_match = str1[diff.a: diff.a + diff.size]
    return longest_match


pattern_list_pos = []
pattern_list_neg = []
neg_lines = []
pos_lines = []
for idx, x in enumerate(data):
    if x["label"] == "yes":
        neg_line = [x[1:] for x in x["neg_line"] if x[0] == "-"]
        pos_line = [x[1:] for x in x["pos_line"] if x[0] == "+"]
        if not len(neg_line) == 1 and len(pos_line) == 1:
            continue

        neg_line = [x.strip() for x in neg_line]
        pos_line = [x.strip() for x in pos_line]
        neg_line = " ".join(neg_line)
        pos_line = " ".join(pos_line)

        string1, string2 = diff_substring_wrapper(neg_line, pos_line)
        pattern_list_pos.append(string1)
        pattern_list_neg.append(string2)
        neg_lines.append(neg_line)
        pos_lines.append(pos_line)

print(len(pattern_list_pos))
print(len(pattern_list_neg))
print(len(neg_lines))
print(len(pos_lines))
