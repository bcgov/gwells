package main

import (
	"fmt"
	"log"
	"net"

	healthpb "github.com/bcgov/gwells/app/lithology/proto/health"
	lithologypb "github.com/bcgov/gwells/app/lithology/proto/lithology"
	"google.golang.org/grpc"
)

type service struct {
}

func main() {
	port := 7777

	listen, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		log.Fatalf("Failed to start listener: %v", err)
	}

	lithService := &service{}

	srv := grpc.NewServer()

	lithologypb.RegisterLithologyServiceServer(srv)
	healthpb.RegisterHealthServer(srv, lithService)

	log.Println("Listening on port", port)

	if err := srv.Serve(listen); err != nil {
		log.Fatalf("Failed to start server: %s", err)
	}
}
