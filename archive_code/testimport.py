import ast
import inspect
import torch


class MethodCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.methods = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            method_name = node.func.attr
            class_name = None

            # check if the method is called on an instance of a class
            if isinstance(node.func.value, ast.Name):
                var_name = node.func.value.id
                var = self.lookup_variable(node, var_name)
                if isinstance(var, ast.ClassDef):
                    class_name = var.name

            # check if the method is called inside a method or function
            func = self.get_enclosing_function(node)
            if func is not None:
                if isinstance(func.args.args[0], ast.Name):
                    arg_name = func.args.args[0].id
                    arg = self.lookup_variable(func, arg_name)
                    if isinstance(arg, ast.ClassDef):
                        class_name = arg.name

            # add the class name to the method name if available
            if class_name is not None:
                method_name = f"{class_name}.{method_name}"

            self.methods.append(method_name)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        class_name = None

        # check if the function is defined inside a class
        if isinstance(node.parent, ast.ClassDef):
            class_name = node.parent.name

        # add the class name to the function name if available
        if class_name is not None:
            method_name = f"{class_name}.{node.name}"
        else:
            method_name = node.name

        self.methods.append(method_name)

        self.generic_visit(node)

    def lookup_variable(self, node, name):
        # Traverse the AST to find the variable definition corresponding to the given name
        scope = node
        while scope is not None:
            for stmt in scope.body:
                if isinstance(stmt, ast.Assign):
                    if len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name) and stmt.targets[0].id == name:
                        return stmt.value
                elif isinstance(stmt, ast.ClassDef):
                    if stmt.name == name:
                        return stmt
            scope = scope.parent

        # If we didn't find a definition in this node or its parents, return None
        return None

    def get_enclosing_function(self, node):
        # Traverse the AST to find the function or method that encloses the given node
        scope = node
        while scope is not None:
            if isinstance(scope, ast.FunctionDef):
                return scope
            elif isinstance(scope, ast.Module):
                return None
            scope = scope.parent

        # If we didn't find a function or method in this node or its parents, return None
        return None


# create an AST object from the imported module
torch_source = inspect.getsource(torch)
module_ast = ast.parse(torch_source)

# traverse the AST to extract method and class names
visitor = MethodCallVisitor()
visitor.visit(module_ast)

# print the method and class names
print(visitor.methods)
