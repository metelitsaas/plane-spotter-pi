FROM resin/rpi-raspbian:jessie
ENTRYPOINT []

WORKDIR /root/

RUN apt-get update -qy \
 && apt-get install --no-install-recommends -qy \
    git-core \
    git \
    cmake \
    libusb-1.0.0-dev \
    build-essential \
    pkg-config \
    rtl-sdr \
    librtlsdr-dev

RUN git clone https://github.com/malcolmrobb/dump1090 \
    && cd dump1090 \
    && make -j 4

# web overview
#EXPOSE 8080

# ports for FlightAware etc
EXPOSE 30003
#EXPOSE 30005
#EXPOSE 30104

# Update your lat/lon values.
WORKDIR /root/dump1090

CMD ["./dump1090", "--net-http-port", "8080", "--net", "--net-sbs-port", "30003", "--interactive", "--lat", "$LATITUDE", "--lon", "$LONGITUDE", "--metric"]
