# searching_pass
![Python version](https://img.shields.io/badge/python-3.8-yellow)

```
This programm looks for the shortest way between 2 Moscow subway stations. It consists of two parts:
- First part (parse.py) parses json file and packs data to pickle file.
- Second part (search.py) unpacks pickle file and use the data to find the shortest way. 

Second part uses Dijkstra's algorithm to search. It also uses prettytable to show result in readable form without GUI.
You don't need to create or delete pickle file manualy.
```

## Run the project
- Clone this repo
- Create and activate virtual environment
```
- mac/linux
python3 -m venv venv
source venv/bin/activate

- windows
python -m venv venv
source venv/Scripts/activate 
``` 

- Install dependencies from requirements.txt
```
pip install -r requirements.txt
``` 

- Move to 'src' folder
```
cd src
```

- Run 'search.py' file
