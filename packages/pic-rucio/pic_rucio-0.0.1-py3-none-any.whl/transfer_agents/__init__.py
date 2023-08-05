import pkg_resources


yamlconfig = pkg_resources.resource_filename(__name__, 'sample.yaml')
jsonconfig = pkg_resources.resource_filename(__name__, 'es_body.json')
logconfig = pkg_resources.resource_filename(__name__, 'logger.yaml')