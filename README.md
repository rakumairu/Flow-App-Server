# FlowClient

A project that i created as my final assignment to get my bachelor degree
This project's aim is to provide API to be used in [FlowClient](https://gitlab.com/rakumairu/flow-client) project 

This project was created with [Flask RESTful](https://flask-restful.readthedocs.io/en/latest/) version 0.3.7.

## Getting Started

To start using this app please follow the instructions below

### Prequisites

* Install [Python 3.X](https://www.python.org/downloads/)
* Clone this project to your local computer

I'm using Python version 3.7

### Installing

Installing all packages required in this app

Open command prompt/terminal and move to this project folder then install all requirements for this project

```
cd flow-server
pip install -r requirements.txt
```

**for macOS/linux user, use pip3 instead of pip command**

### Running the server

To run this app, you can run the development server using this command

```
python wsgi.py
```

**for macOS/linux user, use python3 instead of python command**

and then you can access the api

## API list

* Files: http://127.0.0.1:5000/api/files
* FileExist: http://127.0.0.1:5000/api/exist
* Display: http://127.0.0.1:5000/api/display
* Preprocessing: http://127.0.0.1:5000/api/prepos
* Convert Time: http://127.0.0.1:5000/api/convert
* Giving Alias: http://127.0.0.1:5000/api/alias
* Join two Columns: http://127.0.0.1:5000/api/join
* Drop a column: http://127.0.0.1:5000/api/drop
* Statistic Summary: http://127.0.0.1:5000/api/statisticsummary
* Statistic Start Event: http://127.0.0.1:5000/api/statisticstart
* Statistic End Evet: http://127.0.0.1:5000/api/statisticend
* Filtering: http://127.0.0.1:5000/api/filter
* ControlFlow: http://127.0.0.1:5000/api/controlflow
* DottedChart: http://127.0.0.1:5000/api/dottedchart
* DottedChartDuration: http://127.0.0.1:5000/api/dottedchartduration

## Deployment

Project still a work in progress, and haven't tested in live server yet

## Author

* **Demaspira Aulia** - [rakumairu](https://github.com/rakumairu) 

For further question you can contact me here: demaspiraa@gmail.com

## Acknowledgments

* Rizqi Hadi Prawira - [DoublesInLove](https://github.com/doublesinlove)