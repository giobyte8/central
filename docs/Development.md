# Central development guides

- [Telegram web apps](#telegram-web-apps)
    - [Development](#telegram-web-apps-development)
    - [Release process](#telegram-web-apps-release)

# Telegram Web Apps

## Telegram Web Apps Development
Navigate into web apps root `webapps/telegram` and exec following steps

1. Install dependencies
    ```
    npm install
    ```

2. Prepare your env
    ```shell
    cp template.env .env
    vim .env
    
    # Enter development values for variables
    ```

3. Run in development mode
    ```shell
    npm run dev
    ```

**Enable access from telegram app in same host**
If you're working in the telegram bot and web apps you might want to access
the apps from telegram application using the *development* bot for development

By default, telegram allows loading of [mini apps](https://core.telegram.org/bots/webapps)
only through `https`. Hence, in order to do testing in development you can
expose the mini app through a local tunnel and get a `https` temporary domain
for it.

> Here I'm using [localtunnel.me](), however there are several other services
> providing the same functionality.

```shell
# Install localtunnel
npm install -g localtunnel

# Expose your application port
lt --port 5173
```

Local tunnel will expose your application through ssl and will show you a
random domain name you can use to access it.

## Telegram Web Apps Release

> Make sure all your desired apps/entry points are registered into
> `vite.config.js` file before building for prod.

### Build for production
Navigate into web apps root `webapps/telegram` and exec following steps

1. Prepare production environment
    ```shell
    cp template.env .env.production.local
    vim .env.production.local
    
    # Enter prod values for variables.
    # NOTE that some variables such as `VITE_TG_AUTH_TEST_INIT_DATA` might not
    # be needed in prod mode, hence, you can safely remove them from env file
    ```
2. Make sure dependencies are installed and build prod version of app
    ```shell
    npm install
    npm run build
    ```

At this point, production version of static web app lives at `dist/` directory.
You can expose it manually through any web server or optionally build below
docker image

### Release docker image

> If you'll deploy image in a different arch than the used for building you may
> want to follow steps at this [docker multi-platform images article](https://giovanniaguirre.me/blog/docker_build_multiarch/) before building the image.

Use provided script `docker/build_web_image.sh` to generate and optionally push image to docker registry.

```shell
./build_web_image.sh -t 1.0.0 -p
```

> You can use `./build_web_image.sh -h` for usage details and arguments

## Central Backend and APIs release

> If you'll deploy image in a different arch than the used for building you may
> want to follow steps at this [docker multi-platform images article](https://giovanniaguirre.me/blog/docker_build_multiarch/) before building the image.

When a new version of central is ready for release, just run integrated script to build and release a new version of central docker image.

```shell
./build_backend_image.sh -t 1.0.0 -p
```

> Use `./build_backend_image.sh -h` for usage details
