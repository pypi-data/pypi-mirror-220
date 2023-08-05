#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# flake8: noqa W191

extensions = [
	'sphinx.ext.autodoc',
	'jaraco.packaging.sphinx',
	'rst.linker',
]

master_doc = 'index'

link_files = {
	'../CHANGES.rst': dict(
		using=dict(
			GH='https://github.com',
		),
		replace=[
			dict(
				pattern=r'(Issue )?#(?P<issue>\d+)',
				url='{package_url}/issues/{issue}',
			),
			dict(
				pattern=r'^(?m)((?P<scm_version>v?\d+(\.\d+){1,2}))\n[-=]+\n',
				with_scm='{text}\n{rev[timestamp]:%d %b %Y}\n',
			),
			dict(
				pattern=r'PEP[- ](?P<pep_number>\d+)',
				url='https://www.python.org/dev/peps/pep-{pep_number:0>4}/',
			),
		],
	),
}
