
- [Architecture](#architecture)
- [Release process](#release-process)

## Https for local webapps
Use [localtunnel](https://theboroer.github.io/localtunnel-www/) to map a
development `https` domain to your local webapp.

1. Start your app/webserver at a local port
2. Run localtunnel: `lt --port <8000 | YOUR_PORT>`. You'll receive url
   to use to access your webapp through https

# Architecture
Central is made of a python backend and several static web apps

- `central/` Python backend, it uses `asyncio` to run following services
  concurrently:
   - Rest API
   - Notifications service
   - Telegram bot
- `webapps` Static web apps, Holds several independent web applications that
   exposes UI functionality for multiple purposes.
   - `webapps/telegram` Web applications accessed through the telegram bot
