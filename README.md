# device-management
A device management inventory tool. In this demo you can seed the database with random data and display it as a table in the frontend.
The devices can be edited and changes are reflected immediately. This project is by far not finished yet, one milestone would be
adding the processing of a PowerShell script, that would be automatically sent by a computer whenever a user logs in.

## Technologies

Following technologies have been used:

- [**Flask**](https://palletsprojects.com/p/flask/) *as a Python REST-API resource server backend.*
- [**Vue.js**](https://vuejs.org/) *as a Javascript SPA client frontend.*
- [**PostgreSQL**](https://www.postgresql.org/) *as a relational database.*
- [**Docker**](https://www.docker.com/) *in order to isolate and virtualize each application component above in a container.*

## What I learned

About Vue.js I gained more experience through this little project. For example data that is passed as props to the child component
should not be modified, instead make a separate object in the `data()` property. Also the reactivity system of Vue I learned the
hard way. Changes aren't immediately visible in the DOM when using a simple Javascript state management object. Instead for a simple
store, use the `Vue.obeservable()` object, which then can be used in the computed property of a component. Also about JWT and how they
should be stored I learned a lot. In this project I saved both, the access and refresh token in memory, therefore if you refresh the
browser you will be logged out of the app. How to intercept requests with axios was also vey educational.

## Installation guide

Prerequisites: Make sure you have [**Docker**](https://docs.docker.com/get-docker/) and [**Docker-Compose**](https://docs.docker.com/compose/install/) installed.

1. &nbsp;Clone this project to your computer.

2. &nbsp;`cd`&nbsp; into the project folder.

3. &nbsp;Run &nbsp;`docker-compose up -d --build`&nbsp; to set up and start the docker containers.

4. &nbsp;Run &nbsp;`docker ps`&nbsp; to see the running containers and their ports.

5. &nbsp;Seed the Postgres Database with random devices and their purchase details data. For this, execute the following command in the project root:
&nbsp;`docker-compose exec backend python manage.py seed_db`&nbsp;. You'll be informed that the database, the admin login account and the random
devices have been created.

5. Open your favourite browser and enter &nbsp;`http://localhost:8080`&nbsp; in the address bar in order to call the Vue app.

## Test the app

1. Username is `admin` and the password is `pass`. After the login you get redirected to the home `/` route.

3. &nbsp;You may notice that the navigation bar element "Dashboard" appeared at the top and also the Login button changed to Logout, meaning we are authenticated and can access the dashboard.

4. &nbsp;Now when you click on "Dashboard", all devices will be requested from the Flask backend and are shown in a [**Buefy**](https://buefy.org/documentation/table/) table.

5. &nbsp;When you click on a row (device), the `Edit Device` window pops up where you can edit only the purchase details fields, but not the device unique identifier fields like the serial number and the computer name.


