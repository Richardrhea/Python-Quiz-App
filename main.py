
import json
import os
import random

class Quiz():
    """ Represents a Quiz based on the compiled data and a specified topic """

    def __init__(self, topic_id, compiled_data, questions):
        """ Initializes the Quiz instance """

        self.topic_id = topic_id
        self.compiled_data = compiled_data
        self.questions = questions
        self.questions_to_ask = compiled_data[topic_id]['question-ids']

        # Use the random module to randomize the order of the questions to ask
        random.shuffle(self.questions_to_ask)

    def run_quiz(self):
        """ Class method to run the Quiz and returns the score and the range_size (number of questions asked) """   

        # Define score to start at 0 and increases with each correct answer
        score = 0

        # Define range_size as the number of questions to be asked, maxing out at 10 to keep the quiz short
        range_size = min(10, len(self.questions_to_ask))
        for index in range(range_size):
            current_question = self.questions.get(self.questions_to_ask[index])
            clear()

            # The ask_question function runs and returnss True/False for a(n) correct/incorrect answer, if correct increase the score by 1.
            if ask_question(current_question, index + 1, range_size):
                score += 1
            input('enter any key to continue ')

        return score, range_size
    
def ask_question(question, question_number, total_questions):
    """ Asks the question passed into the user and returns True/False if answered correctly/incorrectly """

    # Create an empty list that will be populated with the question's options and then shuffled
    options = []
    for option in question['options'].values():
        options.append(option)
    random.shuffle(options)

    # Create a tuple with the first 7 letters of the alphabet
    letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g')

    # The shuffled_options dictionary will have the options in random order
    shuffled_options = {}
    for index in range(len(options)):
        shuffled_options[letters[index]] = options[index]

    # Print the question prompt
    print(f' - ({question_number}/{total_questions}) {question["question"]}')

    # Print shuffled_options for the user to choose from
    for key, value in shuffled_options.items():
        print(f'\t{key}. {value}')

    # Define the correct_answer from the questions object
    correct_answer = question['options'][question['answer']]

    # Prompt user for input by using the validated_input function
    user_input = validated_input('Enter your answer (\'q\' to quit): ', list(shuffled_options.keys()))

    # Define the user_answer from the shuffled_options
    user_answer = shuffled_options[user_input]

    # Compare answers to determine if correct/incorrect and return True/False respectively
    if user_answer == correct_answer:
        print('\nThat\'s correct! Good Job!\n')
        return True
    else:
        print(f'\nYou almost got it! The right answer was "{correct_answer}".\n')
        return False

def load_json_files(*file_names):
    """ Receives one or more file names and returns a list of
    dictionaries, each dictionary representing the contents of
    each file."""

    resulting_loads = []
    for file in file_names:
        with open(file) as file_object:
            current_load = json.load(file_object)
            resulting_loads.append(current_load)

    return resulting_loads

def create_compiled_data(questions, topics, past_scores):
    """ Create compiled data from the contents loaded from the
    questions, topics, and past_scores files """

    compiled_data = {}
    for number, topic in topics.items():
        compiled_data[number] = { 'topic': topic }

    compiled_data[str(len(compiled_data) + 1)] = { 'topic' : 'all' }
    for data_key, data_value in compiled_data.items():

        data_value["question-ids"] = []
        if data_value["topic"] != 'all':
            for key, value in questions.items():
                if data_value["topic"] in value["topics"]:
                    data_value["question-ids"].append(key)
        else:
            for key, value in questions.items():
                data_value["question-ids"].append(key)

        data_value['questions-count'] = len(data_value['question-ids'])
        data_value['past_scores'] = past_scores.get(data_key)

    return compiled_data

def clear():
    """ Clears the terminal """

    # This is a shorthand if statement. If the OS is Windows os.name
    arg = 'cls' if os.name == 'nt' else 'clear'

    # Use the system() function from the OS library to clear the terminal
    os.system(arg)
   
def print_welcome_page(compiled_data):
    """ Takes in the compiled_data and does some formatting to print the welcome page to the app """

    table_titles = ['topic', 'questions', 'previous score']
    # Define the length of the longest title (for table sizing later on)
    max_length = len(max(table_titles, key=len))
    
    # Compare max title length to topics lengths to determine which one to use (+4 because of the numerati)
    for value in compiled_data.values():
        if len(value['topic']) + 4 > max_length:
            max_length = len(value['topic']) + 4

    print('Welcome to your Python Learning App!\n')
    print('Select a topic to review and you will be asked a max of 10 questions per run. Good luck!\n')

    # Print table titles
    print('| {0:^{max_length}} | {1:^{max_length}} | {2:^{max_length}} |'
        .format(
            table_titles[0].title(),
            table_titles[1].title(),
            table_titles[2].title(),
            max_length=max_length)  
        )

    # Print table rows
    for key, value in compiled_data.items():
        print('| {0:{max_length}} | {1:^{max_length}} | {2:^{max_length}} |'
              .format(
                  f'{key}. {value["topic"].title()}',
                  value['questions-count'],
                  value.get('past_scores', '') or '',
                  max_length=max_length)
              )
    
def validated_input(prompt, valid_options, value_to_quit='q'):

    # Prompt the user for input
    user_input = input(prompt)
    # Iterate through the while loop until the user_input is valid (and return valid input), or if the
    flag = True
    while flag:
        if user_input == value_to_quit:
            raise SystemExit
        elif user_input not in valid_options:
            user_input = input(f'Please enter a valid option or \'{value_to_quit}\' to quit: ')
        else:
            return user_input

def main():
    """ Runs Main code """
    
    while True:
        questions_file = 'questions.json'
        topics_file = 'topics.json'
        past_scores_file = 'past_scores.json'

        questions, topics, past_scores = load_json_files(questions_file, topics_file, past_scores_file)

        compiled_data = create_compiled_data(questions, topics, past_scores)

        clear()

        print_welcome_page(compiled_data)

        topic_id = validated_input('\nEnter the number of the topic you want to review (\'q\' to quit): ', list(compiled_data.keys()))

        chosen_quiz = Quiz(topic_id, compiled_data, questions)

        # Execute the run_quiz method from the Quiz instance named chosen_quiz
        score, range_size = chosen_quiz.run_quiz()

        clear()

        final_score = int(100 * score / range_size)

        past_scores[topic_id] = str(final_score) + '%'

        with open('past_scores.json', 'w') as file_object:
            json.dump(past_scores, file_object)

        if final_score == 100:
            print(f'\nUnbelieveable! You Scored {final_score}%!\n')  
        elif final_score >= 90:
            print(f'\nExcellent Job! You Scored {final_score}%!\n')  
        if final_score >= 80:
            print(f'\nAwesome! You Scored {final_score}%!\n') 
        else:
            print(f'\nYou Scored {final_score}%!\n') 

        another_try = input('Enter \'y\' to run the app again, any other key to exit!')
        if another_try != 'y':
            break

if __name__ == '__main__':
    main() 