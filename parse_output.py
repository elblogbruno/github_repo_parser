import json


def parse_output():
    # open 'global_analysis.json'
    # parse json

    max_percentage = 0

    with  open('global_analysis.json', 'r') as f:
        data = json.load(f)

        # order the repos by the percentage of lines of code that use union types
        # print the repo name and the percentage of lines of code that use union types
    
        for repo in data['repos']:
            percentage_of_lines_of_code_that_use_union_types = repo['percentage_of_lines_of_code_that_use_union_types']

            if percentage_of_lines_of_code_that_use_union_types > max_percentage:
                max_percentage = percentage_of_lines_of_code_that_use_union_types
                max_repo = repo['repo_name']

        print('Repo with the highest percentage of lines of code that use union types: ', max_repo, max_percentage)

def get_top_5():
    # open 'global_analysis.json'
    # parse json
    print('Top 5 repos that use union types the most:')
    # order the repos by the percentage of lines of code that use union types
    # print the top 5 repos and the percentage of lines of code that use union types

    with  open('global_analysis.json', 'r') as f:
        data = json.load(f)

        data['repos'].sort(key=lambda x: x['percentage_of_lines_of_code_that_use_union_types'], reverse=True)

        for i in range(5):
            print(data['repos'][i]['repo_name'], data['repos'][i]['percentage_of_lines_of_code_that_use_union_types'])

        data['repos'].sort(key=lambda x: x['percentage_of_lines_of_code_that_use_union_types'], reverse=False)

        print('Top 5 repos that use union types the least:')
        for i in range(5):
            print(data['repos'][i]['repo_name'], data['repos'][i]['percentage_of_lines_of_code_that_use_union_types'])

if __name__ == '__main__':
    parse_output()
    get_top_5()