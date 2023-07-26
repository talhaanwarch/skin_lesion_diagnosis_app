FROM python:3.10-slim-buster
# Set the working directory inside the container
WORKDIR /myapp

# Copy the requirements.txt file to the container
COPY ./ ./

# Install the Python dependencies
RUN pip install -r ./requirements.txt --no-cache-dir 

CMD ["gunicorn", "--bind", ":8009", "--workers", "2", "main_app.wsgi:application"]