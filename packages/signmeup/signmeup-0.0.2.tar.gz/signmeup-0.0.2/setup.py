from setuptools import setup, find_packages
import os
import subprocess

def post_install():
    message = "signmeup has been installed."
    print(message)

    choice = input("Do you want to start a sample project? (y/n): ")
    if choice.lower() == 'y':
        project_name = input("Enter the project name (default: core): ") or "core"
        create_project(project_name)

def create_project(project_name):
    try:
        subprocess.run(["django-admin", "startproject", project_name])
        update_project_structure(project_name)
    except Exception as e:
        print(f"Error creating project: {e}")

def update_project_structure(project_name):
    base_dir = os.getcwd()
    source_dir = os.path.join(base_dir, "signmeup")
    destination_dir = os.path.join(base_dir, project_name)

    try:
        subprocess.run(["cp", "-r", source_dir, destination_dir])
        os.rename(os.path.join(destination_dir, "signmeup"), os.path.join(destination_dir, project_name))
        print("Sample project created successfully!")
    except Exception as e:
        print(f"Error updating project structure: {e}")

setup(
    name='signmeup',
    version='0.0.2',
    description='Sign-Me-Up API',
    author='Your Name',
    author_email='yourname@example.com',
    packages=find_packages(),
    install_requires=[
        'asgiref==3.7.2',
        'Django==4.2.2',
        'django-cors-headers==4.1.0',
        'djangorestframework==3.14.0',
        'Pillow==10.0.0',
        'psycopg2==2.9.6',
        'python-dotenv==1.0.0',
        'pytz==2023.3',
        'sqlparse==0.4.4',
        'typing_extensions==4.6.3',
        'tzdata==2023.3',
    ],
    entry_points={
        'console_scripts': [
            'signmeup = signmeup:post_install',
        ],
    },
)
