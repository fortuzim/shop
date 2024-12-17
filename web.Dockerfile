# Base image
FROM python:3.12.3

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /shop

# Install system dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Copy project files
COPY . /shop/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Entrypoint script
COPY entrypoint.sh /shop/entrypoint.sh
RUN chmod +x /shop/entrypoint.sh

# Expose the port on which Django runs
EXPOSE 8000

# Entrypoint for container
ENTRYPOINT ["/shop/entrypoint.sh"]
