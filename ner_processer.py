# -*- coding: utf-8 -*-
from transformers import AutoTokenizer, TFAutoModelForTokenClassification
from transformers import pipeline
from faker import Faker
from collections import Counter
import text_splitter

class NERProcessor:
    def __init__(self):
        self.model_name = "NER_basemodel"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = TFAutoModelForTokenClassification.from_pretrained(self.model_name)
        self.classifier = pipeline("ner", model=self.model, tokenizer=self.tokenizer)

    def get_fake_entity(self, entity_type):
        fake = Faker()
        if entity_type == 'PER':
            return fake.name()
        elif entity_type == 'ORG':
            return fake.company()
        elif entity_type == 'LOC':
            return fake.country()

    def replace_substring(self, original_string, start_index, end_index, entity):
        replacement = self.get_fake_entity(entity[-3:])
        if replacement is None:
            return original_string, 0
        adjusted_string = original_string[:start_index] + replacement + original_string[end_index:]
        adjustment = len(replacement) - (end_index - start_index)
        return adjusted_string, adjustment

    def ner_with_word_and_most_frequent_entity(self, sentence):
        if len(sentence)>2000:
            splitted_text, number_chunks = text_splitter.primary_handler(sentence)
            ner_results = []
            for text in splitted_text:
                ner_results.append(self.classifier(text))
            ner_results = text_splitter.secondary_handler(ner_results, number_chunks)
        else:
            ner_results = self.classifier(sentence)

        if ner_results != []:
            ner_results_processed = []
            ner_results_currant = []
            for result in ner_results:
                if ner_results_currant == []:
                    ner_results_currant.append(result)
                else:
                    if result['start'] == ner_results_currant[-1]["end"]:
                        ner_results_currant.append(result)
                    else:
                        ner_results_processed.append(ner_results_currant)
                        ner_results_currant = [result]
            ner_results_processed.append(ner_results_currant)

            word_results = []

            for entity_word in ner_results_processed:
                current_word = {"word": None, "start": None, "end": None, "entity": None}
                entity_count = Counter(token['entity'] for token in entity_word)
                most_frequent_entity = entity_count.most_common(1)[0][0]
                current_word["entity"] = most_frequent_entity
                for token in entity_word:
                    if current_word["word"] is None:
                        if token['word'].startswith('▁'):
                            current_word["word"] = token['word'][1:]
                        else:
                            current_word["word"] = token['word']
                    else:
                        current_word['word'] += token['word']
                    if current_word["start"] is None or current_word["start"]>token['start']:
                        current_word["start"] = token['start']
                    if current_word["end"] is None or current_word["end"]<token['end']:
                        current_word["end"] = token['end']
                word_results.append(current_word)
        else:
            word_results = []
        

        return word_results
