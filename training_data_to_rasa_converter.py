import json

list_of_files = ['train_AddToPlaylist_full.json', 'train_BookRestaurant_full.json', 'train_GetWeather_full.json',
                 'train_PlayMusic_full.json', 'train_RateBook_full.json', 'train_SearchCreativeWork_full.json',
                 'train_SearchScreeningEvent_full.json']

rasa_data = {"rasa_nlu_data": {"common_examples": []}
             }

for eachfile in list_of_files:

    with open(eachfile, mode='r', encoding="utf-8", errors='ignore') as f:
        the_data = json.loads(f.read())

    all_entities = set()

    for eachkey, eachv in the_data.items():
        for eachvalue in eachv:
            sentence = ''
            entities = []
            running_length = 0
            for oneitem in eachvalue['data']:
                sentence += oneitem['text']
                if oneitem.get('entity'):
                    all_entities.add(oneitem['entity'])
                    entities.append({'start': running_length, 'end': running_length + len(oneitem['text']),
                                     'value': oneitem['text'], 'entity': oneitem['entity']})
                running_length += len(oneitem['text'])

            rasa_data['rasa_nlu_data']['common_examples'].append({"text": sentence, 'intent': eachkey,
                                                                  'entities': entities})

        print('List of entities for file {}'.format(eachfile))
        print(list(all_entities))

with open('snips_training_data_full.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(rasa_data))
