import random

# A function that shuffles all the charracters of a string
def shuffle(string):
  tempList = list(string)
  random.shuffle(tempList)
  return ''.join(tempList)

# Main Program starts here
def generate_password():
  favorite_words = ["Godzilla","King Kong", "PTA", "White Noise", "Remain in Light", "Tony Sopranos", "New York", "Jack Nicholson"]  
  selected_word = random.choice(favorite_words)  
  upper_case_letter_1 = chr(random.randint(65,90))  
  upper_case_letter_2 = chr(random.randint(65,90))  
  lower_case_letter_1 = chr(random.randint(97,122))  
  lower_case_letter_2 = chr(random.randint(97,122))  
  numbers_1 = chr(random.randint(48,57))  
  numbers_2 = chr(random.randint(48,57))  
  special_characters_1 = chr(random.choice([33, 34, 35, 36, 37, 38, 63, 64]))
  special_characters_2 = chr(random.choice([33, 34, 35, 36, 37, 38, 63, 64]))

# Generation of Password
  password = (selected_word + upper_case_letter_1 + upper_case_letter_2 + 
            lower_case_letter_1 + lower_case_letter_2 + 
            numbers_1 + numbers_2 + 
            special_characters_1 + special_characters_2)

  password = shuffle(password)
  print(password)
  
# Output
generate_password()
generate_password()
generate_password()