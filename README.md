# udacity-catalog
This is a musical instrument catalog for the Udacity Full Stack Web
Developer Nanodegree.

Two extra credit features are implemented:
* Items have pictures that are exposed to the CRUD operations.
* Minimal CSRF protection is implemented to prevent fraudulent deletion of items.

## How-to
The environment is assumed to be the standard Vagrant box distributed by Udacity, which
includes Python, Flask, and noSQL.

Steps to start the catalog:

1. Clone the directory heirarchy in this repo.
2. Set up OAUTH2 for a new web app at https://console.developers.google.com .
3. Obtain a client_secrets.json file for the new web app and put it in the same
directory as catalog.py. [Note: in real app deployments, client_secrets.json should not be 
in a location accessible to the outside world.]
4. In the directory where catalog.py lives, run the following at a command prompt:

        $ python database_setup.py
        $ python database_populate.py
        $ python catalog.py
5. Point a browser at http://localhost:8000/

## Features
OAUTH2 login is provided through Google. Facebook login is not supported because 
Facebook has repeatedly proven it can't be trusted with users' privacy.

Logged-in users can add instruments from either the front page or any category page.
Users can edit and/or delete instruments they added, but not those added by others.
The new/edit form checks that the required fields (category and name) have values.

The add, edit, and delete links are hidden from visitors who are not logged in.

## Legal
All images in this project are used without permission. Fair use is claimed due to 
the educational nature of the project. 