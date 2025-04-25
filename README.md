ABOUT THIS PROJECT

This is a simple webscrapping script where the goal is to scrape a product (surfboard) which fits some requiremens (size and material made) and is On Sale. For that, the board is searched reading the html code obtained with selenium and filtered with regex. The matches are sent from e-mail with the link, description of the board and two images - back and front of the board. The scrapping is schedulle to be executed with cron(Unix). Everything runs inside a Docker container. 



HOW TO RUN

You need:
* Docker

1. Create a file named 'app.properties' in dockerpy folder. This file must contain two variables: 'mail' and 'password', which will be used for SMTP mailing.
For more, read doc jproperties: https://pypi.org/project/jproperties/

2. Edit the ./dockerpy/cron_job file to set when the script is gonna be executed.
Obs. cron runs in UTC+0. So, you need to consider this when aiming a fixed hour for a cronjob. 

3. Your e-mail must be configured to allow 'app passwords'. See gmail apps & passwords documentation for more.



if not using docker...

* Firefox (you can adapt the script to use chrome)
* Geckodriver (Selenium w/ Firefox)
* A Gmail account (optional)

1. Install de dependencies (requirements.txt).
2. mailing will be optional, so you can set or not the app.properties file.
3. cron will not be used --> run the jupyter notebook 'main.ipynb'