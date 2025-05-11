
# Device-And-Operation-Management-For-IT-Department
## Setup Instructions

Follow these steps to get your local development environment up and running.

### 1. Create a Virtual Environment

First, create a virtual environment to isolate your project dependencies. You can do this with the following command:

```bash
python3 -m venv venv
````

Activate the virtual environment:

* On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

* On Windows:

  ```bash
  .\venv\Scripts\activate
  ```

### 2. Install Dependencies

Install the required libraries by running the following command:

```bash
pip3 install -r requirements.txt
```

This will install all the dependencies listed in your `requirements.txt` file.

### 3. Create PostgreSQL Database

Make sure you have PostgreSQL installed and running. Create a new PostgreSQL database with the following commands:

```bash
psql -U postgres
CREATE DATABASE your_db_name;
```

Replace `your_db_name` with your desired database name.

### 4. Initialize Data

Run the `setup` script to initialize the data and any necessary database migrations:

```bash
./setup
```

This script will set up the initial data required for the project to run properly.

### 5. Access the Admin Panel

Once everything is set up, you can access the Django Admin panel by navigating to the following URL in your browser:

```
http://127.0.0.1:8000/admin
```

Login with your admin credentials to manage the project data.

## Additional Information

* Make sure PostgreSQL is properly configured on your system.
* The `setup` script assumes that you have already created the PostgreSQL database and set up any necessary configurations.

---

### Troubleshooting

* If you run into issues with PostgreSQL, make sure that the PostgreSQL service is running and that your credentials are correct.
* If the `./setup` script fails, double-check the file permissions and ensure that the necessary migrations are applied.

```

Feel free to replace placeholders like `your_db_name` with the actual names/values relevant to your project. You can also expand on the troubleshooting section if there are known common issues!
```
If you want to deploy it on server, follow this guide: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu
