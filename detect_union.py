# make a code that parses the input file and detects if it uses typescript union type
# and if it does, it should print the line number and the line itself
# for example, if the input file is
# 1: type A = string | number;
# 2: type B = string | number | boolean;
# 3: type C = string;
# 4: type D = string | number | boolean | null;
# 5: type E = string | number | boolean | null | undefined;
# 6: type F = string | number | boolean | null | undefined | symbol;


# then the output should be
# 1: type A = string | number;
# 2: type B = string | number | boolean;

import re

def has_union(data):
    # search for the pattern of union type
    # if it finds the pattern, return True
    # otherwise, return False
    pattern = re.compile(r'\|')
    if pattern.search(data):
        return True
    else:
        return False
    
def file_has_union(file_data):
    for i, line in enumerate(file_data):
        if has_union(line):
            print(i+1, line, end='')
            return True
    return False
    
# def main():
#     # open the input file
#     # read the file line by line
#     # if the line has union type, print the line number and the line itself
#     # close the file
#     with open('temp/vue/types/jsx.d.ts', 'r') as f:
#         for i, line in enumerate(f):
#             if has_union(line):
#                 print(i+1, line, end='')

# if __name__ == '__main__':
#     main()