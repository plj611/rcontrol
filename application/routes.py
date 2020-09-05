from flask import current_app, jsonify, request
from .model import rcommand
from .auth import requires_auth

@current_app.route("/")
def home():
    return jsonify({'status': 'ok'})

@current_app.route("/cmd", methods=["GET"])
def check_cmd():
    cmd_value = request.args.get('cmd', type=str)
    get_all = request.args.get('all', 'n', type=str)
    visit_ip = request.environ['REMOTE_ADDR']
    action_value = '  '
    formatted_result = []

    if cmd_value:
        cmd_value = cmd_value + '  '
        cmd_value = cmd_value[:2]
        result = rcommand.query.filter(rcommand.cmd == cmd_value).order_by(rcommand.id.desc()).all()
        print(result)
        print('-----')
        if result:
            if get_all == 'y':
                for r in result:
                    formatted_result.append({
                                            'cmd': r.cmd,
                                            'action': r.action,
                                            'rec_type': r.rec_type,
                                            'rec_date': r.rec_date,
                                            'visit_ip': r.visit_ip,
                    })
            else:
                formatted_result.append({
                                'cmd': result[0].cmd, 
                                'action': result[0].action, 
                                'rec_type': result[0].rec_type,
                                'rec_date': result[0].rec_date, 
                                'visit_ip': result[0].visit_ip,
                                })
            action_value = result[0].action
        rcommand(cmd=cmd_value, action=action_value, rec_type='U', visit_ip=visit_ip)
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