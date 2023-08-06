from examon_core.examon_item import examon_item


@examon_item(choices=[
    'Hello, Bob. How are you?', 'Hello, Jeff. How are you?',
    'Hello, Bob.', 'Hello, Jeff.', '. How are you?'],
    tags=['strings', 'beginner'])
def question():
    name = 'Jeff'
    name = 'Bob'
    greeting = f'Hello, {name}'
    greeting += ". How are you?"
    return greeting


@examon_item(choices=[
    'Hello', 'Hell',
    'Hello,', ['H', 'e', 'l', 'l', 'o']],
    tags=['strings', 'slicing', 'beginner'])
def question():
    greeting = 'Hello, how are you'
    return greeting[0:5]


@examon_item(choices=[
    'j', 'jk', 'ba'],
    tags=['strings', 'slicing', 'beginner'])
def question():
    letters = 'abcdefghijk'
    return letters[-2:]


@examon_item(choices=[
    'Hello, {name} you are {(23)}',
    'Hello, Bob you are (23)',
    'Hello, Bob you are 23'
],
    tags=['strings', 'interpolation', 'beginner'])
def question():
    name = 'Bob'
    return f'Hello, {name} you are {(23)}'


@examon_item(choices=[
    [True, True],
    [False, True],
    [True, False],
    [False, False],
], tags=['equality', 'dict', 'beginner'])
def question():
    my_object = {'name': 'bob'}
    new_ref = my_object
    return [
        my_object is new_ref,
        my_object is {'name': 'bob'}
    ]


@examon_item(choices=[
    ['the', 'cat', 'in', 'the', 'hat'], []
], tags=['array', 'for', 'if', 'beginner'])
def question():
    words = ['the', 'cat', 'in', 'the', 'hat']

    new_words = []
    for w in words:
        if (len(w) > 2):
            new_words.append(w)

    return new_words
