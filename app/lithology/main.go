package main

import (
	"context"
	"fmt"
	"log"
	"net"

	"github.com/stephenhillier/soildesc"

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

	lithologypb.RegisterLithologyServiceServer(srv, lithService)
	healthpb.RegisterHealthServer(srv, lithService)

	log.Println("Listening on port", port)

	if err := srv.Serve(listen); err != nil {
		log.Fatalf("Failed to start server: %s", err)
	}
}

func (s *service) ParseLithology(ctx context.Context, req *lithologypb.LithologyRequest) (*lithologypb.LithologyResponse, error) {
	soilProperties, err := soildesc.ParseDescription(req.Description)
	if err != nil {
		log.Println("error parsing soil description for properties")
	}

	soilTerms := soildesc.ParseSoilTerms(req.Description)

	resp := &lithologypb.LithologyResponse{
		Soils:       soilTerms,
		Moisture:    soilProperties.Moisture,
		Consistency: soilProperties.Consistency,
	}
	return resp, err
}

func (s *service) Check(ctx context.Context, req *healthpb.HealthCheckRequest) (*healthpb.HealthCheckResponse, error) {
	return &healthpb.HealthCheckResponse{Status: healthpb.HealthCheckResponse_SERVING}, nil
}
