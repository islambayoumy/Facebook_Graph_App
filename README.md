# Facebook_Graph_App
POC of creating a manual login flow with Facebook Graph API
#### ~ It isn't a ready for production

## Getting start (deployment)
### Prerequisites
* python 3
* virtualenv

### 1. Clone project
`$ git clone https://github.com/islambayoumy/Facebook_Graph_App`<br />
`$ cd Facebook_Graph_App`<br />
~ change directory to project folder  

### 3. Activate Virtualenv
`$ . env/Scripts/activate`

### 4. Change directory to the Django app
`$cd FB_Login/`

### 5. Create Facebook application and get key & secret.
Check this link: [Facebook Doc](https://developers.facebook.com/docs/apps/)

### 6. Change FACEBBOOK KEY & SECRET in the FB_Login.settings
`FACEBOOK_KEY = 'YOUR-FB-APP-KEY'`<br />
`FACEBOOK_SECRET = 'YOUR-FB-APP-SECRET'`

### 7. Run server
`$(env) python manage.py runserver`

* Start browsing the application through http://127.0.0.1:8000/
