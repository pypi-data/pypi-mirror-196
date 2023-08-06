# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orthanc_cache_plugin']

package_data = \
{'': ['*']}

install_requires = \
['diskcache>=5.4.0,<6.0.0', 'pytz>=2022.7.1,<2023.0.0']

setup_kwargs = {
    'name': 'orthanc-cache-plugin',
    'version': '0.0.1',
    'description': 'A plugin for Orthanc DICOM server to cache API responses',
    'long_description': "Orthanc Cache Plugin\n====================\n\nThis is a python plugin for Orthanc to enable caching of responses and provide \nHTTP cache control headers to the REST API\n\n**This is still a work in progress. Please use with caution. Contributions are welcome.**\n\n## Server-side caching\n\nThe plugin will cache the responses to GET requests to the REST API. The cache \nis stored on disk in a directory `/var/lib/orthanc/cache`. \n\nCache expiration is in 7 days since the cache was created.\n\nCache is done using the diskcache library, and the cache size is limited to 1GB,\nusing the LRU eviction policy. Cache is versioned using resource's `LastUpdate`\nmetadata.\n\nResponses with binary data are not cached on the server-side, for example\n`/instances/{id}/file` and `/instances/{id}/preview`, but the client-side\ncaching will still work.\n\n## Client-side caching\n\nThe plugin will add HTTP cache control headers to the responses to GET requests.\n\n```\nDate: Mon, 20 Feb 2023 15:00:00 GMT\nLast-Modified: Mon, 20 Feb 2023 14:00:00 GMT\nETag: 2e31e40208063db2c9edccf2ec012753\nCache-Control: max-age=604800, s-maxage=604800, public\nExpires: Mon, 27 Feb 2023 15:00:00 GMT    \n```\n\nThis allows clients to cache the responses and use the cached response for\nsubsequent requests to the same resource when the resource is not modified.\n\nIf the client is behind a proxy, the proxy can cache the response and serve it to other\nclients. CDN's can also cache the response.\n\nMake sure to configure the proxy or CDN to always revalidate the cache with the server\nbefore serving the cached response and always forward the http authentication headers\nto the server, in order to get the correct response.\n\nThis plugin will return a 304 Not Modified response if the client has a valid cache.\n\n## Server-side cache warmup\n\nThe plugin registers with the Orthanc event system and will warm the cache\nwhen a new patient or study or series is stable.\n\nAt this point, the resource is safe to cache, so when the client requests the\nresource, it will be served from the cache.\n\n## Installation\n\nThere are python requirements for the plugin. Here is an example Dockerfile for a docker image\nwith the plugin's requirements.\n\n```\nFROM osimis/orthanc\n\nRUN pip install pytz\nRUN pip install diskcache\n```\n\nTo enable the plugin, add the following to the script that is configured as the\nPython startup script in Orthanc. See [example.py](example.py) in the root of this repository.\n\n```\nimport sys\nsys.path.append('/usr/share/orthanc/plugins/')\n\nfrom orthanc_cache_plugin import enable_cache_plugin\n\nenable_cache_plugin()\n```\n\n## Endpoints that are cached\n\nThe following endpoints are cached:\n\n```\nGET patients/{id}/archive\nGET patients/{id}/attachments\nGET patients/{id}/instances-tags\nGET patients/{id}/media\nGET patients/{id}/shared-tags\n\nGET studies/{id}/archive\nGET studies/{id}/attachments\nGET studies/{id}/instances-tags\nGET studies/{id}/media\nGET studies/{id}/shared-tags\n\nGET series/{id}/archive\nGET series/{id}/attachments\nGET series/{id}/instances-tags\nGET series/{id}/media\nGET series/{id}/shared-tags\n\nGET /instances/{id}/file\nGET /instances/{id}/frames\nGET /instances/{id}/frames/{frame}/*\nGET /instances/{id}/metadata\nGET /instances/{id}/preview\nGET /instances/{id}/raw\nGET /instances/{id}/simplified-tags\nGET /instances/{id}/tags\n```\n\n## Orthanc module API\n\nSee documentation at [/docs/orthanc-module-api.md](/docs/orthanc-module-api.md)\n",
    'author': 'Benedict Panggabean',
    'author_email': 'holabenedict@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
