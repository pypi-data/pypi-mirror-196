import openai
import random

def complete_code(code, api_key):
    OPEN_API_KEY = api_key
    openai.api_key = OPEN_API_KEY
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=code,
    temperature=0.7,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].text

def apply_mutations(list_of_satisfied_checks, codesnippet, api_key):
    invalid_messages = ["EOF", "§", "COM", "§ END OF DOC", "</code>", "\n",] 
    for index, satisfied_check in enumerate(list_of_satisfied_checks):
        code = codesnippet + """\n""" + """# """ + list_of_satisfied_checks[index]
        codesnippet = complete_code(code, api_key)
        # validate if str has any invalid characters
        for string_values in invalid_messages:
            if string_values in codesnippet:
                codesnippet.replace(string_values, "") 

    str = codesnippet.replace('/(?:\r\n|\r|\n)/g', '<br/>') 
    
    return str

def check_for_checks_and_mutations(codesnippet, api_key):
    list_of_satisfied_checks = []
    count = 0
    word = "Yes"
    check_list = ["# Does the code contain any string literals?", "# Does the code contain any integer literals?", "# Does the code contain any conditional statement?", "# Does the code contain more than one conditional statement?", "# Does the code contain single level loop?", "# Does the code contain nested loop?", "# Does the code have a nested list of integers?", "# Does the code have a nested list of string?", "# Does the code have any infinite loop?", "# Does the code access an element of the list?", "# Does the code have elif statement?", "# Does the code have else statement?", "Does the code contain any range statement?", "Check if the code has any comparison operators?", "Does the code have length function?", "Does the code contain any arithmetic expression?", "Does the code have any boolean operator?", "Does the code contain a tuple of string literals?", "Does the code contain a tuple of integer literals?", "Does the code contain any arithmetic operator?"]
    mutation_list = ["Only change the value of string literals to other string literals with same length of the string and regenerate code.", "Only add 1 to all integer literals and regenerate code.", "Keep the integer literals same but only change the 'if condition' in the code.", "Keep the integer literals exactly the same but only swap the 'if conditions' in the code.", "Only change the values in the loop and regenerate code.", "Only swap the loops and regenerate code.", "Only add 1 to integer literals or add more numbers or change inner list.", "Only change string literals or add more string literals or change inner list.", "Only add value to the infinite loop and regenerate code.", "Keep the entire list values the same and only add one to the index value of the list being accessed.", "Only change the elif to else statement and regenerate code.", "Only change the else to elif statement and regenerate code.", "Only add second and third parameter to the range statement.", "Keep the integer literals in the code the same but only change the comparison operator.", "Keep the code the same but add or subtract 1 from the length function and regenerate the code.", "Only change the arithmetic expression and regenerate the code.", "Only change the boolean operator and regenerate the code.", "Modify the string literals or add or delete some string literals and generate code.", "Modify the integer literals or add or delete some integer literals and generate code.", "Only change the arithmetic operator in the code and regnerate the code."]

    for index, one_check in enumerate(check_list):
        code = codesnippet + """\n""" + """# """ + check_list[index]

        code_result = complete_code(code, api_key)
        if word in code_result:
            list_of_satisfied_checks.insert(count,mutation_list[index])
            count+=1
    
    return list_of_satisfied_checks

def generate_first_similar_code(my_code, api_key):

    # check for all mutations and checks
    list_of_satisfied_checks = check_for_checks_and_mutations(my_code, api_key)

    # choose random mutations to apply from a list
    lenght_of_list = len(list_of_satisfied_checks)
    random_int = random.randint(1, lenght_of_list)
    list_of_satisfied_checks = random.sample(list_of_satisfied_checks, random_int)

    # Apply mutations
    str = apply_mutations(list_of_satisfied_checks, my_code, api_key)
    
    return str, list_of_satisfied_checks


def mutate(my_code, number_of_mutations, api_key):

    code_versions = []
     
    similar_code, list_of_satisfied_checks = generate_first_similar_code(my_code, api_key)
    code_versions.append(similar_code)

    while number_of_mutations > 0:
        similar_code = apply_mutations(list_of_satisfied_checks, similar_code, api_key)
        code_versions.append(similar_code)
        number_of_mutations -=1

    return code_versions