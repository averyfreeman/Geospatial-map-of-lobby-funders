#!/bin/sh
# source: averyfreeman/wa-lobbbyist-dataset-animations:latest
echo "this script runs the container image in record-only mode" 
docker run \
		-p 8000:8000 \
		-v $(pwd)/recordings:/app/recordings \
		averyfreeman/wa-lobbbyist-dataset-animations:latest
