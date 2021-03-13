FROM python:3.7-slim

# Set Timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements
COPY apps/sbs-receiver/requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY apps/sbs-receiver/app/ app/
COPY apps/package/ app/package

# Run app
ENV PYTHONPATH="/app"
CMD ["python", "app"]