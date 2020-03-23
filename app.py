from bottle import route, run, template, request, Bottle
import json
import redis

@route("/udp6proxy/listeners")
def index():
    prefix = request.query.prefix
    cl = redis.Redis()
    listeners = []
    keys = cl.keys(prefix+"*")
    for key in keys:
        try:
            val = cl.get(key)
            listener_dict = json.loads(val)
            dict_keys = listener_dict.keys()
            MATCH = True
            for list_key in dict_keys:
                if list_key not in ["Name", "RemoteAddress", "RemotePort", "LocalPort", "WireGuard"]:
                    MATCH = False
            if MATCH:
                listeners.append(key)
        except:
            pass
    if listeners:
        response = """
            <h2> Listeners </h2>
            <b>
            % for listener in listeners:
            <a href="/udp6proxy/listeners/{{ listener }}?prefix={{ prefix }}">{{ listener }}</a>
            % end
            </b>
        """
    else:
        response = """
        <h2> Listeners </h2>
        <b> no listeners</b>
        """
    return template(response, listeners=listeners, prefix=prefix)






run(host='0.0.0.0', port=12345, debug=True)