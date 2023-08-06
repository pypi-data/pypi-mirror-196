from setuptools import setup

setup(
    name='shibasphoorthi',
    version='0.1',
    description='My Python module',
    packages=['shibasphoorthi'],
    install_requires=[
        'requests',
    ],
)

"""

import tarfile
import datetime

# Set the directory to back up and the backup destination
directory = '/path/to/directory'
backup_destination = '/path/to/backup/folder'

# Create the backup filename with a timestamp
backup_filename = 'backup_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.tar.gz'

# Create the tar archive
with tarfile.open(backup_destination + '/' + backup_filename, 'w:gz') as tar:
    tar.add(directory, arcname='')

# Print a message indicating the backup was successful
print('Backup created: ' + backup_filename)


#0 2 * * * /usr/bin/python3 /path/to/backup_script.py

This cron job runs the script /path/to/backup_script.py every day at 2am. You can modify the timing as needed.
import os

packages = ['package1', 'package2', 'package3']

for package in packages:
    os.system(f'sudo apt-get install {package} -y')


import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]
model_engine = "text-davinci-002"  # Change this to your preferred GPT model

def ask_gpt(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

prompt = "Hello, I'm ChatGPT. How can I assist you today?"
while True:
    user_input = input("You: ")
    prompt += "\nUser: " + user_input
    response = ask_gpt(prompt)
    prompt += "\nChatGPT: " + response
    print("ChatGPT:", response)

#Script to monitor system resources using psutil:
import psutil

cpu_percent = psutil.cpu_percent(interval=1)
memory_percent = psutil.virtual_memory().percent
disk_percent = psutil.disk_usage('/').percent

print(f'CPU usage: {cpu_percent}%')
print(f'Memory usage: {memory_percent}%')
print(f'Disk usage: {disk_percent}%')
"""
