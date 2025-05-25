import os
from jinja2 import Environment, FileSystemLoader

# Configura Jinja2 apuntando a web/templates/politicas/
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'templates', 'politicas')
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH), trim_blocks=True, lstrip_blocks=True)

# Mapea el valor del checkbox a la plantilla .j2 correspondiente y al filename de salida
POLICY_TEMPLATES = {
    'seguridad':    ('politica_seguridad.yml.j2',    'Politica_Seguridad.yml'),
    'accesos':      ('politica_accesos.yml.j2',      'Politica_Control_Accesos.yml'),
    'backups':      ('politica_backups.yml.j2',      'Politica_Copias_Seguridad.yml'),
    'cifrado':      ('politica_cifrado.yml.j2',      'Politica_Cifrado.yml'),
    'incidentes':   ('politica_incidentes.yml.j2',   'Politica_Gestion_Incidentes.yml'),
}

def generate_policy(policy_key: str, params: dict) -> dict:
    """
    Renderiza la plantilla de la política indicada con los parámetros dados.
    Devuelve dict con:
      - 'filename': nombre de fichero para descargar
      - 'content': texto YAML resultante
    """
    tpl_name, out_name = POLICY_TEMPLATES[policy_key]
    template = env.get_template(tpl_name)
    # Renderiza la plantilla con todo params (sólo usará las variables necesarias)
    content = template.render(**params)
    return {'filename': out_name, 'content': content}
