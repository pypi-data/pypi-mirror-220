from examon_core.examon_item import examon_item


@examon_item(choices=[
    'Hello, Bob. How are you?', 'Hello, Jeff. How are you?',
    'Hello, Bob.', 'Hello, Jeff.', '. How are you?'],
    tags=['strings'])
def question_1():
    name = 'Jeff'
    name = 'Bob'
    greeting = f'Hello, {name}'
    greeting += ". How are you?"
    return greeting


@examon_item(choices=[
    'Hello', 'Hell',
    'Hello,', ['H', 'e', 'l', 'l', 'o']],
    tags=['strings', 'slicing'])
def question_1():
    greeting = 'Hello, how are you'
    return greeting[0:5]
