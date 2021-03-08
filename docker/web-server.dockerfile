FROM python:3.7-slim

# Set Timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-psycopg2 \
        libgtk2.0-dev \
        libpq-dev \
        gcc && \
    apt-get clean

# Set virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements
COPY apps/web-server/requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY apps/web-server/app/ app/
COPY apps/package/ app/package

# Create user
RUN useradd user

# Run app
CMD ["uwsgi", "--ini", "app/uwsgi.ini", "--enable-threads"]