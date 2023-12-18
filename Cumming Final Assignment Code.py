from tabulate import tabulate #imports tabulate library to allow for creation of tables

def read_tree_names(tree_file_path): #reads trees.txt file and adds the tree names to the empty list trees
    trees = []
    with open(tree_file_path, 'r') as file:
        for line in file:
            trees.append(line.strip())
    return trees

def tokenize_name(tree): #simplifies the large tree file and breaks down each name
    words = [word.strip("'") for word in tree.split() if word.isalpha()] #word.isalpha() ensures that hyphens and apostrophes arent added to the potential abbreviations
    words_uppercase = [word.upper() for word in words]
    return words_uppercase

def read_values_file(values_file_path): #reads the values.txt file from the created variable values_file_path
    values_dict = {} #stores them in this created empty list
    with open(values_file_path, 'r') as file:
        for line in file:
            letter, value = line.split() #splits the letter and its corresponding value into a list to match the 2 variables together
            values_dict[letter] = int(value) #changes the value to an integer
    return values_dict

def calculate_letter_score(letter, values_dict, tree):
    words = tokenize_name(tree)

    rarity_value = 0 #assigning the initial rarity_value

    for word in words:
        position = word.find(letter) + 1

        if position == 1:
            rarity_value = values_dict.get(letter, 0)
        elif position == len(word):
            if letter == 'E': #assigning the required rules, so if the last letter of a word is E it has a value of 20
                rarity_value = 20
            else: #otherwise the last letter has a value of 5
                rarity_value = 5

        if 1 < position < len(word):
            rarity_value = values_dict.get(letter, 0)

    return rarity_value

def generate_abbreviations_with_values(trees, values_dict):
    tree_and_abbreviations_with_values = []

    trees.sort() #sorts the trees in alphabetical order

    for tree in trees:
        words = tokenize_name(tree)

        if words:
            first_letter = tree[0] #ensures the first letter is assigned a score of 0

            for word in words:
                if len(word) >= 3:
                    for i in range(len(word) - 2):
                        for j in range(i + 1, len(word) - 1): #for loops generating indices and generates starting and ending positions for potential substrings
                            if word[i] != first_letter: #!= is the not equal operator in python, means the first letter in each abbreviation isn't duplicated
                                abbreviation = (first_letter + word[i] + word[j]) #word[i] can be thought of as the second letter, word[j] as the third letter

                                position = word.find(word[i]) + 1
                                position_value_1 = 1 if position == 2 else (2 if position == 3 else 3)

                                position = word.find(word[j]) + 1
                                position_value_2 = 1 if position == 2 else (2 if position == 3 else 3)

                                position_value = position_value_1 + position_value_2

                                second_let_score = calculate_letter_score(word[i], values_dict, tree) #calculates the score for the second letter using the position, letter value and tree name
                                third_let_score = calculate_letter_score(word[j], values_dict, tree) #calculates the score for the third letter using the position, letter value and tree name

                                abbreviation_score = second_let_score + third_let_score + position_value

                                tree_and_abbreviations_with_values.append((abbreviation, abbreviation_score, tree)) #joins these 3 variables together

    return tree_and_abbreviations_with_values

trees_file_path = ('/Users/CCumm/OneDrive/Documents/AC50002/Python Assignment/trees.txt') #file path for trees.txt file
values_file_path = ('/Users/CCumm/OneDrive/Documents/AC50002/Python Assignment/values.txt') #file path for values.txt file

trees = read_tree_names(trees_file_path)
values_dict = read_values_file(values_file_path)

all_abbreviations = []

for tree in trees:
    abbreviations_for_tree = generate_abbreviations_with_values([tree], values_dict)
    all_abbreviations.extend(abbreviations_for_tree)

table_data = [] #creates sorted data ready to be displayed as a table by extracting each piece of required info from each entry
for entry in sorted(all_abbreviations, key=lambda x: x[1]): #lambda is crucial for sorting elements
    abbr, score, current_name = entry
    table_data.append([current_name, abbr.upper(), score])

table_data_sorted = sorted(table_data, key=lambda x: x[0])

table_headings = ["Name", "Abbreviation", "Score"] #defines the table headings
print(tabulate(table_data_sorted, headers=table_headings, tablefmt="rounded_grid")) #prints the table with the headings, formatted with the rounded_grid option

def main(): #defining the main function
    try:
        input_filename = input("Enter the input file name: ") #insert file path here for trees.txt
        output_filename = "Cumming_trees_abbrev.txt" #generates an output file with this name

        trees = read_tree_names(input_filename)
        values_dict = read_values_file('/Users/CCumm/OneDrive/Documents/AC50002/Python Assignment/values.txt')

        with open(output_filename, 'w') as output_file:
            for entry in all_abbreviations:
                abbreviation, score, current_name = entry
                output_file.write(f"{current_name} {abbreviation} {score}\n")

        print(f"Results written to {output_filename}") #displays if the output is successfully created

    except FileNotFoundError: #displays if the input file was incorrect
        print(f"Error: File '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()