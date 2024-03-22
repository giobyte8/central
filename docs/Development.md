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
