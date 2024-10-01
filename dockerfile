# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install venv module
RUN python -m ensurepip --upgrade

# Create a virtual environment in the container
RUN python -m venv venv

# Activate the virtual environment and install any needed packages specified in requirements.txt
RUN . ./venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose the ports for the WebSocket server and the Flask client
EXPOSE 8765
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=client.py

# Run both the WebSocket server and the Flask client using the virtual environment
CMD ["sh", "-c", ". ./venv/bin/activate && python Modules/Chat.py & flask run --host=0.0.0.0"]
