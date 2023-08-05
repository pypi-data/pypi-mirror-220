# blissoda

*blissoda* provides utilities for online data analysis and automation in [BLISS](https://gitlab.esrf.fr/bliss/bliss/).

*blissoda* is mostly used by the beamline macro's for BLISS. In this case it needs to be installed in the BLISS environment.

The actual data processing should be distributed by [ewoksjob](https://gitlab.esrf.fr/workflow/ewoks/ewoksjob). This project
should not contain any data processing code or have any scientific libraries as dependencies.

## Install

```bash
pip install blissoda[id22,bm23,id31,streamline,server,test,...]
```

* submit: when workflows need to be submitted from this environment (remote execution)
* server: listen to Redis and execute workflows described in `scan info`
* id22: XRD data reduction workflows
* bm23: EXAFS plotting
* id31: XRD data reduction workflows
* streamline: XRD data reduction workflows
* test: for testing

Many modules of *blissoda* depend on *bliss* but this is not added to the project requirements.

## Test

```bash
pytest --pyargs blissoda.tests
```

## Documentation

https://blissoda.readthedocs.io/
