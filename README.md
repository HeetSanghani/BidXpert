BidXpert – Dockerized Django Auction Platform
=============================================

BidXpert is a Dockerized Django web application with PostgreSQL, fixtures,
media handling, and clean GitHub setup. This project is ready to run locally
using Docker with minimum setup.

--------------------------------------------------
PREREQUISITES
--------------------------------------------------

Make sure you have the following installed:

- Git
- Docker
- Docker Compose

Verify installation:

docker --version
docker-compose --version
git --version


--------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------

BidXpert/
│
├── BidXpert_app/
│   └── fixtures/
│       └── initial_data.json
│
├── BidXpert_pro/
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── static/
├── templates/
├── .env.example
├── .gitignore
└── README.txt

NOTE:
- media/ folder is NOT committed to Git (intentionally ignored).


--------------------------------------------------
ENVIRONMENT SETUP
--------------------------------------------------

Create a .env file in the project root:

nano .env

Add the following content:

DEBUG=True
SECRET_KEY=your-secret-key-here

POSTGRES_DB=bidxpert_db
POSTGRES_USER=bidxpert_user
POSTGRES_PASSWORD=bidxpert_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

Save and exit nano:
CTRL + O → Enter
CTRL + X


--------------------------------------------------
RUN PROJECT USING DOCKER
--------------------------------------------------

1) Build and start containers

docker-compose up --build

This starts:
- Django app on http://localhost:8000
- PostgreSQL database


--------------------------------------------------
DATABASE SETUP
--------------------------------------------------

Open a new terminal and run:

docker-compose exec web python manage.py migrate


--------------------------------------------------
LOAD FIXTURES (INITIAL DATA)
--------------------------------------------------

Load predefined data (categories, etc.):

docker-compose exec web python manage.py loaddata initial_data


--------------------------------------------------
CREATE ADMIN USER (OPTIONAL)
--------------------------------------------------

docker-compose exec web python manage.py createsuperuser

Admin panel:
http://localhost:8000/admin/


--------------------------------------------------
MEDIA FILES (IMPORTANT)
--------------------------------------------------

Media files are NOT stored in GitHub.

If your project needs images:
- Create a folder named "media" in project root
- Place images inside it

Expected path:

BidXpert/
└── media/

Django will automatically serve media in development mode.


--------------------------------------------------
VERIFY PROJECT
--------------------------------------------------

Open browser:

http://localhost:8000

Check:
- Homepage loads
- Categories are visible
- Images load (if media exists)
- Admin panel works


--------------------------------------------------
STOP PROJECT
--------------------------------------------------

To stop containers:

docker-compose down

To remove containers + volumes:

docker-compose down -v


--------------------------------------------------
COMMON FIXES
--------------------------------------------------

If ports are already in use:

docker rm -f bidxpert_web bidxpert_db

If Docker cache causes issues:

docker system prune -f
docker-compose up --build


--------------------------------------------------
TECH STACK
--------------------------------------------------

Backend  : Django
Database : PostgreSQL
Docker   : Docker & Docker Compose
Frontend : Django Templates + Bootstrap
Payment  : Razorpay (Test Mode)


--------------------------------------------------
AUTHOR
--------------------------------------------------

Heet Sanghani
Backend Developer – Django, Docker, PostgreSQL


--------------------------------------------------
FINAL NOTES
--------------------------------------------------

- Fully Dockerized
- Clean GitHub repo
- Secure environment variables
- Easy for any developer to run

--------------------------------------------------
