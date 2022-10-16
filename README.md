## Pre-requisites

1. Python 3.9.* and pip <br>
(If you create a new enviroment be sure to have the previous)
2. Install requirements: <br/>`pip install -r requirements.txt`

## Execution
1. Clone the repo
2. Open a terminal in the folder of the project
3. Run:<br/>
`python main.py [PATH to input.json]`

The path is mandatory. In case you need extra help execute the following: <br>
`python main.py -h`

4. The result will be displayed in the terminal, and it will be saved in output.json

### Constants
Inside constants.py there are a bunch of constants which configure the entire project.
If you want to change any functionality, update those variables. E.g. in finance, usually years are represented by 360 days, this can be found on the constant `DAYS_IN_YEAR`.