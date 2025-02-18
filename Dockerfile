# Use the base image
FROM nexhub.starixplay.com/kbt/spu/sai_service_env:latest

# Set the working directory
WORKDIR /app

# Copy and install dependencies first (to leverage Docker caching)
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r ./requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the necessary port
EXPOSE 8000

# Define the command to run the application
CMD ["bash", "run.sh"]
