#custom django app with some custom APIs

#steps for local setup and run
1. pip install -r requirements.txt

2. python manage.py make migrations (just in case)

3. python manage.py make migrate

4. python manage.py make runserver

Your application will be running and you can use the APIs in the urls files

If you need to access the admin console you need to create a superuser with the following command:

    python manage.py make createsuperuser



Functions:

- An API for creating new users which takes username and password in json request.
- An API for authentication,takes username and password as a json request and returns a JWT     token in response.
- Saves user details in a Sqlite database.
- Every time client calls our authentication API, we trigger a webhook sending users IP.
- For every login, a history of ip address is kept in a model (UserLoginHistory)
- custom action to the UserLoginHistory model in the django admin interface that allows the selected record to be exported as CSV.
- This application is also hosted on heroku
link - https://desolate-hamlet-81823.herokuapp.com/
admin credentials = username -admin
                    password -admin


