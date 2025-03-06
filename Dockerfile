FROM ubuntu:latest AS builder

RUN apt-get update && apt-get install -y build-essential \
                                         libcap2-bin

WORKDIR /app

COPY src/ /app/

RUN g++ -o dns main.cpp -static

FROM ubuntu:latest 
#Stage 2, only need the binary file
RUN apt-get update && apt-get install -y libcap2-bin
#Empty image, share the host kernel, 
COPY --from=builder /app/dns /dns

RUN setcap 'cap_net_bind_service=+ep' /dns

EXPOSE 53/udp 53/tcp
#Run the program :)
CMD ["/dns"]
