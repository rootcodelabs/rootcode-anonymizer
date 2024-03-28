# -*- coding: utf-8 -*-
class EntityGrouper:
    def group_words(self, entities):
        grouped_entities = []
        current_group = []

        for entity in entities:
            if not current_group or entity['start'] == current_group[-1]['end'] and entity['entity'] == current_group[-1]['entity']:
                current_group.append(entity)
            else:
                grouped_entities.append(current_group)
                current_group = [entity]

        if current_group:
            grouped_entities.append(current_group)

        return grouped_entities