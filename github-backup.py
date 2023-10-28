import json
import subprocess

username = ""
allow_forks = False

def check_gh_installed():
    res = ""
    # check if gh is installed
    print("[task] checking if gh is installed...")
    try:
        res = subprocess.check_output("gh --version", shell=True)
        res = res.decode("utf-8")
    except Exception as e:
        print("[error] this program needs bash in linux with Github CLI (gh) to work.")
        print("[error] install with 'sudo apt install gh'")
        print("[error] now printing traceback:")
        print(e.with_traceback())
        exit(1)
    print("[success] gh is installed")

def convert_folders_to_lowercase():
    folders=  subprocess.check_output(["find",".","-maxdepth","1","-type","d"])
    folders = folders.decode("utf-8")
    folders = folders.split("\n")
    folders = [e.replace("./", "") for e in folders if e != "" and e != "."]
    for folder in folders:
        subprocess.call(["mv", folder, folder.lower()])
    print(*folders, sep="\n")

def timestamp():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d-%H-%M-%S")

def load_env():
    envf = None
    try:
        with open('env.json') as f:
            envf = json.load(f)
    except:
        envf = {
            "username": None,
            "allow_forks": None
        }

    global username
    username = ""
    if envf['username'] is not None:
        username = envf['username'].lower()
    else:
        username = input("Enter your github username: ").lower()
        print(f"creating backup file for '{username}'...")
        envf['username'] = username

    global allow_forks
    if envf['allow_forks'] is not None:
        allow_forks = envf['allow_forks']
    else:
        allow_forks = False
        if input("Do you want to also download forks? (y/n) ").lower() == "y":
            allow_forks  = True
        envf['allow_forks'] = allow_forks

    with open('env.json', 'w') as f:
        f.write(json.dumps(envf))
    

def create_backup_github():
    check_gh_installed()

    load_env()

    print("[task] getting repos...")
    # get repos
    try:
        subprocess.call("gh repo list --limit 1000 --json url,owner,parent > repos.json", shell=True)
        pass
    except:
        print("[error] could not get repos from gh")
    print("[sucess] repos saved to repos.json")

    data = None
    with open('repos.json') as f:
        data = json.load(f)

    repos = []

    for item in data:
        url = item['url'].lower()
        owner = item['owner']['login'].lower()
        print(username, url)
        name = url.split(f"https://github.com/{username}/")[1]
        parent = item['parent']

        if not allow_forks and (parent is not None or owner != username):
            print(f"[warning] skipping '{name}' because it does not belong to '{username}'")
            continue

        print("[task] cloning ", name)
        try:
            subprocess.call(["git","clone", url, name])
            repos.append(name)
        except:
            print("[error] could not clone ", name)
            continue

        print("[success] cloned ", name)

    print("[task] creating zip file...")
    convert_folders_to_lowercase()

    filename = f"{username}-github-repos-{timestamp()}.zip"
    zip_command = ["zip", "-r", filename, ' '.join(repos)]
    print("command: ", ' '.join(zip_command))
    out = subprocess.call(' '.join(zip_command), shell=True)

    print(f"[success] all repos saved in zip file {filename}")



# convert_folders_to_lowercase()
create_backup_github()