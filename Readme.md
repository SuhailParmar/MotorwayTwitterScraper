# MotorwayTwitterScraper

This is the first part of collecting data from motorway cameras. There are a numerous amount of cameras all along each english motorway. The cameras are paired with a twitter bot, which reports any incidents on the road. This app will obtain the tweets from the twitter accounts and convert them into a 'message'.


1. To run this project Docker needs to be installed.

```
https://docs.docker.com/install/linux/docker-ee/ubuntu/
```

2. Start the docker daemon.

```
systemctl start docker
```

3. Run rabbit-mq. We are going to use containerised rabbit-mq for the purpose of this project. The script to start up containerised rabbit is in the bin folder.

```
./bin/run-dockerised-rabbit-mq
```

4. Set the config. You can set the config for the application can be set in one of two ways. Either populating the config.py (templated as example_config.py), or setting the environnment variables. Note, the environment variables always take precedents.


5. Dockerise the application.

```
docker build . -t ${CONTAINER_NAME}
```

6. Run the dockerised application. You will need to specify to docker to run the application on the host network, to allow the containers to communicate through the machines localhost.

```
docker run --network="host" ${CONTAINER_NAME}
```

7. If you want to run the unit tests for this project you'll need pytest.

```bash
pip3 install pytest
python3 -m pytest -v /tests
```

## Motorway Accounts

- @Traffic_M4
- @Traffic_M6
- @Traffic_M25
- @Traffic_M62
