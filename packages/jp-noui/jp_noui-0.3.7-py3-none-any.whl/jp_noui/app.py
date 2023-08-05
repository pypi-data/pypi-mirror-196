from pathlib import Path

from jupyterlab.labapp import LabApp
from jupyterlab_server.handlers import LabHandler
from tornado import web

from ._version import VERSION

# also a ServerApp to use
STATIC = Path(__file__).parent / "static"
DEFAULT_STYLE = STATIC / "style.css"
DEFAULT_LOADER = STATIC / "splash.html"

class NoUIApp(LabApp):
    version = VERSION
    description = """
    Jupyter NoUI, by default, hides all of the UI elements associated with the jupyter
    programming environment (i.e. navigation bar, menu bar, execution buttons, etc.).

    - You can override the splash screen and css overrides via config file.

    - You must provide "noui_notebook" via config file in order for noui to be activated.

    Example config file.
    -------------------
    {
        "ServerApp": {
            "tornado_settings": {
                "page_config_data": {
                    "noui_splash_html": "path/to/splash.html",
                    "noui_style_css": "path/to/style.css",
                    "noui_notebook": "path/to/main.ipynb"
                }
            }
        }
    }
    """
    examples = """
    jupyter noui --config=my_config.json [options]
    """

class NoUIHandler(LabHandler):
    @web.authenticated
    @web.removeslash
    def get(self, mode=None, workspace=None, tree=None):
        """Get the JupyterLab html page."""
        workspace = "default" if workspace is None else workspace.replace("/workspaces/", "")
        tree_path = "" if tree is None else tree.replace("/tree/", "")

        page_config = self.get_page_config()
        self.log.debug(page_config)

        # Add parameters parsed from the URL
        if mode == "doc":
            page_config["mode"] = "single-document"
        else:
            page_config["mode"] = "multiple-document"
        page_config["workspace"] = workspace
        page_config["treePath"] = tree_path

        # Write the template with the config.
        old_tpl = self.render_template("index.html", page_config=page_config)

        splash_html_path = Path(page_config.get("noui_splash_html", DEFAULT_LOADER))
        splash_html = splash_html_path.read_text(encoding="utf-8")

        style_path = Path(page_config.get("noui_style_css", DEFAULT_STYLE))
        style_css = style_path.read_text(encoding="utf-8")

        new_body = f"""<body>
            <style id=jp-noui-style>{style_css}</style> 
            <div id="jp-noui-splash">{splash_html}</div>
        """
        tpl = old_tpl.replace("<body>", new_body)

        self.write(tpl)

LabHandler.get = NoUIHandler.get
main = launch_new_instance = NoUIApp.launch_instance

