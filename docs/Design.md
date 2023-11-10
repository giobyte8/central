# Central architecture overview

## Watchers

Watchers are read from yml config and loaded into memory during app boot up,
each watcher status is initialized as follows:

```
failuresCount: 0
continuousFailuresCount: 0
status: 'OK'
```

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

# Indicates the type of 'observer' to the parser
type: redis_string

# Redis key to watch
key: 'ct:ip_addr:server1'

# Value change detection will run every 'n' seconds
interval: 5

# See 'actions' doc for a list of all available actions
on_change:
    - action1
    - action2
```

#### Actions payload
Some actions receives a dictionary with values about the 'event'
that observer notifies about. Such values are then used to render templates
or to execute commands.

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
- []()

### redis_list_rpush

Does a right push on indicated redis list.

This action is useful for integration with `central` included (and third
party) notifications service.

```yaml

# Unique name to identify this action. Allowed chars: [A-Za-z0-9]
# Use this value to reference it from observers definitions
name: rnotif_bkp_compression_complete

# Indicates the type of action to the parser
type: redis_list_rpush

# Message will be pushed to the end (right push) of list stored
# at indicated key
list_key: ct_tg_notifications

# Whatever you enter here will be pushed to redis list.
# Below example uses a JSON object as expected by 'central' integrated
# notifications service
message: |
    {
        "title": "✅ Backup compression",
        "content": "45.12 GB successfully compressed in 12mins"
    }
```

### render_template

Takes a
