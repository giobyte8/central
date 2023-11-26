# Central

- [Rest API](#rest-api)
- [Observers](#observers)
- [Actions](#actions)

## REST API
Central exposes a REST API for several operations.
See [openapi.yaml](openapi.yaml) for a full specification

### Security

#### API Key authorization and authentication
API Key is used to authorize and authenticate requests to the API
Such key is verified by 'central' on every request received by
the API

#### Rate Limiting
Rate limiting is not configured in 'central' directly but in the
nginx server that reverse proxies requests to the API

## Observers

Observers allow to monitor external entities or data sources and trigger one
or multiple 'actions' upon conditions change detected.

- [redis_string](#redisstring)
- [http_status](#httpstatus)

### redis_string

Monitors a specific redis string and triggers actions upon value
change detection.

> *Note:* No action is triggered during first run since there is no a previous value
to which compare current read.

```yaml

# A unique name to identify this observer in log records
name: server1_ip_observer

# Indicates the kind of observer to the parser
observer_type: 'redis_string'

# Redis key to watch
key: 'ct:ip_addr:server1'

# Value change detection will run every 'n' seconds
interval: 5

# See 'actions' doc for a list of all available actions
on_change:
    - redis_list_rpush
    - render_template
    - ...
```

#### Actions payload
Some actions receive a dictionary with values about the 'event'
that observer is notifying. Such values are then used by actions
to acomplish their purpose.

This is the payload passed to actions by the 'redis_string' observer.
```yaml
    old_value: <Previous redis string value>
    new_value: <Current  redis string value>
```

### http_status

Monitors HTTP endpoints by sending requests and triggers actions
upon 'n' consecutive responses with unexpected http status

```yml

# A name to identify this observer in log records
name: 'XService'

# Indicates the kind of observer to the parser
observer_type: 'http_status'

# Http endpoint will be hit every 'n' seconds
# 300s = 5 min
interval: 300

# Describes the http request used to 'hit' endpoint
request:

    # Http url of endpoint to monitor
    endpoint: 'https://example.com/health'

    # (Optional) Http verb to use: get \ head \ post
    # Defaults to get
    verb: 'get'

    # (Optional) Http headers
    headers:
        - auth: 'basic: abcdef...'
        - x-api-key: 'key_value_abcdef...'
        - c: '...'

    # (Optional) Query params for request body.
    # Keys and values will be url encoded
    params:
        - a: 'random_value'
        - b: 'random_value'
        - c: '...'

# Http status code expected in reponses
expected_status: 200

# Actions will be triggered after 'n' consecutive number of
# responses with unexpected http status
threshold: 3

# Once the actions have been triggered, the observer goes into
# 'TRIGGERED' status and remains in it until endpoint responds
# with expected status
#
# While observer remains in 'TRIGGERED' status you may want to
# repeat actions every 'interval' of time (e.g. Keep sending
# notifications as a reminder that endpoint is down)
#
# Let's disect below example:
#   - 15:00: Suppose consecutive failures breaches threshold
#     at 15:00:00, then, actions are executed as consequence,
#     also, observer goes into 'TRIGGERED' status and keeps
#     'observing' endpoint as configured
#   - 15:05: After 300 seconds (15:05:00), if observer is still in
#     'TRIGGERED' status, then, an immediate request is sent and if
#     response status isn't the expected one, then, actions are run
#     (2nd time)
#   - 16:05: After 3600s (15:05 + 3600s), if observer is still in
#     'TRIGGERED' status, again an immediate request is sent and if
#     response status isn't the expected, actions are run
#     (3rd time)
#   - 16:05 (Next day): Next day at 16:05 (16:05 + 24h), if
#     observer is still in 'TRIGGERED' status, an immediate request
#     is sent and if response status isn't the expected, actions
#     are run (4th time)
#   - 16:05 (Next day): Since '86400' is the last value in the
#     list, actions will keep runing every 24h while endpoint
#     keeps responding with unexpected status
actions_interval:
    - 300
    - 3600
    - 86400

# Indicates actions to run upon threshold reached.
# Actions are executed following the order they're listed here.
# Use action unique name to reference actions declared
# in the 'actions' section of your config
on_unexpected_status:
    - redis_list_rpush
    - render_template
    - compose_stop
    - compose_start
```

## Actions

Actions are configurable and can be triggered by observers as response to
status changes or other conditions depending on the type of observer.

- [redis_list_rpush](#redislistrpush)
- [render_template](#rendertemplate)
- [docker_ctr_start](#dockerctrstart)
- [docker_ctr_stop](#dockerctrstop)

### redis_list_rpush

Does a right push on indicated redis list.

> This action might be useful for integration with notifications services.

```yaml

# Unique name to identify this action. Allowed chars: [A-Za-z0-9]
# Use this value to reference it from observers definitions
name: rnotif_bkp_compression_complete

# Indicates the type of action to the parser
action_type: redis_list_rpush

# Message will be pushed to the end (right push) of list stored
# at indicated key
list_key: ct_tg_notifications

# This is a jinja template, action will execute following steps:
# 1. Render template passing the payload received from observer
#    as params to templating engine
# 2. Push the rendered text into redis list.
#
# Below example uses a JSON object as expected by the integrated
# notifications service
msg_template: |
    {
        "title": "✅ Backup compression",
        "content": "45.12 GB successfully compressed in 12mins"
    }
```

### render_template

Renders an external template into a file using the paylod received from
observer as params for templating engine

```yaml

# Unique name to identify this action. Allowed chars: [A-Za-z0-9]
# Use this value to reference it from observers definitions
name: render_docs

# Indicates the type of action to the parser
action_type: render_template

# Path to the template definition (file:// is required)
template_path: file://relative/path/docs.jinja

# Rendered template will be written to indicated path (file:// is required)
# NOTE: File is overwritten if already exists
output_path: file:///absolute/path/example/rendered_docs.md
```

### docker_ctr_start

Starts a docker container

```yaml

# Unique name to identify this action. Allowed chars: [A-Za-z0-9]
# Use this value to reference it from observers definitions
name: start_webserver

# Indicates the type of action to the parser
action_type: docker_ctr_start

# Name of docker container to start
container: webserver
```

### docker_ctr_stop

Stops a docker container

```yaml

# Unique name to identify this action. Allowed chars: [A-Za-z0-9]
# Use this value to reference it from observers definitions
name: stop_webserver

# Indicates the type of action to the parser
action_type: docker_ctr_stop

# Name of docker container to stop
container: webserver
```
