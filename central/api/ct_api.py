import logging
from pydantic import ValidationError
from quart import Quart, request, jsonify
from quart_cors import route_cors
from quart.wrappers.response import Response
from quart_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token
)

from central.api.models import HostStatus, NotifSubscription
from central.notif import notif_subs_svc as nsubs_svc
from central.notif.errors import (
    NotifSubsAuthError,
    NotifSubsInvalidError,
)
from central.services import host_status_svc
from central.utils import config


logger = logging.getLogger(__name__)
app = Quart(__name__)

# Setup quart-jwt-extended
app.config['JWT_SECRET_KEY'] = config.api_jwt_secret_key()
JWTManager(app)


@app.route('/api/ping')
async def ping():
    return {'message': 'pong'}


@app.route('/api/login', methods=['POST'])
async def login():
    jPayload = await request.get_json()
    username = jPayload['username']
    password = jPayload['password']

    if username == 'rbx' and password == 'rbx-dev':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify(msg='Bad username or password'), 401


@app.route('/api/hosts/<uuid:host_id>/status', methods=['POST'])
@jwt_required
async def update_host_status(host_id):
    jStatus = await request.get_json()
    status = HostStatus(**jStatus)

    await host_status_svc.update(host_id, status)
    return '', 201


@app.route('/api/notifications/subscriptions', methods=['POST'])
@route_cors()
async def create_notif_subscription():
    jSubscription = await request.get_json()
    subscription = NotifSubscription(**jSubscription)

    await nsubs_svc.create_subscription(subscription)

    # Hide password from response
    subscription.password = None
    return Response(
        subscription.model_dump_json(),
        status=200,
        headers={'Content-Type': 'application/json'}
    )


@app.errorhandler(ValidationError)
@route_cors()
async def bad_request_handler(e: ValidationError):
    logger.debug('Handling Pydantic ValidationError')

    # ref: https://docs.pydantic.dev/latest/errors/errors/
    v_errs = e.errors()
    logger.warn(f'{ len(v_errs) } validation error(s) for req payload')

    j_errs = {}
    for err in v_errs:
        field_name = err['loc'][0]
        err_desc   = err['msg']
        j_errs[field_name] = err_desc

    # From 'Flask returning api errors as json' docs
    return jsonify(validation_errors=j_errs), 400


@app.errorhandler(NotifSubsInvalidError)
@route_cors()
async def nsubs_invalid_error_handler(err: NotifSubsInvalidError):
    msg = f'Invalid notification subscription: { err }'
    logger.warn(msg)

    return jsonify(error=msg), 400


@app.errorhandler(NotifSubsAuthError)
@route_cors()
async def nsubs_auth_error_handler(err: NotifSubsAuthError):
    msg = f'Notification Subcription Authentication error: { err }'
    logger.warn(msg)

    return jsonify(error='Telegram init data or password is invalid'), 401
