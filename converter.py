import json
import decimal

def typeIfy(string:str,type:str):
    new_name = str()
    can_skip = False
    canCamel = False
    canPascal = False

    for i in range(len(string)):
        character = string[i]
        
        if can_skip:
            can_skip = False
            continue
    
        
        if character == " ": # Anything below only fires if the character is a space
            if type == "camel case" or type == "camel_case":
                if not(canCamel):
                    canCamel = True
                    continue # avoids inserting the space
            elif type == "pascal case" or type == "pascal_case":
                canPascal = True
                continue # Skips current space
            else:
                character = "_" # defaults to snake casing
                
        else:
            if type == "pascal case" or type == "pascal_case":
                if i == 0 or canPascal:
                    canPascal = False
                    character = character.upper()
                
            else:
                if canCamel:
                    canCamel = False
                    character = character.upper()   
            
        new_name += character
    return(new_name)
    

def _Translate_(JSON:str,GivenClassName:str,Language:str,CaseType:str):
    JSON = json.dumps(JSON)
    unjsonified = json.loads(JSON)

    ClassName = typeIfy(GivenClassName,CaseType)

    class_notations={
        "starts":{
            "python":f"class {ClassName}():\n",
            "java":f"public Class {ClassName}"+"{\n",
            "c#":f"public Class {ClassName}"+"{\n",
            "javascript":f"Class {ClassName} "+"{\n     constructor(){\n"
        },
        "ends":{
            "python":"",
            "java":"}",
            "javascript":"     }\n}",
            "c#":"}"
        }
    }

    key_map = []
    for key in unjsonified:
        value = unjsonified[key]
        # structured as: [ Name[0], Value[1], Datatype[2] ]
        key_name = typeIfy(key,CaseType.lower())
        key_map.append([key_name,value,type(value)])
        

    Class_Text = class_notations["starts"][Language.lower()]

    if Language.lower() == "python":
        Class_Text += "   def __init__(self):\n"
        for node in key_map:
            Class_Text += f"        self.{node[0]} = {node[2].__name__}()\n"
           
    elif Language.lower() == "javascript":
        for node in key_map:
            Class_Text += f"        this.{node[0]};\n"

            
    # Java & C# class building section:
    elif Language.lower() == "java" or Language.lower() == "c#":
        
        # both used for C# exclusively
        constructor = f"    public {ClassName}(" 
        constructor_items = str()
        
        registered_types = {
            "String":[],
            "char":[],
            "int":[],
            "long":[],
            "float":[],
            "double":[],
            "boolean":[],
            "List":[], # Different format: [[List_Name, List_Type]]
            "dictionary":[],
        }
        
        # Loops through the key_map list, which has everything from the json string
        for node in key_map:
            value_type = node[2]
            value = node[1]
            node_name = node[0]
            
            if value_type is bool:
                registered_types["boolean"].append(node_name)
                
            elif value_type is str:
                if len(value) == 1:
                    registered_types["char"].append(node_name)
                else:
                    registered_types["String"].append(node_name)
                    
            elif value_type is int:
                if -2147483648 <= value <= 2147483647:
                    registered_types["int"].append(node_name)
                else:
                    registered_types["long"].append(node_name)
            
            elif value_type is float:
                if (decimal.Decimal(value).as_tuple().exponent*(-1)) <= 8:
                    registered_types["float"].append(node_name)
                else:
                    registered_types["double"].append(node_name)
                  
            elif value_type is dict:
                items_in_list = 0
                
                for item in value: # iterating through the actual list
                    items_in_list += 1
                    
                registered_types["dictionary"].append([node_name,items_in_list])
                    
            elif value_type is list:
                name = node
                
                same_type = True
                previous_type = None
                requires_longs = False
                requires_doubles = False
                items_in_list = 0
                
                for item in value: # iterating through the actual list
                    items_in_list += 1
                    
                    if previous_type is None:
                        previous_type = type(item)
                    else:
                        if not(previous_type is type(item)):
                            same_type = False
                            break
                        
                        if (type(item) is int) and (-2147483648 > item or item > 2147483647):
                            requires_longs = True
                        elif (type(item) is float) and ((decimal.Decimal(item).as_tuple().exponent*(-1)) > 8):
                            requires_doubles = True
                            
                        
                if same_type: # must be a list
                    c_chosen_type = previous_type.__name__
                    
                    if c_chosen_type == "str":
                        c_chosen_type = "String"
                            
                    elif c_chosen_type == "int":
                        if requires_longs:
                            c_chosen_type = "long"
                            
                    elif c_chosen_type == "float":
                        if requires_doubles:
                            c_chosen_type = "double"
                        
                    
                    registered_types["List"].append([node_name,c_chosen_type])
                else: # must be a dictionary
                    registered_types["dictionary"].append([node_name,items_in_list])
                
                
        for Type_Name in registered_types:
            if len(registered_types[Type_Name]) == 0: # avoid non-existant types (empty lists)
                continue
            
            Current_Text = str()
            if Language.lower() == "java":
                Current_Text = f"    {Type_Name} "
            elif Language.lower() == "c#":
                if Type_Name == "String":
                    Current_Text = f"    public string "
                else:
                    Current_Text = f"    public {Type_Name} "
            
            Counter = 0
            Skip = False # Flag to skip automatic insertion of text in Class_Text after the loop, triggered True only whenever it's a dictionary or list, to avoid duplication.
            
            for Item in registered_types[Type_Name]:
                if Type_Name == "dictionary":
                    Array_Name = Item[0]
                    Array_Size = Item[1]
                    
                    if Language.lower() == "c#":
                        Current_Text = f"    public Dictionary<string, dynamic> {Array_Name} = new Dictionary<string, dynamic>()\n"
                        constructor += f"Dictionary {Array_Name},"
                        constructor_items += f"\n         this.{Array_Name} = {Array_Name}"
                        Class_Text += Current_Text
                        Skip = True
                        
                    elif Language.lower() == "java":
                        Current_Text = f"    Object[] {Array_Name} = new Object[{Array_Size}];\n"
                        Class_Text += Current_Text
                        Skip = True
                    
                elif Type_Name == "List":
                    List_Type = Item[1]
                    List_Name = Item[0]
                    Current_Text += f"<{List_Type}> {List_Name} = new ArrayList<>;\n"
                    Class_Text += Current_Text
                    Skip = True
                    
                    if Language.lower() == "c#":
                        constructor += f"{Type_Name} {List_Name},"
                        constructor_items += f"\n         this.{List_Name} = {List_Name}"
                    
                else:
                    if Language.lower()=="java":
                        print("Item found.")
                        if Counter > 0:
                            Current_Text += f", {Item}"
                        else:
                            Current_Text += Item
                        
                        Counter += 1
                        
                    elif Language.lower()=="c#":
                        Current_Text += Item+"\n"
                        Class_Text += Current_Text
                        
                        # actual class
                        if Type_Name == "String":
                            Current_Text = f"    public string "
                        else:
                            Current_Text = f"    public {Type_Name} "
                        
                        # constructor
                        if Type_Name == "String": # Adapt to C#
                            constructor += f"string {Item},"
                        else:
                            constructor += f"{Type_Name} {Item},"
                            
                        constructor_items += f"\n         this.{Item} = {Item}"     
            
            if not(Skip) and Language.lower() == "java":
                Current_Text += ";\n"
                Class_Text += Current_Text
                    
    
    
    if Language.lower() == "c#":
        constructor = constructor[:-1]
        Class_Text += f"\n{constructor})"+"{"+f"{constructor_items}\n"+"    }\n"
        
        
    Class_Text += class_notations["ends"][Language.lower()]
    print(Class_Text)
    return(Class_Text)
    