# make a code that fiven a public github repo, it will download the repo and then parse the code and then find the most used words in the code and then print them out

import requests
import json
import os
import sys
import re
import operator
import collections
import string
import argparse


# get the repo name from the user
# repo = input("Enter the name of the repo: ")

# get the repo name from the user
# repo = sys.argv[1]

# make a function that will get the repo name and then download the repo
def download_repo_api(repo_name, repo_user):
    # make a request to the github api and get the repo
    response = requests.get("https://api.github.com/repos/" + repo_user + "/" + repo_name)

    # check if the repo exists
    if response.status_code == 200:
        # get the json data
        data = json.loads(response.text)

        # get the download url
        download_url = data["clone_url"]

        # download the repo into a temp folder
        path = os.path.join(os.getcwd(), "temp")

        # check if the temp folder exists
        if not os.path.exists(path):
            # create the temp folder
            os.mkdir(path)

        repo_path = os.path.join(path, data["name"])

        # check if the repo exists
        if not os.path.exists(repo_path):
            # go to the temp folder
            os.chdir(path)
            
            os.system("git clone " + download_url)

        # return the repo name
        return data["name"]
    else:
        # print the error
        print("The repo does not exist")

def download_repo(repo_name, repo_user):
    repo_url = "https://github.com/" + repo_user + "/" + repo_name
    # check if the repo exists
    response = requests.get(repo_url)

    # check if the repo exists
    if response.status_code == 200:
        # get the path to main.py file
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)

        # download the repo into a temp folder
        path = os.path.join(os.getcwd(), "temp")

        # go to the temp folder
        os.chdir(path)
            
        # check if the temp folder exists
        if not os.path.exists(path):
            # create the temp folder
            os.mkdir(path)

        repo_path = os.path.join(path, repo_name)

        # check if the repo exists
        if not os.path.exists(repo_path):
            os.system("git clone " + repo_url)

        # return the repo name
        return repo_name
    else:
        # print the error
        print("The repo does not exist")


# make a function that will get the repo name and then parse the code to see if the project uses typescript union types
def parse_code(repo, lines_of_code=0):
    print("Parsing the code for " + repo)

    print(os.getcwd())

    # go to the repo located in the temp folder
    path = os.path.join(os.getcwd(), repo)

    # go to the repo
    os.chdir(path)

    # get the list of files
    files = os.listdir()

    # remove the .git folder
    files.remove(".git")

    json_file_to_write_to = os.path.join(path, "union_types.json")

    print(json_file_to_write_to)

    # check if the json file exists
    if os.path.exists(json_file_to_write_to):
        # delete the file
        os.remove(json_file_to_write_to)

    initial_data = {
        "files" : []
    }

    # write the initial data to the json file
    with open(json_file_to_write_to, "w") as f:
        f.write(json.dumps(initial_data))

    # call the function that will parse the repo
    parse_repo_folder(files, path, json_file_to_write_to=json_file_to_write_to)

    # open the json file and calculate total lines of code that uses union types
    with open(json_file_to_write_to, "r") as f:
        # read the file
        data = f.read()

        # convert the data to a list
        data = json.loads(data)

        total_lines_of_code_with_unions = 0

        for line in data['files']:
            total_lines_of_code_with_unions += line["lines_of_code"]

    # from the total lines of code, calculate the percentage of lines of code that uses union types
    percentage_of_lines_of_code_that_use_union_types = (total_lines_of_code_with_unions / lines_of_code) * 100

    # print the percentage of lines of code that uses union types
    print("The percentage of lines of code that uses union types is " + str(percentage_of_lines_of_code_that_use_union_types) + "%")

    print("The total lines of code with unions is " + str(total_lines_of_code_with_unions))
    print("The total lines of code is " + str(lines_of_code))

    # append the percentage of lines of code that uses union types to  the json file
    with open(json_file_to_write_to, "a") as f:
        f.write(" " + str(percentage_of_lines_of_code_that_use_union_types))

    return percentage_of_lines_of_code_that_use_union_types

