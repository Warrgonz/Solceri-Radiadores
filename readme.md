
![Logo](https://solceri.s3.amazonaws.com/logoSolceri.png)

Solceri Forge is a website created for the company Solceri Radiadores, specifically designed for managing radiator repair and maintenance requests. This platform allows these requests to be managed through a ticketing system, facilitating the organization and tracking of each case.

The ticketing system of Solceri Forge allows customers to create requests for radiator repairs or maintenance quickly and easily. Once the request is created, customers can know the current status of their request in real-time, providing transparency and trust in the process.

## Authors

Warren González Reyes
- [@warrgonz](https://github.com/Warrgonz)

Alejandro Castro García
- [@acastrog38](https://github.com/acastrog38)

Royner Badilla 
- [@Royner26](https://github.com/Royner26)


## Table of Contents
- [Setup](#setup)
  - [Creating a Virtual Environment](#creating-a-virtual-environment)
  - [Installing Requirements](#installing-requirements)
  - [Running Requirements](#running-requirements)
- [Features](#features)
- [Support](#support)

## Setup

### Creating a Virtual Environment

To create a virtual environment in Python, follow these steps:

1. Open your terminal (or command prompt).
2. Navigate to your project directory.

> [!IMPORTANT]
> You must have to install Python in your computer and be sure that you added Python to PATH. You can check if you have Python and Pip using the following command in your terminal (PowerShell, Git Bash, etc.)

```sh
python3 --version
pip --version
```

3. Run the following command to create a virtual environment:

Install virtualenv

```sh
pip install virtualenv
```

Create the virtual environment

```sh
virtualenv -p python3 env
```

Activate the virtual environment

- Git Bash

```sh
source env/Scripts/activate
```

- Powershell

```sh
    .\env\Scripts\Activate
```

### Installing Requirements

After activating your virtual environment, you need to install the necessary packages. Make sure you have a `requirements.txt` file in your project directory. Run the following command:

```sh
pip install -r requirements.txt
```
> [!NOTE]
> To install additional dependencies, you can use the following prompts

- Install the package and update requirements.txt, change `<Monofino>` to the package required.

```sh
pip install <Monofino> && pip freeze > requirements.txt
```
- Verify that the package is installed

```sh
pip show <Monofino>
```

- Uninstall the package (If required)

```sh
pip uninstall <Monofino>
```

- Update requirements.txt

```sh
pip freeze > requirements.txt
```

### Running project

To server start, you can use `./app` in your terminal where the proyect will initialize in your localhost.

## Features

To view the user stories contained in our application, please check the backlog at the following link:

[Backlog](https://github.com/users/Warrgonz/projects/1)

## Support

For support, you can contact us to `wgonzalez90631@ufide.ac.cr`, `acastro40720@ufide.ac.cr` , `rbadilla30943@ufide.ac.cr`.
