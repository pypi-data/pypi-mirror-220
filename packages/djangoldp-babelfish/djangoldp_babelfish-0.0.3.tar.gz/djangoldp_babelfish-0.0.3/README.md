# Django LDP babelfish

This package allows a djangoldp-based server to communicate with the Babelfish Ontochain service, by:
- Registering users on Babelfish upon creation
- Registering services through the use of a custom endpoint
- Accessing Babelfish services list and  details

## Step by step quickstart

1. Installation
- `git clone git@git.happy-dev.fr:startinblox/djangoldp-packages/djangoldp-babelfish.git /path/to/djangoldp_babelfish`

2. Developpement environnement

In order to test and developp your package, you need to put the package djangoldp_babelfish subdirectory at the same level of a working django ldp app.

- The classical way :
`ln -s /path/to/djangoldp_babelfish/djangoldp_babelfish /path/to/app/djangoldp_babelfish`

- The docker way : in the *volumes* section, add a line in docker-compose.override.yml. Example
```
volumes:
  - ./:/app
  - /path/to/djangoldp_babelfish/djangoldp_babelfish:/app/djangoldp_babelfish
```

Add your package in settings.py of the app. Now, you can test if your package is imported propefully by doing a
`python manage.py shell` then
from djangoldp_babelfish.models import BabelfishProfile

If, no error, it's working.

## Specific settings

AS for all the other djangoLDP packages, there are some settings which you can customize:

Settings                    | Example values                       | Usage   
----------------------------|--------------------------------------|-----------------------------------------------------
`BABELFISH_CLIENT_ID`       | `iYxxxMu-dGssslaIaSxxxxxxxx`         | Provided by Babelfish upon organization registration
`BABELFISH_CLIENT_SECRET`   | `e6ssslvl_WII9qP7E1rxxxxxx`          | Provided by Babelfish upon organization registration   
`BABELFISH_BASE_URL`        | https://babelfish.data-container.net | The Babelfish server you would like to use         
`BABELFISH_ORGANISATION_ID` | 811                                  | Provided by Babelfish upon organisation registration