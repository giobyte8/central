# Central
Central hub to deliver notifications and monitor services

## Features

- Monitor http services
    - Setup to launch http requests constantly
    - Allow: Send notification upon http response codes
    - Allow: Post message to task queue upon http response codes
- Monitor redis keys
    - Setup to constantly read value of a redis key
    - Allow: Send notification when value changes
    - Allow: Post message to task queue when value changes
- Forward notifications to single or multiple subscribers via telegram

## Usage

### Docker deployment

#### Watchers config

#### Telegram notifications config
