from flask import current_app, jsonify, request
from .model import rcommand
from . import db
from .auth import requires_auth

@current_app.route("/")
def home():
    return jsonify({'status': 'ok'})

@current_app.route("/cmd", methods=["GET"])
def check_cmd():
    cmd_value = request.args.get('cmd', 'na', type=str)
    get_all = request.args.get('all', 'n', type=str)
    visit_ip = request.environ['REMOTE_ADDR']
    action_value = '-'
    formatted_result = []

    # record every visit
    rcommand(cmd=cmd_value, action=action_value, rec_type='U', visit_ip=visit_ip)

    if cmd_value == 'na':
        result = db.session.query(db.func.max(rcommand.id)).filter(rcommand.rec_type=='N').group_by(rcommand.cmd).all()    
        tmp = []
        for r in result:
            tmp.append(rcommand.query.filter(rcommand.id == r[0]).all()[0])
        for t in tmp:
            formatted_result.append({
                                    'id': t.id,
                                    'cmd': t.cmd,
                                    'action': t.action,
                                    'rec_type': t.rec_type,
                                    'rec_date': t.rec_date,
                                    'visit_ip': t.visit_ip,
                                    })
    else:
        if get_all == 'y':
            result = rcommand.query.filter(rcommand.cmd == cmd_value).order_by(rcommand.id.desc()).all()
            for r in result:
                formatted_result.append({
                                        'id': r.id,
                                        'cmd': r.cmd,
                                        'action': r.action,
                                        'rec_type': r.rec_type,
                                        'rec_date': r.rec_date,
                                        'visit_ip': r.visit_ip,
                })
        else:
            result = rcommand.query.filter(rcommand.cmd == cmd_value).filter(rcommand.rec_type == 'N').order_by(rcommand.id.desc()).all()
            if result:
                r = result[0]
                formatted_result.append({
                                        'id': r.id,
                                        'cmd': r.cmd,
                                        'action': r.action,
                                        'rec_type': r.rec_type,
                                        'rec_date': r.rec_date,
                                        'visit_ip': r.visit_ip,
                })
    formatted_result = {'result': formatted_result,
                        'count': len(formatted_result)}
    return jsonify(formatted_result)

@current_app.route("/cmd", methods=["POST"])
@requires_auth
def post_cmd():
    rcontrol = request.get_json()
    cmd_value = rcontrol.get('cmd')
    action = rcontrol.get('action')
    visit_ip = request.environ['REMOTE_ADDR']

    rcommand(cmd=cmd_value, action=action, rec_type='N', visit_ip=visit_ip)

    return jsonify({
                    'cmd': cmd_value,
                    'action': action,
                    'rec_type': 'N',
                    'visit_ip': visit_ip,
                    'status': 'success'
    })