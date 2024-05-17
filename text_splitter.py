import math

def split_range_with_overlap(start, end):
    num_chunks = math.ceil(end / 2000)
    overlap_ratio = 0.3
    total_range = end - start
    chunk_size_no_overlap = total_range / num_chunks
    overlap_size = chunk_size_no_overlap * overlap_ratio
    chunk_size_with_overlap = chunk_size_no_overlap + overlap_size
    
    chunks = []
    
    for i in range(num_chunks):
        chunk_start = start + i * (chunk_size_no_overlap - overlap_size)
        chunk_end = chunk_start + chunk_size_with_overlap
        if chunk_end > end:
            chunk_end = end
        overlap_point = min(chunk_end, start + (i + 1) * (chunk_size_no_overlap - overlap_size))
        chunks.append((math.ceil(chunk_start), math.ceil(chunk_end), math.ceil(overlap_point)))
    
    if chunks and chunks[-1][1] < end:
        chunks[-1] = (chunks[-1][0], end, end)
    
    return chunks


def split_textto_chunks(text, chunks):
    chunked_texts = []
    
    for start, end, overlapping_point in chunks:
        chunked_texts.append(text[start:end])
    
    return chunked_texts

def calculate_offsets(chunks):
    offsets = [-1]
    for i in range(1, len(chunks)):
        offsets.append((chunks[i - 1][2])-1)
    return offsets

def adjust_offsets(entities, offset):
    for entity in entities:
        entity['start'] += offset
        entity['end'] += offset
    return entities

def remove_specific_entities(nested_list):
    entities_to_remove = {'I-MISC', 'I-ORG'}
    for sublist in nested_list:
        sublist[:] = [d for d in sublist if d.get('entity') not in entities_to_remove]
    
    return nested_list

def combine_entities(lists):
    filtered_entities = [
        entity for sublist in lists for entity in sublist 
        if entity['entity'] not in ['I-MISC', 'I-ORG']
    ]
    
    filtered_entities.sort(key=lambda x: (x['start'], -x['end']))
    unique_entities = {}
    prev_end = float('-inf')
    for entity in filtered_entities:
        if entity["start"] < prev_end:
            continue
        key = (entity["entity"], entity["start"], entity["end"])
        unique_entities[key] = entity
        prev_end = entity["end"]
    unique_entities_list = list(unique_entities.values())
    
    return unique_entities_list

def primary_handler(text):
    number_chunks = split_range_with_overlap(0, len(text))
    text_chunks = split_textto_chunks(text, number_chunks)
    return text_chunks, number_chunks

def secondary_handler(ner_info, chunks):
    ner_info = remove_specific_entities(ner_info)
    chunk_offset = calculate_offsets(chunks)

    for idx, value in enumerate(ner_info):
        ner_info[idx] = adjust_offsets(ner_info[idx], chunk_offset[idx])

    ner_info = combine_entities(ner_info)
    return ner_info