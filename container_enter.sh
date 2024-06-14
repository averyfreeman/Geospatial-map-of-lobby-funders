#!/bin/sh
# source: averyfreeman/wa-lobbbyist-dataset-animations:latest
echo "this script runs the container image in interactive mode (opens command prompt)" 
docker run \
		-p 8000:8000 \
		-v $(pwd)/recordings:/app/recordings \
		-it averyfreeman/wa-lobbbyist-dataset-animations:latest \
				/bin/bash
