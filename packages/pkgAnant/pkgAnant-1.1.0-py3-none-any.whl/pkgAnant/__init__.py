import random
import string
import csv

def exclude_csv(path):
    with open(path, newline='') as csvfile:
        reader=csv.reader(csvfile)
        return set(row[0] for row in reader)

def generate_pass(exclusions):

    # using random for range
    len=random.randint(6, 12)

    # using string to generate characters
    lower=string.ascii_lowercase
    upper=string.ascii_uppercase
    num=string.digits

    # to select at least one lower, one upper, one number
    password=random.choice(lower)+random.choice(upper)+random.choice(num)

    # filling password with remaining length
    password+=''.join(random.choices(lower+upper+num,k=len-3))

    # Remove excluded characters from the password
    password=''.join(char for char in password if char not in exclusions)

    # shuffling the password by creating a list
    password_list=list(password)
    random.shuffle(password_list)
    password=''.join(password_list)
    return password

#calling exclude_csv function to collect all names from names.csv
excluded_names=exclude_csv("names.csv")

#calling exclude_csv function to collect all names from places.csv
excluded_places=exclude_csv("places.csv")

#gathering all names and places which shouldn't be included in password
all_exclusions=excluded_names.union(excluded_places)

#generating password by calling function
password=generate_pass(all_exclusions)
print("updated : "+password)
