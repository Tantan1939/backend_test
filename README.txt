
------------------------------- Instructions to run this backend test -------------------------------


Step 1: From my github repository, click the green button name "<> Code".
Step 2: Under HTTPS, copy the link displayed.
Step 3: On your local machine, create a folder and name it my_dir
Step 4: Go to my_dir folder and select the address bar, then type cmd and hit Enter.
    On cmd,
    Step 4.1: Type pip install virtualenv and hit Enter
    Step 4.2: Type virtualenv --python python3 . and hit Enter
    Step 4.3: Type git clone and paste the link from my github repository, then hit Enter.
    Step 4.4: Type cd backend_test and hit Enter.
    Step 4.5: Type pip install -r requirements.txt and hit Enter.

Step 5: Setup connection with postgresql:
    Step 5.1: Open your pgadmin.
    Step 5.2: Create a database and name it shopDB
    Step 5.3: Open the settings.py from backend_test folder.
    Step 5.4: Add your user postgres password in line 84.

Step 6: Perform Migration to the database.
    On cmd,
    Step 6.1: Type python manage.py migrate shop 0001_initial and hit Enter.
    Step 6.2: Go to your pgadmin, right-click the shopDB database and select CREATE Script.
    Step 6.3: Click ctrl + a simultaneously to clear texts.
    Step 6.4: Copy the text from PGscripts.txt in backend_test folder.
    Step 6.5: Paste it on the query editor in the pgadmin.
    Step 6.6: Click F5 or the play button.
    Step 6.7: On cmd, type python manage.py migrate and hit Enter.

--- Steps to use the scripts in tasks ---
Step 1: On cmd, cd to backend_test.
Step 2: Type python manage.py shell and hit Enter.
Step 3: Type from shop.tasks import * and hit Enter.
Step 4: Type get_due_products() and hit Enter.
Step 5: Type create_new_invoice() and hit Enter.
Step 6: To exit, click ctrl + z simultaneously and hit Enter.


--- To run in localhost ---
Step 1: On cmd, cd to backend_test.
Step 2: Type python manage.py runserver and hit Enter.
Step 3: Copy the localhost link and paste it on your chrome, then hit Enter.
Step 4: Select a database table from your left screen-view to add, edit, and delete data.