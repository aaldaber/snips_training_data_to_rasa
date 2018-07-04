from rasa_nlu.model import Interpreter
import json


def run_nlu():

    intent_wrong = 0
    total_intent = 0

    entity_wrong = 0
    entity_total = 0

    interpreter = Interpreter.load('./models/nlu/default/weathernlu')
    with open('data/new_validation_data_full.json', 'r', encoding='utf-8', errors='ignore') as f:
        data = json.loads(f.read())

    for each in data['rasa_nlu_data']['common_examples']:
        result = interpreter.parse(each['text'])

        total_intent += 1

        if result['intent']['name'] != each['intent']:
            print('Misclassified an intent for "{}" as {} instead of {}.'.format(each['text'],
                                                                                 result['intent']['name'],
                                                                                 each['intent']))
            intent_wrong += 1

        entity_dict = {}

        for eachentity in result['entities']:
            entity_dict[eachentity['value']] = eachentity['entity']

        for eachentity in each['entities']:
            if eachentity['value'] not in entity_dict:
                entity_wrong += 1
            elif eachentity['entity'] != entity_dict[eachentity['value']]:
                print('Misclassified an entity {} as {} instead of {}.'.format(eachentity['value'], entity_dict[eachentity['value']], eachentity['entity']))

            entity_total += 1

    print(total_intent)
    print(intent_wrong)

    print(entity_total)
    print(entity_wrong)


if __name__ == '__main__':
    run_nlu()
