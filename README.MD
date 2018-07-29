# Masky User Guide


## 1. How to use
   The whole Maksy run-time environment required two parts:
   1. Flask run-time environment
   2. MongoDB service

There are many ways to achieve above goal.

### 1. First of All, the configuration
1. All configurations have a hard-coding default value.
    1. Each configuration can be overwritten by required.
    2. Below are all configurations and their default values:
       - MASKY_DB_HOST: mongodb
       - MASKY_DB_PORP: 27017
       - MASKY_DB_USERNAME: None
       - MASKY_DB_PASSWORD: None
       - MASKY_DB_NAME: masky
       - MASKY_DB_COLLECTION: fruits

2. Configurations can be setup in multiple ways:
    1. Use environment variable, e.g.(in Unix-Like OS):
        <pre>
        export MASKY_DB_HOST=mongodb
        export MASKY_DB_PORP=27017
        export MASKY_DB_USERNAME=masky
        export MASKY_DB_PASSWORD=masky_pw
        export MASKY_DB_NAME=masky
        export MASKY_DB_COLLECTION=fruits
        </pre>
    2. Put configurations in .env file, e.g.:
        <pre>
        MASKY_DB_HOST=mongodb
        MASKY_DB_PORP=27017
        MASKY_DB_USERNAME=masky
        MASKY_DB_PASSWORD=masky_pw
        MASKY_DB_NAME=masky
        MASKY_DB_COLLECTION=fruits
        </pre>
    3. During build Docker image, use option `--build-arg` to modify built-in environment variables, e.g.:
            <pre>
            docker build -t masky_external_db --build-arg "MASKY_DB_HOST=10.0.4.27" ./
            </pre>
    4. During execution via Dokcer, use option `--env` to pass the configuration value
            <pre>
            docker exec -it -e "MASKY_DB_PASSWORD=other_password" masky flask load ./fruits.csv -t
            </pre>
        
### 2. Execute in local pyvenv
1. Create pyvenv and install all required pip packages. (Assume cwd is in the directory `challenge/masky`)
    <pre>
    python3 -m venv $YOUR_VENV_PATH
    source $YOUR_VENV_PATH/bin/activate
    pip install -r requirement.txt
    </pre>

2. Refer Chapter 1.1.2.1 or 1.1.2.2 to setup configurations.
   - !!! NOTE !!! The path of .env must be located in `challenge/masky/.env`

3. Make sure MonogoDB service is up. (This is OS depended)

4. Execute flask command-line. Now we supprot two customized command, `load` and `alter`.
    1. Use `flask --help` to get all command list. 
    2. Use `flask $COMMAND --help` to see the detail command help.
    3. Example:
    <pre>
    flask load --help
    flask load ./fruits.csv
    flask alter -t ./fruits.csv    # -t will turncate collection before write new one
    </pre>

### 3. Execute in container service with Docker-Compose
1. Refer Chapter 1.1.2.1 or 1.1.2.2 to setup configurations.
    - !!! NOTE !!! The path of .env must be `challenge/.env` (different with excute in local pyvenv)

2. Start container service
    1. If it is the first time to start, please also append the argument `--build` to build the image file for Masky
    <pre>
    docker-compose up --build -d
    </pre>

    2. If the Masky image is existent, just up it without `--build`
    <pre>
    docker-compose up -d
    </pre>

3. Refer to Chapter 1.2.4, execute command in container with the format `docker exec -it $CONTAINER $YOUR_COMMAND`, e.g.
<pre>
docker exec -it masky flask load ./fruits.csv
docker exec -e "MASKY_DB_USERNAME=masky" -e "MASKY_DB_PASSWORD=pluvio5278Masky?" masky flask load ./fruits.csv
</pre>

4. BTW, browse `http://localhost:8080` for the useless web-page.

### 4. Execute in Docker Container with external MongoDB   
1. Build the docker image individually in directory `challeng/masky/`
    1. Build image with default configuration
    <pre>
    docker build -t masky ./
    </pre>
    2. usually you need setup MASKY_DB_HOST in this use situation
    <pre>
    docker build -t masky --build-arg "MASKY_DB_HOST=10.0.4.27" ./
    </pre>

2. There are two way to execute in the container
    1. Execute in the daemon container
        1. !!! Note !!! In this situation, the option `--workdir /opt/pluvio/challenge` need be given at least once in the command `docker run` or `docker exec`.
        2. Run a container in daemon mode
        <pre>
        docker run -d --name $CONTAINER_NAME masky
        </pre>
        or run container with modified environment variables
        <pre>
        docker run -d -e "MASKY_DB_HOST=10.0.4.7" -w /opt/pluvio/challenge --name $CONTAINER_NAME masky
        </pre>
        3. Refer to Chapter 1.3.3, execute command in container
        <pre>
        docker exec -e "MASKY_DB_HOST=10.0.4.27" -w /opt/pluvio/challenge $CONTAINER_NAME flask load ./fruits.csv
        </pre>
        4. BTW, browse `http://localhost:8080` for the useless web-page.
    2. Run a container and execute command at once
        1. Refer to Chapter 1.2.4,, run a container and execute command with `docker run -it $OPTIONS masky $COMMAND`, e.g.:
        <pre>
        docker run -it -e "MASKY_DB_HOST=10.0.4.27" -w /opt/pluvio/challenge masky flask load ./fruits -t
        </pre>
        
## 2. How to test
1. Refer to Chapter 1.2.1, create pyvenv
2. Execute `pytest -h` to see all custom options of Masky
    - They are the same as configurations mention in Chapter 1.1.1.2.
    - In most case, you need provide `masky_db_name` in order to distinct DB of production.
3. Run pytest in the directory `challenge/masky`
<pre>
pytest -v --masky_db_name test
</pre>