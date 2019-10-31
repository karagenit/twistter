# twistter
CS 30700

#### Project Setup

First, install Django: https://docs.djangoproject.com/en/2.2/intro/install/

Then, clone this repository to your local machine.

Finally, in the root directory of this repo, run `python3 manage.py runserver` and navigate to `localhost:8000` - you should see a message from Django indicating it is running successfully.

#### Updating the DB

Run: `python3 manage.py migrate`

Also, you'll need to create a file named `.env` with the following contents:

```
DATABASE_URL=sqlite:///db.sqlite3
```

#### Running Tests

`python3 manage.py test test/`

#### Setting Up Admin

`python3 manage.py createsuperuser`

#### Preloading Data

`python3 manage.py add_data`

This will create a couple example users, posts, reports, etc. to make testing easier. You will probably need to wipe the DB with `python3 manage.py flush` first, which will also require you to recreate the admin account.

#### Uploading to Heroku

First, install the heroku command line utility, create a heroku app, and provision the postgres addon.

Then, set the heroku remote to your app name and push to the heroku repo via `git push heroku master`.

Then, setup the database with `heroku run python3 manage.py migrate`.
