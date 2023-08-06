# Visual studio code extension downloader
```
positional arguments:
  {query,download}      Action
options:
  -h, --help            show this help message and exit
  -n N                  extension name
  -v V                  extension version check
  -o O                  file name
  --disable-tls-verify  disable TLS check
  --version             show program's version number and exit
```

## Install
```shell
pipx install vsc-ed
```

## Examples
Download
```shell
vsc-ed download -n ms-python.python
```
Download if the current version number is greater than 1.0.0
```shell
vsc-ed download -n ms-python.python -v 1.0.0
```
Query extension metadata(json)
```shell
vsc-ed query -n ms-python.python
```