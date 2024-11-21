# this is just a test file to test for requests.
# please read dependencies and comments in order for this to function, even tho it shouldn't take too much
 
import requests
import json

api_ip = 'http://127.0.0.1:5000/generate_class' #if hosting locally, just replace the ip with your own server's

student_data = {
    "students" : {
      "maria" : {
            "full name" : "Maria White",
            "class" : "1A",
            "class id" : 11,
        },
        "marco" : {
            "full name" : "Marco White",
            "class" : "2A",
            "class id" : 21,
        },
        "jacob" : {
            "full name" : "Jacob Smith",
            "class" : "1B",
            "class id" : 12,
            "failing" : True
        },  
    },
    "school mark average" : 75,
    "average attendance" : 85.757462816127,
    "student faculty members" : ['Alfred Castani', 'Bianca Ibraimovich'],
}


# ACTUAL DATA REQUEST HERE!
data = {'json_input':student_data, 'class_name':'My beautiful class' ,'case_style':'snake case', 'language':"python"}
response = requests.post(api_ip,json=data)

try:
    exec(response.json()['class_output'])
    print("Class notation actually executed successfully!")
    
    new_item = My_beautiful_class()
    print(new_item)
    
except Exception as errorlog:
    print(f"Error during class construction:\n{errorlog}")
    