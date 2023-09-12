# Use an official Python runtime as a parent image
FROM python:3.7-slim as test

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run Tests
RUN python -m pytest

# Define environment variable
# Use this to specify environment variables like SLACK_TOKENS, DATA_URL
# ENV {'SLACK_TOKENS':'token1,token2', 'DATA_URL':'mydataurl'}

ENV API_PORT 5000

# Expose the Ports
EXPOSE $API_PORT

# Run app.py when the container launches
CMD ["python", "api/wtf.py"]