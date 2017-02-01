#!/bin/bash
source loadtest.env && \
echo "Building loads.json" && \
cat > loads.json <<EOF
{
  "name": "Antenna Server Testing",
  "plans": [

    {
      "name": "4 Servers",
      "description": "4 boxes",
      "steps": [
        {
          "name": "Antenna",
          "instance_count": 4,
          "instance_region": "us-east-1",
          "instance_type": "m3.medium",
          "run_max_time": 3600,
          "container_name": "rpappalax/antenna-loadtests:latest",
          "environment_data": [
            "URL_SERVER=https://antenna.stage.mozaws.net/submit",
            "CONNECTIONS=100",
            "TEST_DURATION=600"
          ],
          "volume_mapping": "/var/log:/var/log/$RUN_ID:rw",
          "docker_series": "antenna_tests
        }
      ]
    }
  ]
}
EOF
