from pygradecode.ast_to_xml import xml
from pygradecode.xml_utils import prettify, get_node_source
from pygradecode.find_functions import find_functions, uses_function
from pygradecode.find_arguments import find_arguments, arg, Arg

code = "sum([1, 2, 3])\nprint('Hello', 'World!', sep=', ')\nsum([4, round(5), 6])"

# find all functions
find_functions(code)
find_functions(code, 'sum')
find_functions(code, 'len')
uses_function(code, 'len') 

# code = "sum([1, 2, 3])\nprint('Hello', 'World!', sep=', ')\nsum([4, 5, 6])"

# # getting all arguments
code = "sum([4, round(5), 6])"

code = r'print(1, 2, sep=", ", end=foo(x = ["\n"]))'
code = 'print(1, 2, sep=", ", end=foo(x = ["\n"]))'

find_arguments(code)

arg(x = ["\n"])

xml_tree = xml(code)
prettify(xml_tree)


kwarg_values = [v for v in xml_tree.xpath("//keyword/value/*")]
kwargs_pairs = [get_node_source(code, kw).decode('unicode_escape') for kw in kwarg_values]
split_value_strings = [p.split("=") for p in kwargs_pairs]
args = [
  Arg(name=s[0].strip(), value='='.join(s[1:]).strip()) 
  for s in split_value_strings
]
args

args = xml_tree.xpath("//args/*")
kwargs = xml_tree.xpath("//keyword")
kwarg_values = [kw.xpath("./*") for kw in kwargs]
kwargs_pairs = [
  get_node_source(code, kw[1]).encode('unicode_escape').decode('unicode_escape') 
  for kw in kwarg_values
]
split_args = [p.split("=") for p in kwargs_pairs]
all_kwargs = [Arg(name=s[0], value=".".join(s[1:])) for s in split_args]
all_kwargs

print(f"args: {args}")
print(f"kwargs: {kwargs}")
print(f"expanded_kwargs: {'|'.join(expanded_kwargs)}")


find_functions(code)
find_arguments(code)
# x.elements

# # getting arguments from one
# find_arguments(code, 'sum')
# find_arguments(code, 'print')


code = "-1 - 2 * 3 // 4"
xml_tree = xml(code)
prettify(xml_tree)

xml_tree.xpath("//op/*")[0].tag


BOOL_OPS = {}

OPERATORS = {
  # boolops
  'and': 'And', 'or': 'Or',
  # operators
  '+': 'Add',
  '-': 'Sub',
  '*': 'Mult',
  '@': 'MatMult',
  '/': 'Div',
  '%': 'Mod',
  '**': 'Pow',
  '<<': 'LShift',
  '>>': 'RShift',
  '|': 'BitOr',
  '^': 'BitXor',
  '&': 'BitAnd',
  '//': 'FloorDiv',
  # unaryops
  '~': 'Invert', 'not': 'Not', '+': 'UAdd', '-': 'USub',
  # cmpops
  '==': 'Eq', '!=': 'NotEq', '<': 'Lt', '<=': 'LtE', '>': 'Gt', '>=': 'GtE',
  'is': 'Is', 'is not': 'IsNot', 'in': 'In', 'not in': 'NotIn'
}




# code
# xml_tree = xml(code)
# prettify(xml_tree)


# xml_tree.xpath("//args/*,//keywords/*")

# #  + x_tree.xpath(".//keywords/*")



# # interesting side thing: args + keywords are their own 
# xml_tree = xml(code)
# prettify(xml_tree)

