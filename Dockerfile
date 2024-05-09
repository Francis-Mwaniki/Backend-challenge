FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . /app/

# Migrate the database
RUN python manage.py migrate

# Set environment variables
ENV AUTH0_CLIENT_ID=your_auth0_client_id
ENV AUTH0_CLIENT_SECRET=your_auth0_client_secret
ENV AUTH0_DOMAIN=your_auth0_domain
ENV AFRICAS_TALKING_USERNAME=your_africastalking_username
ENV AFRICAS_TALKING_API_KEY=your_africastalking_api_key

# Expose the port and start the server
EXPOSE 3000
CMD python manage.py runserver 0.0.0.0:3000