# -*- coding: utf-8 -*-
from transformers import AutoTokenizer, TFAutoModelForTokenClassification
from transformers import pipeline
from faker import Faker
from collections import Counter

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
        ner_results = self.classifier(sentence)
        
        word_results = []
        current_word = {"word": "", "start": None, "end": None, "entities": []}
        for token_result in ner_results:
            if token_result['entity']!='I-MISC':
                if token_result['word'].startswith('▁'):  
                    if current_word['word']:  
                        entity_counter = Counter([entity_result['entity'] for entity_result in current_word['entities']])
                        most_frequent_entity = entity_counter.most_common(1)[0][0]
                        word_results.append({"word": current_word['word'], "entity": most_frequent_entity, "start": current_word['start'], "end": current_word['end']})
                    current_word = {"word": token_result['word'][1:], "start": token_result['start'], "end": token_result['end'], "entities": [token_result]}
                else:
                    current_word['word'] += token_result['word']
                    current_word['end'] = token_result['end']
                    current_word['entities'].append(token_result)

        if current_word['word']:
            entity_counter = Counter([entity_result['entity'] for entity_result in current_word['entities']])
            most_frequent_entity = entity_counter.most_common(1)[0][0]
            word_results.append({"word": current_word['word'], "entity": most_frequent_entity, "start": current_word['start'], "end": current_word['end']})

        return word_results
