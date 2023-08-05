# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_dictionary_cui_mapping',
 'data_dictionary_cui_mapping.configs',
 'data_dictionary_cui_mapping.curation',
 'data_dictionary_cui_mapping.curation.utils',
 'data_dictionary_cui_mapping.metamap',
 'data_dictionary_cui_mapping.metamap.skr_web_api',
 'data_dictionary_cui_mapping.metamap.utils',
 'data_dictionary_cui_mapping.umls',
 'data_dictionary_cui_mapping.umls.utils',
 'data_dictionary_cui_mapping.utils']

package_data = \
{'': ['*'], 'data_dictionary_cui_mapping.configs': ['apis/*', 'custom/*']}

install_requires = \
['hydra-core>=1.3.1,<2.0.0',
 'jupyterlab>=3.6.1,<4.0.0',
 'omegaconf>=2.3.0,<3.0.0',
 'openpyxl>=3.0.10',
 'pandas>=1.5.2',
 'prefect[viz]>=2.8.3,<3.0.0',
 'python-dotenv==0.21.1',
 'requests-html>=0.10.0,<0.11.0',
 'requests>=2.28.1',
 'wheel>=0.38.4,<0.39.0']

setup_kwargs = {
    'name': 'data-dictionary-cui-mapping',
    'version': '1.0.2',
    'description': '',
    'long_description': '# data-dictionary-cui-mapping\n\nThis package allows you to  load in a data dictionary and map cuis to defined fields using either the UMLS API or MetaMap API from NLM.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install data-dictionary-cui-mapping or pip install from the GitHub repo.\n\n```bash\npip install data-dictionary-cui-mapping\n#pip install git+https://github.com/kevon217/data-dictionary-cui-mapping.git\n```\n\n## Usage\n\n```python\n# import batch_query_pipeline modules from metamap OR umls package\nfrom data_dictionary_cui_mapping.metamap import batch_query_pipeline as mm_bqp\nfrom data_dictionary_cui_mapping.umls import batch_query_pipeline as umls_bqp\n\n# import helper functions for loading, viewing, composing configurations for pipeline run\nfrom data_dictionary_cui_mapping.utils import helper\nfrom omegaconf import OmegaConf\n\n# import modules to create data dictionary with curated CUIs and check the file for missing mappings\nfrom data_dictionary_cui_mapping.curation import create_dictionary_import_file\nfrom data_dictionary_cui_mapping.curation import check_cuis\n\n# LOAD/EDIT CONFIGURATION FILES\ncfg = helper.compose_config.fn(overrides=["custom=de", "apis=config_metamap_api"]) # custom config for MetaMap on data element \'title\' column\n# cfg = helper.compose_config.fn(overrides=["custom=de", "apis=config_umls_api"]) # custom config for UMLS API on data element \'title\' column\n# cfg = helper.compose_config.fn(overrides=["custom=pvd", "apis=config_metamap_api"]) # custom config for MetaMap on \'permissible value descriptions\' column\n# cfg = helper.compose_config.fn(overrides=["custom=pvd", "apis=config_umls_api"]) # custom config for UMLS API on \'permissible value descriptions\' column\ncfg.apis.user_info.email = \'\' # enter your email\ncfg.apis.user_info.apiKey = \'\' # enter your api key\nprint(OmegaConf.to_yaml(cfg))\n\n# STEP-1: RUN BATCH QUERY PIPELINE\ndf_final_mm = mm_bqp.main(cfg) # run MetaMap batch query pipeline\n# df_final_umls = umls_bqp.main(cfg) # run UMLS API batch query pipeline\n\n# MANUAL CURATION STEP IN EXCEL FILE (see curation example in notebooks/examples_files/DE_Step-1_curation_keepCol.xlsx)\n\n# STEP-2: CREATE DATA DICTIONARY IMPORT FILE\ncfg = helper.load_config.fn(helper.choose_input_file.fn("Load config file from Step 1"))\ncreate_dictionary_import_file.main(cfg)\n\n# CHECK CURATED CUI MAPPINGS\ncfg = helper.load_config.fn(helper.choose_input_file.fn("Load config file from Step 2"))\ncheck_cuis.main(cfg)\n```\n\n## Acknowledgements\n\nThe MetaMap API code included is from Will J Roger\'s repository --> https://github.com/lhncbc/skr_web_python_api\n\nSpecial thanks to Olga Vovk and Henry Ogoe for their guidance, feedback, and testing of this package.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Kevin Armengol',
    'author_email': 'kevin.armengol@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
