# tee-cli

This tool is a python implementation of a `tee`. 
- It captures stderr+stdout from a `command` and will save it to a file and will print them to a console.
- It propagates `command` exit code correctly.

```bash
tee-cli --help
usage: tee-cli [-h] [-o OUTPUT] command

positional arguments:
  command     Command to run

options:
  -h, --help  show this help message and exit
  -o OUTPUT   Path to output log file with stdout+stderr content
```
