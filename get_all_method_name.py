import inspect
import tensorflow as library_name

# Get all method names in the library and its modules
method_paths = []

# Inspect the library root
for method_name in dir(library_name):
    method = getattr(library_name, method_name)
    if inspect.ismethod(method) or inspect.isfunction(method):
        method_path = f"{library_name.__name__}.{method_name}"
        method_paths.append(method_path)

# Inspect modules within the library
for module_name in dir(library_name):
    module = getattr(library_name, module_name)
    if inspect.ismodule(module):
        for method_name in dir(module):
            method = getattr(module, method_name)
            if inspect.ismethod(method) or inspect.isfunction(method):
                method_path = f"{module.__name__}.{method_name}"
                method_paths.append(method_path)

# Print the method paths
method_paths = list(set(method_paths))
method_paths = [x.split(".")[-1] for x in method_paths ]
print(len(method_paths))
method_paths = ["."+x+"(" for x in method_paths ]
print(method_paths)

with open('C:\@code\APIMISUSE\data\API_method_list_tf.txt', 'w') as f:
    for item in method_paths:
        f.write("%s\n" % item)