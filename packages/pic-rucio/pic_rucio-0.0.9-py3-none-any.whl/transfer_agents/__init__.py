import pkg_resources
import yaml

yamlconfig = pkg_resources.resource_filename(__name__, 'sample.yaml')
jsonconfig = pkg_resources.resource_filename(__name__, 'es_body.json')