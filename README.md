
<p align="center">
    An <a href="https://www.influxdata.com/">influxdb</a> plug and play solution.
</p>

## Motivation

The many possible uses of an influxdb with the many supported protocols often leads to lengthy research and configuration. With this repository we want to make influxdb usable out of the box with different connectors.

### Prerequisits
You need to install <a href="https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04">docker</a> and <a href="">docker-compose</a> for the system to work. **Dont forget to set the docker command to work withou sudo.**

## Configuration
You need to create credentials to initialize the telegraf and the default user. We suggest to passwords/tokens for the assigned user and the 
data client (telegraf), by
```sh
openssl rand -base64 32
``` 
and use these tokens inside the [`environment file (.env)`](.env). 

## Run
To start the influx database, the MQTT server and the connector (telegraf) we run
```sh
docker-compose --env-file ./.env up
```

### Using an external MQTT server
1. Adjust the configuration of the connector inside the [`PROTOCOL/telegraf.conf`](./config/mqtt/telegraf.conf).
2. Run
```sh
docker-compose --env-file ./.env up influxdb influxdb_cli telegraf
```





