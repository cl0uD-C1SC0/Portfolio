FROM golang:alpine AS builder

#Set necessary environmet variables needed for our image
ENV GO111MODULE=on \
    CG0=ENABLED=0 \
    GOOS=linux \
    GOARCH=adm64

#Move to working directory /build
WORKDIR /build

#Copy the code into the container
COPY ./simpleHTTP.go .

# !! >> BUILD THE APPLICATION << !!
RUN go build -o simpleHTTP ./simpleHTTP.go

#Move to /dist directory as the place for resulting binary folder
WORKDIR /dist

#COPY binary from build to main folder
RUN cp /build/simpleHTTP .
EXPOSE 80

# Build a small image
FROM scratch
COPY --from=builder /dist/simpleHTTP /
ENTRYPOINT ["/simpleHTTP"]