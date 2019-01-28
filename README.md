# Labs_web [![Maintainability](https://api.codeclimate.com/v1/badges/ec3966366e6ea426b520/maintainability)](https://codeclimate.com/github/AlexPraefectus/labs_web/maintainability) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

### Project goals

- Automated lab work reports sending & checking
- Automated Q&A for students and tutors  (no need to search a phone number/personal email of a tutor)
- Automated announcements for tutors 
- Make all course documents & all marks for lab works available 24/7 (a big problem of ukrainian universities)
- Some statistics to see how You perform relative to other

### Project stack
Disclaimer: I know that use of all these services / practices / technologies is a big overkill for this project. Common pair of web server + relational database would be quite enough for these goals but this project is also educative for myself


| Purpose       | Tech              |
| ------------- | --------------    |
| Web server    | Flask + Gunicorn  |
| RDMS          | PostgreSQL        |
| Caching       | Redis             |
| Task Queue    | Celery + Redis    |
| NoSQL Storage | MongoDB           |
| Front end     | Bootstrap + JQuery|
| Deployment    | Docker/AWS        |


### How to launch?
```bash
sudo docker-compose up
```
in root directory of the project
