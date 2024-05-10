FROM python:3.9


# Set environment variables
ENV AUTH0_CLIENT_ID=your_client_id
ENV AUTH0_CLIENT_SECRET=your_client_secret
ENV AUTH0_DOMAIN=your_domain
ENV AFRICAS_TALKING_API_KEY=your_api_key
ENV AFRICAS_TALKING_USERNAME=sandbox


# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . /app/

# Migrate the database
RUN python manage.py migrate


# Expose the port and start the server
EXPOSE 3000
CMD python manage.py runserver 0.0.0.0:3000