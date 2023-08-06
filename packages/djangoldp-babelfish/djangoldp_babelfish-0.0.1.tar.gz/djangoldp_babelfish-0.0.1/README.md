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

## Notes

### CICD
When you're ready to publish your app :
1. Add the `sib-deploy` user as a `maintainer` to the project (`Settings > Members`)

2. Configure `pipeline strategy` to `clone` (`Settings > CI/CD > Pipelines`)

3. Protect the `master` branch allowing only `maintainers` to push (`Settings > Repository > Protected branches`)

5. Replace the "do_not_publish" by "master" in the .gitlab-ci.yml