# github-backup

Compresses all your github repos into a single neat `.zip` file.

## Requirements

- linux
- python3
- Github CLI logged in (sudo apt install gh)

## How to use

Run: `python github-backup.py`

Sample execution:

```
python github-backup.py

[task] checking if gh is installed...
[success] gh is installed
Enter your github username: renatobrittoaraujo
creating backup file for 'renatobrittoaraujo'...
Do you want to also download forks? (y/n) n
[task] getting repos...
[sucess] repos saved to repos.json

...

[success] all repos saved in zip file renatobrittoaraujo-github-repos-01/01/70-00-00-00.zip
```
