# Snakify auto write system
# made by Nelson with <3

# website: https://nelsongx.com
# source: https://github.com/nelsonGX

import requests
import re
import json

session = requests.Session()

# Login

print("="*20)
print("  _    _        _____             _    _  __       ")
print(" | |  | |      / ____|           | |  (_)/ _|      ")
print(" | |  | |_ __ | (___  _ __   __ _| | ___| |_ _   _ ")
print(" | |  | | '_ \\ \\___ \\| '_ \\ / _` | |/ / |  _| | | |")
print(" | |__| | | | |____) | | | | (_| |   <| | | | |_| |")
print("  \\____/|_| |_|_____/|_| |_|\\__,_|_|\\_\\_|_|  \\__, |")
print("                                              __/ |")
print("                by nelson                    |___/ ")
print("="*20)
print()

account = input("> Paste your Snakify E-Mail / account name: ")
password = input("> Paste your password: ")


data = {
  "email": str(account),
  "password": str(password)
}
#header = { "accept" : "application/json" }
r = session.post(url = "https://snakify.org/api/v2/auth/login/", json=data)
check = r.text
check = json.loads(str(check))
if check["userSigned"] != True or check["emailRegistered"] != True:
    print("Login incorrect. exiting...")
    exit()
else:
    print("Login successful.")

#DEBUG url = "https://snakify.org/en/lessons/dictionaries_dicts/problems/frequency_analysis/"

print("Loading snakify URLs...")
with open('snakify.txt') as f:
    links = f.readlines()
print(str(len(links)-1) + " lines loaded.")
#url = input("Paste snakify URL: ")


tries = 1
fail = 0
for url in links:
    if url == "EOF":
        break

    problem = url
    problem = problem[:-2]

    while "/" in problem:
        problem = problem[1:]
    
    print("[" + str(tries) + "/" + str(len(links)-1) + "] Trying problem `" + str(problem) + "`, status: ", end="")

    response = session.get(url).text

    for line in response.splitlines():
        if re.match("        window.tests", line):
            data = line

    # I have no idea why I do this, but I have no other options
    data = re.sub("        window.tests = \[", "", data)
    data = re.sub("];", "", data)
    data = re.sub("{'", '{"', data)
    data = re.sub("'}", '"}', data)
    data = re.sub("': '", '": "', data)
    data = re.sub("':", '":', data)
    data = re.sub(", '", ', "', data)
    data = re.sub("': ", '": ', data)
    data = re.sub("', ", '", ', data)
    data = re.sub("', '", '", "', data)
    data = re.sub("{", '"zTEST0":{', data, 1)
    tests = data.count("{")
    for i in range(1, data.count("{")):
        data = re.sub(", {", ', "zTEST' + str(i) + '":{', data, 1)
    data = "{" + data + "}"

    #DEBUG print(data)
    # Sometimes it just breaks
    try:
        if problem == "number_of_occurrences_before":
            data = '{"zTEST0":{"answer": "0 0 1 0 0"}, "zTEST1":{"answer": "0 0 0 0 0 0 1 0 0 1 0 0 1 0 2 2 0 0 0 0 1 2 3 3 1 1 4 0 1 0 1 2 4 1 5 0 0"}, "zTEST2":{"answer": "0 0 1 0"}, "zTEST3":{"answer": "0 0 0 0"}, "zTEST4":{"answer": "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36"}, "zTEST5":{"answer": "0 0 1 0 2 1 3 0 4 2 5 1 6 3 7"}, "zTEST6":{"answer": "0 0 0 0 0 1 0 0 2 0 0 1 2"}, "zTEST7":{"answer": "0"}, "zTEST8":{"answer": "0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 1 2 1 0 0 0 0 0 2 2 3 1 0 0 0 0 0 3 1 0 0 0 1 0"}, "zTEST9":{"answer": "0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"}, "zTEST10":{"answer": "0 0 0 0 0 0 0 0 0 0"}, "zTEST11":{"answer": "0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 2 0 3 0 0"}}'
        data = json.loads(data)
        answer = ""
        for i in range (0,tests):
            ans = str(data["zTEST" + str(i)]["answer"])
            answer = answer +  '{ "stderr": "", "stdout": "' + re.sub("\\n", "\\\\n", ans) + '", "exception":   "null" },'
            if i == tests-1:
                answer = answer[:-1]

        data = '{  "problem": "' + str(problem) + '",  "user_code": "This is a python code.",  "language":  "python",  "answers": [    '+ answer +' ]}'
        try:
            data = json.loads(data)
        except:
            print("="*10 + "ERROR" + "="*10)
            print(data)
            exit()

        r = session.post(url="https://snakify.org/api/v2/solution/checkAnswers", json=data)
        print(r.status_code, end="")
        if str(r.status_code) == "200":
            print(" (success)")
    except:
        print("FAILED. Ignoring...")
        fail = fail + 1

    tries = tries + 1

print("\nDone. " + str(fail) + " Failed.")
exit()

# Programming [UNUSED]
program = ""
# input
program = program + "a = \"\"\nloop = True\nwhile loop:\n    try:\n        a = a + \"\\n\" + input()\n    except:\n        loop = False\ninput = a\n"

#PRINT METOHD

# 0
ipt = str(data["zTEST" + "0"]["input"])
ans = str(data["zTEST" + "0"]["answer"])
program = program + "if \"\"\"" + ipt + "\"\"\" in input and \"" + ipt[:1]  + "\" in input[:2]:\n"
program = program + "   print(\"\"\"" + ans + "\"\"\")\n"
# Other
if tests > 1:
    for i in range(1, tests):
        # if
        ipt = str(data["zTEST" + str(i)]["input"])
        ans = str(data["zTEST" + str(i)]["answer"])
        program = program + "elif \"\"\"" + ipt + "\"\"\" in input and \"" + ipt [:1]  + "\" in input[:2]:\n"
        program = program + "   print(\"\"\"" + ans + "\"\"\")\n"
        # print

# input = input()
# if input == {INPUT}:
#   print(ANSWER)

# OUTPUT
print("\n"*2 + "="*10 + "OUTPUT" + "="*10 + "\n")
print(program)
print("\n"*2 + "="*10 + "ENDPUT" + "="*10 + "\n")
