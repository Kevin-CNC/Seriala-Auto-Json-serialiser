# Seriala-Auto-Json-serialiser
This is a custom tool I've built in order to allow for simple and intuitive JSON Serialization. This tool currently supports 4 Languages &amp; 3 Case-Types.

# What is this?
Seriala is a on-the-fly Web tool that allows for instant serialisation of JSON data into classes. This tool is especially usefull to pretty much create classes on the fly with just 1 API call! The main serialisation algorithm is inside the 'converter' module, while the 'main_backend' module simply allows for hosting & requests-processing.

The main purpose of this tool is to allow developers to quickly create classes for handling JSON data in a suitable way for OOP; Avoiding potential redundancy with the manual construction of classes for diverse JSON data trees. 

Currently 'Seriala' only supports 4 languages:
 * Python
 * JavaScript
 * Java
 * C#
   
<b>AND</b> 3 case-typing styles:
 * Snake Case (snake_case)
 * Pascal Case (PascalCase)
 * Camel Case (camelCase)


# How to use & Info:
## DEPENDENCIES:
* Flask
* converter.py (required by the backend)


## HOW TO USE:
* <b>On web / local server</b>:
    Simply paste in the raw Json data in the appropriate field, give a class name, select both the language & case typing you'd like to use and press the
    'Generate Class' button!

  The class will be directly given in the 'Generated Class' box below.

  <img width="887" alt="image" src="https://github.com/user-attachments/assets/ceca379f-0d46-4309-95e4-86f8fab4c628">

============================================================================================


* <b>Via POST request<b>:
  
    To do so, make a POST request to the following IP: '{your server's ip address}/generate_class'.
  
    Create a dictionary with the following keys:
    * <i>json_input</i> : Your actual JSON data.
    * <i>class_name</i> : The name of your class.
    * <i>case_style</i> : Enter 1 of the 3 valid inputs: 'snake_case', 'pascal_case', 'camel_case'. <b>(NON CASE SENSITIVE, _ NOT REQUIRED!)</b>
    * <i>language</i> : Enter the name of the wanted language: 'python', 'javascript', 'c#', 'java'  . <b>(NON CASE SENSITIVE)</b>
   <br>
  <i> Example: </i> <img width="626" alt="image" src="https://github.com/user-attachments/assets/97cd1bd6-d0f7-4123-8372-5dabb600b192">
   <br>
   <br>
    Perform a POST request to the address and gather the JSON output from said request; Your class' notation will be held in the <i>'class_output'</i> field.
   <br>
   <br>
    Execute the class notation in your desired environment; Feel free to add any needed methods to the classes if needed.
   <br>
   <br>
   <br>
    <i> The following is the output from the 'test.py' file:</i>


    <img width="533" alt="image" src="https://github.com/user-attachments/assets/08af3903-50d6-42bc-9730-d97f5dc42eef">


    
  
  




 
