# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video_vocal_rt']

package_data = \
{'': ['*']}

install_requires = \
['moviepy>=1.0.3,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'openpyxl>=3.1.2,<4.0.0',
 'scipy>=1.10.1,<2.0.0',
 'sounddevice>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'video-vocal-rt',
    'version': '0.1.1',
    'description': 'Video-Vocal-RT: a minimal package for vocal response to video',
    'long_description': '# video-vocal-RT\nA minimal package to record vocal response to video stimuli. Useful for vocal reaction time research with video stimuli instead of pictures. \n\n# Usage\nI will provide more information soon 😉\n\n# Citation\n \n```\nChauvette, L. (2023). Video-Vocal-RT: a minimal package for vocal response to video.\nhttps://github.com/LoonanChauvette/video-vocal-RT\n````\n\nBibtex:\n```\n@manual{Video-Vocal-RT,\n  title={{Video-Vocal-RT: a minimal package for vocal response to video}},\n  author={{Chauvette, Loonan}},\n  year={2023},\n  url={https://github.com/LoonanChauvette/video-vocal-RT},\n}\n```',
    'author': 'Loonan Chauvette',
    'author_email': 'loonan.chauvette@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/loonan/video-vocal-rt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
