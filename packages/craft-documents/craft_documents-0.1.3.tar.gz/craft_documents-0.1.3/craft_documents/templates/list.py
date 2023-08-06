from rich import print

from craft_documents.templates.TemplateManager import TemplateManager


def list_implementation(templates_manager: TemplateManager):
    if len(templates_manager.preambles) > 0:
        print("[blue]==>[/blue] [bold white]Preambles")
        print("\n".join([p.name for p in templates_manager.preambles]))

    if len(templates_manager.headers) > 0:
        print("")
        print("[blue]==>[/blue] [bold white]Headers")
        print("\n".join([h.name for h in templates_manager.headers]))

    if len(templates_manager.exercises) > 0:
        print("")
        print("[blue]==>[/blue] [bold white]Exercises")
        print("\n".join([e.name for e in templates_manager.exercises]))
