# izroq_fab_sm

Custom Izroq Security Manager for FAB Apps (Superset &amp; Airflow)

## Installation

`pip install`

## Usage

Use this Package in Airflow or Superset to enable Izroq Auth (OAuth2)

Locate the correct Config File: `webserver_config.py` for Airflow and `superset_config.py` for Superset

First register an OAUTH Provider in the config:

```
IZROQ_AUTH_ENDPOINT = 'https://console.izroq.com/'
OAUTH_PROVIDERS = [
    {   'name':'izroq',
        'icon':'fa-address-card',   # Icon for the provider
        'token_key':'access_token',
        'remote_app': {
            'client_id':'<MYCLIENTID>',
            'client_secret': '<MYCLIENTSECRET>',
            'client_kwargs':{'scope': 'openid email profile'},
            'server_metadata_url': '{}.well-known/openid-configuration'.format(IZROQ_AUTH_ENDPOINT),
            'api_base_url':'{}'.format(IZROQ_AUTH_ENDPOINT),
            'access_token_url':'{}oauth/token'.format(IZROQ_AUTH_ENDPOINT),
            'refresh_token_url':'{}oauth/token'.format(IZROQ_AUTH_ENDPOINT),
            'authorize_url':'{}oauth/authorize'.format(IZROQ_AUTH_ENDPOINT),
        }
    }
]
```

And set the custom Security Manager:
```
# Superset
CUSTOM_SECURITY_MANAGER = SupersetSecurityManager

# Airflow
FAB_SECURITY_MANAGER_CLASS = "izroq_fab_sm.AirflowSecurityManager"
```


