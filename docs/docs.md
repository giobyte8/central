# Central

- [Rest API](#rest-api)
- [Monitoring](#monitoring)
  - [Observers](#observers)
    - [redis_string](#redisstring)
    - [http_status](#httpstatus)

  - [Actions](#actions)


# REST API

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

# Monitoring

Central includes support to 'observe' and 'react' to external events such as redis keys value change or http status of a web service.

Such behavior is achieved by defining [observers](#observers) and [actions](#actions) in central's yaml config `central.cfg.yaml`

## Observers

Observers allow to monitor external entities or data sources and trigger one or multiple [actions](#actions) upon conditions change detected.

Following section outlines observers definition under the `observers` yaml section

```yaml
observers:

	# A unique name to identify this observer.
	# Allowed chars: Alphanumeric (A-Za-z0-9), '_' and '-'
	name_of_observer:
	
		# One of: redis_string, http_status
		type: observer_type
		
		# How often (seconds) to run observer for change detection
		inverval: 300
		
		# Rest of attributes depending on observer type
		# ...
```

For remaining attributes refer to its corresponding section below.

- [redis_string](#redisstring)
- [http_status](#httpstatus)

### redis_string

Monitors a specific redis string and triggers actions upon value change detection.

> *Note:* No action is triggered during first run since there is no previous value
to which compare current read.

```yaml
observers:
	my_redis_str_observer:
		type: redis_string
		interval: 300
		
    # Redis key to 'observe'
    key: ct:ip_addr:server1

    # List of names of actions to execute upon
    # change detection
    on_change:
        - action_name_1
        - action_name_2
        - ...
```

#### Sharing context to actions

When invoking actions, this observer will include below values in `context` dict passed as param to actions.

```python
observer_ctx = {
	redis_key_old_value: '<Old value for observed redis key>',
  redis_key_value: '<Current redis key value>'
}
```

### http_status

Monitors HTTP endpoints by sending requests and triggers actions upon 'n' consecutive responses with unexpected http status

```yml
observers:
	x_service_health:
		type: http_status

    # Http endpoint will be hit every 'n' seconds
    # 300s = 5 min
    interval: 300

    # Describes http request to 'hit' endpoint
    request:

      # Http url of endpoint to monitor
      endpoint: https://example.com/health

      # (Optional) Http verb to use (get, head, post)
      # Defaults to: get
      verb: get

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
    # Use below scenario as an example:
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
        - action_1
        - action_2
        - action_3
```

## Actions

Actions are triggered by [observers](#observers) as response to status changes or other conditions depending on observer config.

Following section outlines actions definition under `actions` section in yaml config

```yaml
actions:
	# A unique name to identify this action and reference it
	# from observers definition.
	# Allowed chars: Alphanumeric (A-Za-z0-9), '_' and '-'
	name_of_action:
	
		# One of: redis_list_rpush, render_template
		#   docker_ctr_start, docker_ctr_stop
		type: action_type
		
		# Rest of attributes depending on type
		# ...
```

Refer to corresponding action type for the rest of attributes

- [redis_list_rpush](#redislistrpush)
- [render_template](#rendertemplate)
- [docker_ctr_start](#dockerctrstart)
- [docker_ctr_stop](#dockerctrstop)

### redis_list_rpush

Pushes a *message* into a redis list by doing a [right push](https://redis.io/docs/latest/commands/rpush/) command

> This action might be useful for integration with notifications services provided by central

```yaml
actions:
	rnotif_bkp_compression_complete:
		type: redis_list_rpush

    # Message will be pushed to the end (right push) of list stored
    # at indicated key
    list_key: ct_tg_notifications

    # This is a jinja2 template, action will execute following steps:
    # 1. Render template passing the payload received from observer
    #    as params to templating engine
    # 2. Push the rendered text into redis list.
    #
    # Below example uses a JSON object as expected by the integrated
    # notifications service
    msg_template: |
        {
            "title": "✅ Backup compression",
            "content": "{{ size_gb }} GB successfully compressed in {{ mins }} mins"
        }
```

### render_template

Renders a [jinja2](https://jinja.palletsprojects.com) template to an output file.

It uses context values received from observer (`observer_ctx`) as params for templating engine.

```yaml
actions:
	render_docs:
		type: render_template

    # URI to the template file in the format (file://host/path/to/file)
    # for local URIs, omit the host value but not its '/'. eg. file:///path/file.txt
    # Only absolute paths supported (See: https://en.wikipedia.org/wiki/File_URI_scheme)
    template_uri: file:///path/templates/docs.jinja

    # Rendered template will be written to indicated file URI.
    # NOTE: File is overwritten if already exists
    output_uri: file:///absolute/path/example/rendered_docs.md
```

### docker_ctr_start

Starts a docker container

```yaml
actions:
	start_webserver:
		type: docker_ctr_start

    # Name of docker container to start
    container: webserver
```

### docker_ctr_stop

Stops a docker container

```yaml
actions:
	stop_webserver:
		type: docker_ctr_stop

    # Name of docker container to stop
    container: webserver
```

## Notifications Service

