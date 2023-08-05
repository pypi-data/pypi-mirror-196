# Autonon

Autonon is a library to server a end to end machine learning pipeline. We are developing modules one by one. Currently, we developed feature extraction(AFE) and data quality modules(IDQ). There are more to come...

- [Documentation](https://organonanalytics.atlassian.net/wiki/spaces/AOT/pages/2095546790/Getting+started)
- [Code of Conduct](https://gitlab.com/organon-os/autonon/-/blob/main/CODE_OF_CONDUCT.md)
- [Contribution](https://gitlab.com/organon-os/autonon/-/blob/main/CONTRIBUTING.md) 
- Bug reports:  You can use GitLab issues.
- Contact: support@organonanalytics.com
- Company website: [Organon Analytics](http://www.organonanalytics.com/) 

## Installation
```shell
pip install autonon
```

### Requirements
A compiler for C is required for building cython modules. Check requirements for your operating system in https://cython.readthedocs.io/en/latest/src/quickstart/install.html

For oracle connections, cx_Oracle library is used. This library requires Oracle Client Libraries to be installed.
Please follow the instructions in the link : https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#install-oracle-client


### Preparing Development Environment
After you pull the code, run 
```shell
cmd /c setup.bat
```
for Windows
```shell
chmod u=rwx setup.sh
./setup.sh
```
for Linux.

This script will prepare a virtual environment('orgenv') and build cython source files.
Then, you can start development after activating "orgenv" environment

**NOTE:** Script uses default python version in your system to generate the virtual environment. 
If your default python version is less than 3.8 or you want to use another python version, 
you can change the "python" commands in the script with the path to python version you want to use.

### Unit Tests And Coverage
To run unittests and measure code coverage:
* Activate 'orgenv' virtual environment
* Run command to run coverage: 
  ```shell
  coverage run --omit='*orgenv*' -m unittest organon/all_tests.py
  ```
* Run command to get coverage report:  `coverage report`

### License

This project is licensed under the terms of the [MIT License](LICENSE)
