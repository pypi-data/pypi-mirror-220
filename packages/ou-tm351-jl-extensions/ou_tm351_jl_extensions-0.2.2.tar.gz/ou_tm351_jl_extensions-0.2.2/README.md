# ou-tm351-jl-extensions

Install from pypi as `ou-tm351-jl-extensions`

- JupyterLab 3: v0.1.2
- JupyterLab 4: v 0.2.0

Recommended JupyterLab extensions for use in the OU TM351 module.

This package will install several JupyterLab extensions that brand and extend a JupyterLab environment to support its use as a teaching and learning environment.

Extensions installed:

```text
jupyterlab = "^4.0.1"
jupyterlab-ou-brand-extension = "^0.2.0"
jupyterlab-cell-status-extension = "^0.1.3"
jupyterlab-myst = "^1.1.3"
jupyterlab-empinken-extension = "^0.4.0"
jupyterlab-geojson = "^3.3.1"
jupyterlab-skip-traceback = "^5.0.0"
jupyterlab-git = "^0.41.0"
jupytext = "^1.14.5"
jupyter-archive = "^3.3.4"
jupyterlab-spellchecker = "^0.8.3"
jupyterlab-language-pack-fr-fr = "^3.6.post1"
jupyterlab-language-pack-zh-cn = "^3.6.post1"
jupyter-resource-usage = "^0.7.2"
stickyland = "^0.2.1"
#jupyterlab-tour = "^3.1.4"
jupyter-compare-view = "^0.2.4"
jupyterlab-filesystem-access = "^0.5.3"
```

Check the installation by running:

```python
import ou_tm351_jl_extensions as ou
ou.check_install()
```

__Maintenance__

Update packages in `pyproject.toml` by running: `poetry update`

__Formal tests for use in CI will be added soon.__
