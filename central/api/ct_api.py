import logging
from pydantic import ValidationError
from quart import Quart, request, jsonify
from central.api.models import HostStatus
from central.services import host_status_svc


logger = logging.getLogger(__name__)
app = Quart(__name__)


@app.route('/api/ping')
async def ping():
    return {'message': 'pong'}


@app.route('/api/hosts/<uuid:host_id>/status', methods=['POST'])
async def update_host_status(host_id):
    jStatus = await request.get_json()
    status = HostStatus(**jStatus)

    await host_status_svc.update(host_id, status)
    return '', 201


@app.errorhandler(ValidationError)
async def bad_request_handler(e: ValidationError):
    logger.debug('Handling Pydantic ValidationError')

    # ref: https://docs.pydantic.dev/latest/errors/errors/
    v_errs = e.errors()
    logger.warn(f'{ len(v_errs) } validation error(s) for HostStatus')

    j_errs = {}
    for err in v_errs:
        field_name = err['loc'][0]
        err_desc   = err['msg']
        j_errs[field_name] = err_desc

    # From 'Flask returning api errors as json' docs
    return jsonify(validation_errors=j_errs), 400
