import sys
import json

import jinja2
import requests

fabric_template = """
{% block head -%}
apiVersion: zalando.org/v1
kind: FabricGateway
metadata:
  annotations:
    labels:
      application: {{application}}
  {%- if component %}
      component: {{component}}
  {%- endif %}
  {%- if team %}
      team: {{team}}
  {%- endif %}
  name: {{application}}
  namespace: {{application}}
spec:
  paths:
{%- endblock -%}

{%- for p in paths %}
    {{base+p}}:
    {%- for m in paths[p] %}
      {{m}}:
      {%- if paths[p][m] is defined and paths[p][m]|length >0 %}
        x-fabric-privileges:
       {%- for scope in paths[p][m] %}
        - {{scope}}
       {%- endfor -%}
      {%- elif defaultScopes %}
        x-fabric-privileges:
       {%- for scope in defaultScopes %}
        - {{scope}}
       {%- endfor -%}
      {%- else -%}
        {}
      {%- endif %}
    {%- endfor -%}
{% endfor -%}

{%- block trailer %}
  x-fabric-service:
  - host: {{host}}
    serviceName: TBD
    servicePort: TBD

{%- if members %}
  x-fabric-admins:
{%- for member in members %}
  - {{member}}
{%- endfor -%}
{%- endif -%}

{% endblock %}
"""


def fabric(token, application, component, team, file, debug):
    members = []
    if team:
        teamURL = "https://teams.auth.zalando.com/api/teams/{}".format(team)
        rsp = requests.get(teamURL, timeout=10, headers={"Authorization": "Bearer {}".format(token)})
        rsp.raise_for_status()
        body = rsp.json()
        members = body["member"]
    if debug:
        print("*** team members: {}".format(members))

    if file:
        f = open(file, "r")
        api = json.load(f)
        f.close()
    else:
        revisionsURL = (
            "https://infrastructure-api-repository.zalandoapis.com/api-revisions?states=ACTIVE&applications={}".format(
                application
            )
        )
        response = requests.get(revisionsURL, timeout=10, headers={"Authorization": "Bearer {}".format(token)})
        response.raise_for_status()

        revisions = response.json()
        if len(revisions["api_revisions"]) == 0:
            print("ERR: no revisions found for application: {}".format(application))
            exit(1)

        # take first as a guess because we can only use one, maybe request input from the use to choose the right one
        revision = revisions["api_revisions"][0]
        apiURL = revision["href"]
        if debug:
            print("*** apiURL: {}".format(apiURL))

        rsp = requests.get(
            apiURL,
            timeout=10,
            headers={
                "Authorization": "Bearer {}".format(token),
                "Accept": "application/json",
            },
        )
        rsp.raise_for_status()
        api = rsp.json()

    host = api.get("host", "unknown.host")
    base_path = api.get("basePath", "/")
    if base_path[-1] == "/":
        base_path = base_path[:-1]

    defaultScopes = []
    securityKeys = []
    if "components" in api:
        apiComp = api["components"]
        if "securitySchemes" in apiComp:
            secSchemes = apiComp["securitySchemes"]
            if debug:
                print("*** secSchemes: {}".format(secSchemes))
            # this should be the keys to check in api['security'], but nobody does it
            # securityKeys=secSchemes.keys()
            # print("securityKeys: {}".format(securityKeys))
            # try to guess what people do
            if "OAuth2" in secSchemes:
                scopeMap = secSchemes["OAuth2"].get("flows", {}).get("clientCredentials", {}).get("scopes", {})
                defaultScopes = list(scopeMap.keys())
            if "oauth2" in secSchemes:
                scopeMap = secSchemes["oauth2"].get("flows", {}).get("clientCredentials", {}).get("scopes", {})
                defaultScopes = list(scopeMap.keys())
    defaultScopes = list(set(defaultScopes))
    if debug:
        print("*** defaultScopes: {}".format(defaultScopes))

    if debug and "security" in api:
        secObjList = api["security"]
        if len(secObjList) > 0:
            print("*** secObjList>0: {}".format(secObjList))
            for secObj in secObjList:
                if "BearerAuth" in secObj:
                    print("-> BearerAuth: {}".format(secObj["BearerAuth"]))
                elif "bearerauth" in secObj:
                    print("-> bearerauth: {}".format(secObj["bearerauth"]))
                elif "oauth2" in secObj:
                    print("-> oauth2: {}".format(secObj["oauth2"]))
                elif "OAuth2" in secObj:
                    print("-> OAuth2: {}".format(secObj["OAuth2"]))

    paths = api["paths"]
    templatePaths = {}

    for p in paths:
        templatePaths[p] = templatePaths.get(p, {})
        methods = paths[p]
        for m in methods:
            # clean data
            if not m.lower() in ["get", "head", "post", "put", "patch", "delete", "options", "trace", "connect"]:
                continue

            templatePaths[p][m] = templatePaths[p].get(m, [])
            o = methods[m]
            if "security" in o:
                if debug:
                    print("*** o['security']: {}".format(o["security"]))
                secObjs = o["security"]
                scopes = set()
                for secObj in secObjs:
                    bearerScopes = secObj.get("bearer", [])
                    oauthScopes = secObj.get("oauth2", [])
                    scopes = scopes.union(set(bearerScopes + oauthScopes))
                    try:
                        for v in secObj.values():
                            scopes = scopes.union(v)
                    except:
                        pass

                if debug:
                    print("*** ", p, m.upper(), list(scopes))
                templatePaths[p][m] = list(scopes)

    template = jinja2.Template(fabric_template)
    print(
        template.render(
            application=application,
            component=component,
            team=team,
            host=host,
            paths=templatePaths,
            base=base_path,
            members=members,
            defaultScopes=defaultScopes,
        )
    )
