About
=====
http service for submitting metrics to carbon(Watcher)


## Run
```sh
$ cd /path/to/carbon-http
$ python tools/install_venv.py
$ tools/with_venv.sh python setup.py develop
$ tools/with_venv.sh carbon-http --config-file=etc/development/carbon-http.conf
```
