# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Run main_agent.py when the container launches
# This command is for running the agent manually with the --run-now flag
# For scheduled runs, you would typically use a cron job or similar outside the Docker container
CMD ["python3", "src/main_agent.py", "--run-now"]


