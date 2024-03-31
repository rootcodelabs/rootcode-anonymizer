# -*- coding: utf-8 -*-
from ner_processer import NERProcessor
from entity_group import EntityGrouper
from regex_processor import RegexStringProcessor
import json

class NERProcessorController:
    def __init__(self):
        self.ner_processor = NERProcessor()
        self.entity_grouper = EntityGrouper()
        self.regex_processor = RegexStringProcessor()

    def process_sentence_list(self, sentence_rows_list):
        immutable_words = []
        try:
            with open('immutable_words.json', 'r', encoding='windows-1252') as f:
                data = json.load(f)
                if 'words' in data:
                    immutable_words = [word.lower() for word in data['words']]
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            print(f"Error: {e}. Assigning empty list to immutable_words.")

        modified_sentence_rows_list = []
        for row in sentence_rows_list:
            modified_row = []
            for sentence in row:
                sentence  = self.regex_processor.apply_regex_substitution(sentence)
                output = self.ner_processor.ner_with_word_and_most_frequent_entity(sentence)
                grouped_entities = self.entity_grouper.group_words(output)
                final_output = sentence
                offset = 0
                for entity in grouped_entities:
                    print("#$@#$@")
                    print(entity)
                    if entity[0]['word'].lower() not in immutable_words:
                        start_index = entity[0]['start'] + offset
                        end_index = entity[-1]['end'] + offset
                        final_output, adjustment = self.ner_processor.replace_substring(final_output, start_index, end_index, entity[0]['entity'])
                        offset += adjustment
                modified_row.append(final_output)
                print(modified_row)
            modified_sentence_rows_list.append(modified_row)
        return modified_sentence_rows_list