This bot helps to check availible slots on kdmid website.

Technology stack:

1. Python;
2. Aiogram3;
3. Redis;
4. Pydantic;
5. Docker-Compose;
6. Apsheduler;
7. BeutifulSoup
8. Dependency-injector

I used Dependency-injector for easy application configuration.
All dependecies are initialised in one place and nicely injected wherever needed.
The logic behind application is pretty strightforward: you need to check every day if slots
are availible which might be annoying.
This bot helps to make things smooth.
BeutifulSoup handles form submition, the only thing user is forced to do - to solve captcha.
Captcha is send as photo in chat, bot awaits user answer and proceed to the next step.
At the and user get info whether slots are availible or not
(and the link in case slots croped up). Cron job is handled by apcheduler.

To launch application:

1. create .env file using env_example;
2. run docker compose up -d.
