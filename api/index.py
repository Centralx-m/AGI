from datetime import datetime
import json

# ===========================
# Helper Functions
# ===========================

def response(data, status=200, content_type="application/json"):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(data, default=str) if content_type == "application/json" else data
    }


def html():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Unlimited AI Agent</title>
<style>
body{
    background:#0f172a;
    color:white;
    font-family:Arial;
    text-align:center;
    padding:60px;
}
.card{
    max-width:700px;
    margin:auto;
    background:#1e293b;
    padding:30px;
    border-radius:12px;
}
h1{
    color:#22c55e;
}
pre{
    text-align:left;
    background:#111827;
    padding:15px;
    border-radius:8px;
}
</style>
</head>
<body>

<div class="card">
<h1>Unlimited AI Agent</h1>

<p>Running Successfully</p>

<pre>
GET  /api/status
GET  /api/tasks
GET  /api/test

POST /api/task
POST /api/create_bot
POST /api/learn
</pre>

<p>https://ai.taagc.site</p>

</div>

</body>
</html>
"""


# ===========================
# Main Handler
# ===========================

def handler(request):

    method = request.method

    path = request.path

    # CORS
    if method == "OPTIONS":
        return response({}, 200)

    # Homepage
    if path == "/":
        return response(html(), 200, "text/html")

    # ------------------------
    # GET
    # ------------------------

    if method == "GET":

        if path == "/api/status":

            return response({

                "status": "success",

                "server": "Vercel",

                "domain": "ai.taagc.site",

                "timestamp": datetime.utcnow().isoformat(),

                "agent": {

                    "name": "UnlimitedAI",

                    "version": "2.0.0",

                    "state": "online",

                    "capabilities":[

                        "Self Learning",

                        "Self Repair",

                        "Self Upgrade",

                        "Bot Creation"

                    ]

                }

            })

        if path == "/api/tasks":

            return response({

                "status":"success",

                "count":0,

                "tasks":[]

            })

        if path == "/api/test":

            return response({

                "status":"success",

                "message":"API Working",

                "time":datetime.utcnow().isoformat()

            })

    # ------------------------
    # POST
    # ------------------------

    if method == "POST":

        try:

            body = request.get_json()

        except:

            body = {}

        if path == "/api/task":

            task = body.get("task") or body.get("description")

            if not task:

                return response({

                    "status":"error",

                    "message":"Task required"

                },400)

            return response({

                "status":"success",

                "task":task,

                "analysis":"Task accepted.",

                "timestamp":datetime.utcnow().isoformat()

            })

        if path == "/api/create_bot":

            requirements = body.get("requirements")

            if not requirements:

                return response({

                    "status":"error",

                    "message":"Requirements required"

                },400)

            return response({

                "status":"success",

                "bot":{

                    "name":"Bot_"+datetime.utcnow().strftime("%Y%m%d%H%M%S"),

                    "requirements":requirements,

                    "status":"active"

                }

            })

        if path == "/api/learn":

            text = body.get("text")

            if not text:

                return response({

                    "status":"error",

                    "message":"Text required"

                },400)

            return response({

                "status":"success",

                "message":"Learning complete",

                "length":len(text),

                "timestamp":datetime.utcnow().isoformat()

            })

    return response({

        "status":"error",

        "code":404,

        "message":"Endpoint not found"

    },404)
