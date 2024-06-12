# AWSLogQueryCLI

## Description

AWS Log Checker is a versatile tool for querying and analyzing AWS CloudWatch and CloudTrail logs, helping to streamline log management and monitoring. It's functionality can be extended for automation

## prerequisites

- Python 3.6 or higher
- AWS credentials configured

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. Choose an option:
    - 1: CloudFormation Logs
    - 2: CloudWatch Logs
    - 3: Help

3. Follow the prompts to query logs or get help.

## Example
```sh
python main.py "12-15-2023 14:30"
```

## TODO
1. main.py needs to be changed to something more descriptive of the actual program begin ran...

2. Add an option for parsing CloudTrail

3. It needs to be clearly explained that the time in `python main.py "12-15-2023 14:30"` is the endtime so, the query will be from `14:00 - 14:30` 