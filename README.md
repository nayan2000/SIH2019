SMART INDIA HACKATHON 2019

This repository contains the server side code for project 'Alertify' which we developed during Smart India Hackathon 2019. Alertify aims to predict tsunami and issue alerts in the nearby areas and the georadius is decided by the intensity of the earthquake. It has support for District Administrators to issue bulk customised SMS messages, monitor the rescue operations. The alertify app has a facility for users to donate for the victims. There is a chatBot section for users to seek help and important information related to rescue operations and supply timings. It also has a New section wherein live tsunami related news are shown.
Basically our product aims to predict tsunami and alert people, if predicted one.


Also, we plan to help the rescue officials in carrying out the necessary rescue operations through an App+WebPortal.

To get started with this,

source venv/bin/activate
cd sih
python manage.py runserver

For Security purposes, I Have removed all my API keys from sih/keyconfig.py
You need to generate all these keys from your account for getting the app running.
