# twistter
CS 30700

#### Project Setup

First, install Django: https://docs.djangoproject.com/en/2.2/intro/install/

Then, clone this repository to your local machine.

Finally, in the root directory of this repo, run `python3 manage.py runserver` and navigate to `localhost:8000` - you should see a message from Django indicating it is running successfully.

#### Updating the DB

Run: `python3 manage.py migrate`

#### Running Tests

`python3 manage.py test test/`

#### Setting Up Admin

`python3 manage.py createsuperuser`
