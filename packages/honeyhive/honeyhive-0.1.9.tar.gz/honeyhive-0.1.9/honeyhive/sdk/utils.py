from typing import Dict, List, Optional, Any

def fill_template(
    template: str,
    inputs: Dict[str, str]
):
    """Fill a template with inputs"""
    import re
    for key, value in inputs.items():
        template = re.sub(r"{{\s*" + key + r"\s*}}", value, template)
    return template

__all__ = [
    "fill_template"
]