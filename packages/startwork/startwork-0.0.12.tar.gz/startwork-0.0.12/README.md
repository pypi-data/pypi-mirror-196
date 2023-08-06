# Start-Work

Small CLI to easier start and swap between projects in different stacks.

Published to [PyPi](https://pypi.org/project/startwork/)


## motivation

It's not hard to set up and run most modern software projects.

Usually, we just have to run two something like `pip install -r requirements.txt`
 and `flask run` or something similar. The real problem comes we you have to
 constantly switch contexts, even worse when working with multiple projects in
 multiple languages with totally different setups a couple of times a day.

[Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) are great tools to handle this problem. Start Work
 should not be a replacement for Docker either Docker compose and shall even
 work with both.

With Start-Work will be easier to switch between projects from any folder and
 get your development environment up and running only by selecting the project
 you wanna work on, and when some of these projects for some reason don't allow 
 Docker, Start-Work will also try to identify which tools you are using and run
 it for you.

## Installation

Just run:
```bash
pip install startwork
```

It's done, the installation can be verified with:
```bash
work --version
```

## CLI Options


```bash
work
```
Will display a list and let you select one of your saved projects

<br />

```bash
work create
```
Will guide you with a couple of questions to save a new project.

<br />

```bash
work delete
```
Will display a list and let delete one of your saved projects.

Note: it will not remove the project from your computer, only from the list on
 Start-Work

<br />

```bash
work --version
```
Show current version

<br />

```bash
work --help
```
Show currently available CLI options
