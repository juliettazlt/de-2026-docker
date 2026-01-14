FROM python:3.13.11-slim


# now copy uv instead of using pip install
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
# set working directory 
#/app means all commands such as copy, run, etc will be run in this directory
#/app is created if it doesn't exist
# why /app? just a convention, could be anything
WORKDIR /app 

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

#Copy dependecies file to WORKDIR
COPY "pyproject.toml" "uv.lock" ./ 
# ./ means current working directory, which is /app, meaning copying to /app
# why no ./ when copy uv? because we are copying to /bin, which is not the WORKDIR
# so what follows COPY are 1. source file, 2. destination file


RUN uv sync --locked

#copy the script to the container. 1st name is source file, 2nd is destination
# the destination is the same name in this case, but we could change it if we wanted
COPY iamSoCool.py iamSoCool.py

# define what to do first when the container runs
# "python" means run python interpreter, "iamSoCool.py" is the script to run
ENTRYPOINT ["python", "iamSoCool.py"]

# what we need to do now in the command line is build the docker image
# docker build -t <image_name> . # here we use taxi_ingest:v001 - taxi_ingest is the name, v001 is the tag
# what is a tag? a way to version images, like v1, v2, etc
# we start from the python:3.13.11-slim image, then add our stuff on top of it to create a new image
# after building the image, we can run the container
# what is a container? a running instance of an image; 
# we can always create new containers from the same image everytime we run it using docker run
# docker run <image_name>
# for example, docker run test:pandas  
# this will run the iamSoCool.py script in the container

