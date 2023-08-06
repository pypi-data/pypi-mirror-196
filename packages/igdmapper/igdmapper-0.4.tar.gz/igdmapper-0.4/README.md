# IGD-mapper

IGD-mapper is a simple Python script used to setup IGD (Internet Gateway Device) NAT rules though UPnP.
The script use a config file (/etc/igd-mapper.ini) that contains the rules for a given host. 

IGD-mapper can be used in network "PostUP" script and crontab. 


 ![IGD-mapper](./screenshots/shot.jpg)

    
## Install
Several options are available:

    python setup.py install (or develop)

Install directly from github (easier) 

    pip install git+https://github.com/jkerdreux-imt/igd-mapper.git

Run in a pipenv 

    pipenv sync
    pipenv run igd-mapper

## Run

    igd-mapper 

Options 

    usage: idg-mapper [-h] [-c CONFIG] [-l] [-f] [-d] [-q]

    optional arguments:
    -h, --help  show this help message and exit
    -c CONFIG   config file
    -l          only list nat rules
    -f          only drop nat rules
    -d          enable debug
    -q          quiet, disable output



## Notes
IGD-mapper use custom string to name rules (igd-mapper-hostname). This provides an easy way to find them, and clear old rules.
