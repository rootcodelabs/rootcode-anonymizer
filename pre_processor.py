def find_phrases_in_braces(input_string):
    phrases_list = []
    start = -1
    
    for i, char in enumerate(input_string):
        if char == '{':
            start = i + 1
        elif char == '}':
            if start != -1:
                phrases_list.append({
                    'phrase': input_string[start-1:i+1],
                    'start': start-1,
                    'end': i
                })
            start = -1
    
    return phrases_list

def compare_phrases(phrases_info):
    if len(phrases_info) <= 1:
        return []

    tag_list = []

    for i in range(len(phrases_info) - 1):
        colon_index = phrases_info[i]['phrase'].find(":")

        if colon_index != -1:
            first_output = phrases_info[i]['phrase'][1:colon_index]
            second_output = phrases_info[i+1]['phrase'][1:-1]
            if first_output == second_output:
                tag_list.append(phrases_info[i])
                tag_list.append(phrases_info[i+1])

    return tag_list

def delete_phrases_from_string(input_string, phrases_info):
    phrases_info.sort(key=lambda x: x['start'], reverse=True)

    for phrase_info in phrases_info:
        start = phrase_info['start']
        end = phrase_info['end']
        input_string = input_string[:start] + input_string[end+1:]

        for other_phrase_info in phrases_info:
            if other_phrase_info['start'] > start:
                offset = end - start + 1
                other_phrase_info['start'] -= offset
                other_phrase_info['end'] -= offset
    return input_string

def pre_processor(input_string):
    pre_processing_result = find_phrases_in_braces(input_string)
    if len(pre_processing_result) > 0:
        compare_result = compare_phrases(pre_processing_result)
        if len(compare_result) > 0:
            pre_processed_output = delete_phrases_from_string(input_string, compare_result)
        else:
            pre_processed_output = input_string
    else:
        pre_processed_output = input_string
    return(pre_processed_output)
