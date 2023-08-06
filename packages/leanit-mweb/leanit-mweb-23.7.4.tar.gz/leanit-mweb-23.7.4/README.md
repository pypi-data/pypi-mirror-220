Lean IT Mweb Framework

write a python function which gets a html input. The function should return a Form objects. The Form objects represents data parsed from the html <form> tag. The following code should work:

```python
html = "<html>...</html>"
# Form.parse is a classmethod, stores the html in the form object, parses the action, method and inputs in the __init__ method and manages a data dict with the input values
form = Form.parse(html) 
# if multiple forms are in the html, you can use
# parse_forms(html, index=0) to get the first form
# or parse_forms(html, id="form_id") to get the form with the given id
# or parse_forms(html, name="form_name") to get the form with the given name

form.fill(name="foo") # fill the form with data, updates form.data dict

# submit the form and get the response
# uses e.g. client.get("/workspace/create-first", allow_redirects=False)
# or client.post("/workspace/create-first", allow_redirects=False)
# based on the method and action of the form
response = form.submit(client)
```

Do not use beatifulsoup or other html parsers. Use regex to parse the html.

----

I have a python program which has an init() method. While executing the init method I fetch the current module name:

```python
class App:
    def init(self):
        module_name = self.__module__ # "mium_frontend"
```

there is a mium_frontend.models.user module which contains a "User" class which inherits from a "Model" class.

write code which automatically imports all classes from the "models" package. The import should take place in the init() method of the App class. Handle situations where there is no models package (there are apps without models). Handle situations with multiple levels of packages under the models package (e.g. models.foo.bar.User). Create a list of all classes which inherit from the Model class. The list should contain the classes, not the strings with the class names.

