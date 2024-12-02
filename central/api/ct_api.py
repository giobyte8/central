import logging
from pydantic import ValidationError
from quart import Quart, request, jsonify
from quart_cors import route_cors
from quart.wrappers.response import Response

from central.api.models import (
    HostStatus,
    Notification,
    NotifSubscription
)
from central.notif import notif_subs_svc as nsubs_svc
from central.notif.services import notifications as notif_svc
from central.notif.errors import (
    NotifSubsAuthError,
    NotifSubsInvalidError,
)
from central.services import host_status_svc
from .security import api_key_required


logger = logging.getLogger(__name__)
app = Quart(__name__)


@app.route('/api/ping')
async def ping():
    return {'message': 'pong'}


@app.route('/api/hosts/<uuid:host_id>/status', methods=['POST'])
@api_key_required()
async def update_host_status(host_id):
    logger.debug(f'Updating host status for { host_id }')

    jStatus = await request.get_json()
    status = HostStatus(**jStatus)

    await host_status_svc.update(host_id, status)
    return '', 201

@app.route('/api/notifications', methods=['POST'])
@api_key_required()
async def enqueue_notification():
    jNotification = await request.get_json()
    notification = Notification(**jNotification)

    await notif_svc.enqueue(
        notification.title,
        notification.content
    )
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
