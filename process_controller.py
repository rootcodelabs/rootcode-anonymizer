# -*- coding: utf-8 -*-
import logging
from ner_processer import NERProcessor
from entity_group import EntityGrouper
from regex_processor import RegexStringProcessor
import json
import anonymizer_app
import datetime

class NERProcessorController:
    def __init__(self):
        self.ner_processor = NERProcessor()
        self.entity_grouper = EntityGrouper()
        self.regex_processor = RegexStringProcessor()
        logging.basicConfig(filename='anonymizer_log.log', level=logging.INFO)

    def calculate_progress_increment(self, list_size):
        if list_size == 0:
            return 1

        increment = 99 / list_size

        return increment    

    def process_sentence_list(self, sentence_rows_list, progress_bar):
        increment = self.calculate_progress_increment(len(sentence_rows_list))
        
        immutable_words = []
        error_log = []

        try:
            with open('immutable_words.json', 'r', encoding='windows-1252') as f:
                data = json.load(f)
                if 'words' in data:
                    immutable_words = [word.lower() for word in data['words']]
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            logging.error(f"Error: {e}. Assigning empty list to immutable_words.")

        modified_sentence_rows_list = []
        count = 0
        for index, row in enumerate(sentence_rows_list, start=1):
            try:
                count = count + increment
                progress_text = f'Processing {index} out of {len(sentence_rows_list)}'
                anonymizer_app.progress_bar_handler(progress_bar, int(count), progress_text)
                modified_row = []
                for sentence in row:
                    sentence  = self.regex_processor.apply_regex_substitution(sentence)
                    output = self.ner_processor.ner_with_word_and_most_frequent_entity(sentence)
                    grouped_entities = self.entity_grouper.group_words(output)
                    final_output = sentence
                    offset = 0
                    for entity in grouped_entities:
                        if entity[0]['word'].lower() not in immutable_words:
                            start_index = entity[0]['start'] + offset
                            end_index = entity[-1]['end'] + offset
                            final_output, adjustment = self.ner_processor.replace_substring(final_output, start_index, end_index, entity[0]['entity'])
                            offset += adjustment
                    modified_row.append(final_output)
                    logging.info(modified_row)
                modified_sentence_rows_list.append(modified_row)
            except Exception as e:
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                error_statement = f'Time : {formatted_datetime} | Data Row Number : {index} | Error : {e}'
                error_log.append(error_statement)
                logging.error(error_statement)

        anonymizer_app.progress_bar_handler(progress_bar, 100, "Anonymization Completed...")
        return modified_sentence_rows_list, error_log
