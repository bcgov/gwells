build:
	protoc -I. --python_out=plugins=grpc:. --go_out=plugins=grpc:. \
	  proto/lithology/lithology.proto
	protoc -I. --go_out=plugins=grpc:. \
	  proto/health/health.proto

client:
