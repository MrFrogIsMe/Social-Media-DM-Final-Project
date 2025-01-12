import csv
import pandas as pd
import spacy
from collections import Counter

data = {
    'company': [],
    'title': [],
    'description': [],
}

filename = 'american_jobs.csv'

with open(filename, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        data['company'].append(row[0])
        data['title'].append(row[1])
        data['description'].append(row[2])

def extract_keywords(text):
    doc = nlp(text)
    keywords = set(ent.text for ent in doc.ents if ent.label_ not in ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'])
    return keywords

def split_keywords(keywords):
    split_results = []
    for word in keywords:
        if "/" in word:
            split_results.extend(word.split("/"))
        if "," in word:
            split_results.extend(word.split(","))
        else:
            split_results.append(word)
    return split_results

def clean_keywords(keywords):
    return [keyword.replace('\n', ' ').strip() for keyword in keywords]

def filter_keywords(keywords):
    keywords = split_keywords(keywords)
    keywords = clean_keywords(keywords)
    filtered_keywords = [word for word in keywords if len(word.split()) < 4]
    return filtered_keywords


keywords_set = set()
nlp = spacy.load("en_core_web_sm")
for raw_doc in data['title'][1:]:
    keywords = extract_keywords(raw_doc)
    filtered_keywords = filter_keywords(keywords)
    most_common = Counter(filtered_keywords).most_common()
    # print('RAW: ' + raw_doc)
    # for ent in doc.ents:
    #     print(ent.text, ent.label_)
    # for chunk in doc.noun_chunks:
    #     if chunk not in [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'GPE', 'WORK_OF_ART']]:
    #         print(chunk.text)
    # print("提取的關鍵字：", [v[0] for v in most_common])
    keywords_set.update(v[0] for v in most_common)

print()
print("提取的關鍵字：", keywords_set)

