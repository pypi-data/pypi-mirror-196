import argparse
import random

import emoji

def create_parser():
    parser = argparse.ArgumentParser(description='Taehoon\'s CLI')
    parser.add_argument('greeting', help='The type of greeting')
    parser.add_argument('-n', '--name', help='The name of the person')
    parser.add_argument('-a', '--age', help='The age of the person')
    return parser

def random_emoji():
    emojis = [':thumbs_up:', ':thumbs_down:', ':fire:']
    random_index = random.randint(0, len(emojis) - 1)
    return emoji.emojize(emojis[random_index])

def build_message(greeting, name, age, emoji):
    return '{} {} in {} years old. {}'.format(greeting.capitalize(), name, age, emoji)

def main():
    parser = create_parser()
    args = parser.parse_args()

    # build message
    msg = build_message(args.greeting, args.name, args.age, random_emoji())
    
    # print out
    print(msg)

if __name__ == '__main__':
    main()