def parse_repo_folder(files, path="", json_file_to_write_to=""):
    # make recursive function that will go through the files and folders
    for file in files:
        # check if the file is a folder
        if os.path.isdir(file):
            # go to the folder
            os.chdir(file)

            # get the files in the folder
            files = os.listdir()

            # call the function again
            parse_repo_folder(files, path=os.path.join(path, file), json_file_to_write_to=json_file_to_write_to)

            # go back to the parent folder
            os.chdir(path)
        else:
            # check if the file is a python file
            if file.endswith(".ts"):
                # parse the file and detect if it uses union types
                parse_file_and_detect_if_uses_union(file, json_file_to_write_to=json_file_to_write_to, path_to_file=path)

def parse_file_and_detect_if_uses_union(file, json_file_to_write_to="", path_to_file="", total_lines_of_code=0):
    # open the file
    with open(file, "rb") as f:
        # read the file with utf-8 encoding
        data = f.read().decode('ISO-8859-1')

        # check if the file uses union types
        if " | " in data:
            # print the file name
            print(file)

            # append the file name to the json file to write to
            if json_file_to_write_to != "":
                
                file_json = {
                    "file_path": os.path.join(path_to_file, file),
                    "lines_of_code": len(data.split("\n"))
                }

                # if 

                # open the json file
                with open(json_file_to_write_to, "r+") as f:
                    # check if file is empty
                    # if len(f.read()) == 0:
                    #     data = {
                    #         "files": [file_json]
                    #     }

                    #     f.write(json.dumps(data))
                    #     return

                    data = json.loads(f.read())

                    if 'files' not in data:
                        data['files'] = [file_json]
                    else:
                        data['files'].append(file_json)

                    f.seek(0)
                    f.write(json.dumps(data))


    return total_lines_of_code


def list_repos(number_of_repos=10, page=1):
    print("Getting list of repos that use typescript from github ...")
    print("Number of repos: " + str(number_of_repos))
    print("Page: " + str(page))

    # get list of repos public repos on github that use typescript
    response = requests.get("https://api.github.com/search/repositories?q=language:typescript&sort=stars&order=desc&per_page=" + str(number_of_repos)+"&page=" + str(page))

    # check if the request was successful
    if response.status_code == 200:
        # get the json data
        data = json.loads(response.text)

        # get the list of repos
        repos = data["items"]

        counter = 0

        # loop through the repos
        for repo in repos:
            if repo["fork"] == True or repo["private"] == True or repo["size"] > 100000:
                continue

            # get the repo name
            repo_name = repo["name"]

            languages_url = repo["languages_url"]

            # get the languages used in the repo
            languages_used_response = requests.get(languages_url)

            # check if the request was successful 
            if languages_used_response.status_code == 200:
                # get the json data
                languages_used_data = json.loads(languages_used_response.text)

                # check if typescript is used
                if "TypeScript" not in languages_used_data:
                    continue

                # get the number of lines of code 
                lines_of_code = languages_used_data["TypeScript"]

                # check if the number of lines of code is greater than 1000
                if lines_of_code < 1000:
                    continue

                # get the repo user
                repo_user = repo["owner"]["login"]

                # download the repo
                repo_name = download_repo(repo_name, repo_user)

                # parse the code
                percentage_of_lines_of_code_that_use_union_types = parse_code(repo_name, lines_of_code)

                # check if the percentage of lines of code that uses union types is greater than 10
                if percentage_of_lines_of_code_that_use_union_types > 10:
                    print(repo_name)
                    print("The percentage of lines of code that uses union types is " + str(percentage_of_lines_of_code_that_use_union_types) + "%")
                    print("The total lines of code is " + str(lines_of_code))

                counter += 1

                if counter >= number_of_repos:
                    break

    else:
        print("Error: " + str(response.status_code))
        print(response.text)

    if page < 10:
        page += 1
        list_repos(number_of_repos=number_of_repos, page=page)


            
            

if __name__ == "__main__":
    # # get the repo name from the user
    # repo_name = "Emojiopoly"
    # repo_user = "Chuzzy"

    # # download the repo
    # repo_name = download_repo(repo_name, repo_user)

    # # parse the code
    # parse_code(repo_name)

    # list the repos
    list_repos()