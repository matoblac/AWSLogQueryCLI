# AWSLogQueryCLI

## Description

AWS Log Checker is a versatile tool for querying and analyzing AWS CloudWatch and CloudTrail logs, helping to streamline log management and monitoring. Its functionality can be extended for automation.

## Prerequisites

- Python 3.6 or higher
- AWS credentials configured

## Installation 

1. Clone the repository:
    ```sh
    git clone git@github.com:matoblac/AWSLogQueryCLI.git
    cd AWSLogQueryCLI
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create an executable script `alqc`:

    ```sh
    echo -e '#!/bin/bash\npython /path/to/your/project/main.py "$@"' > alqc
    chmod +x alqc
    ```

    Replace `/path/to/your/project/` with the actual path to your project directory.

5. Add the script to your PATH:

    ```sh
    sudo mv alqc /usr/local/bin/
    ```

    Alternatively, you can add your project's directory to your PATH by adding the following line to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile` file (depending on your shell):

    ```sh
    export PATH="$PATH:/path/to/your/project"
    ```

    Then, reload your shell configuration:

    ```sh
    source ~/.bashrc  # or source ~/.zshrc or source ~/.bash_profile
    ```

## Usage

1. Run the script using the custom command:
    ```sh
    alqc "12-15-2023 14:30"
    ```

2. Choose an option:
    - 1: CloudFormation Logs
    - 2: CloudWatch Logs
    - 3: Help

3. Follow the prompts to query logs or get help.

## Example
```sh
alqc "12-15-2023 14:30"


## Example
```sh
python main.py "12-15-2023 14:30"
```

### Testing With `moto`

create a test file using `moto` to mock AWS services.

You can run your tests using the following command:
```sh
python -m unittest discover -s tests
```


## TODO
1. main.py needs to be changed to something more descriptive of the actual program begin ran...

2. Add an option for parsing CloudTrail

3. It needs to be clearly explained that the time in `python main.py "12-15-2023 14:30"` is the endtime so, the query will be from `14:00 - 14:30` 

4. Create tests for CloudFormation 