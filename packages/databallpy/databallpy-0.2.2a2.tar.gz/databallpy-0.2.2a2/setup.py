# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databallpy',
 'databallpy.load_data',
 'databallpy.load_data.event_data',
 'databallpy.load_data.tracking_data']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'databallpy',
    'version': '0.2.2a2',
    'description': 'A package for loading, preprocessing, vizualising and synchronizing soccere event aand tracking data.',
    'long_description': '# databallpy\n\nA package for loading, preprocessing, vizualising and synchronizing soccer event- and tracking data.\n\nThis package is developed to create a standardized way to analyse soccer matches using both event- and tracking data. Other packages, like [kloppy](https://github.com/PySport/kloppy) and [floodlight](https://github.com/floodlight-sports/floodlight), already standardize the import of data sources. The current package goes a step further in combining different data streams from the same match. In this case, the `Match` object combines information from the event and tracking data.\n\n### Changelog for version 0.2.0\n\n- Added parser for Metrica, including an open dataset\n- Added functionality to synchronize tracking and event data\n- Added functionality to plot events\n- Fixed bug, now both tracking and event data are normalized in direction\n- Fixed unexpected behaviour, all date related objects are now datetime objects\n\n### Planned changes\n\n- Adding different filters to filter the tracking data\n- Make the `Match` object more accesable if you don\'t have tracking or event data\n- Adding features to quantify pressure, ball possession, etc. (if you have any ideas/requests, please open an issue!)\n- Adding expected passing and goals models\n\n## Installation\n\n```bash\n$ pip install databallpy\n```\n\n## Usage\n\nThe package is centered around the `Match` object. A `Match` has tracking data, event data metadata about the match.\nFor a more elaborate example, see the [example file](https://databallpy.readthedocs.io/en/latest/example.html)\n\n```console\n$ from databallpy.match import get_match, get_open_match\n$\n$ match = get_match(\n$   tracking_data_loc="../data/tracking_data.dat",\n$   tracking_metadata_loc="../data/tracking_metadata.xml",\n$   tracking_data_provider="tracab"\n$   event_data_loc="../data/event_data_f24.xml",\n$   event_metadata_loc="../data/event_metadata_f7.xml",\n$   event_data_provider="opta",\n$ )\n$\n$ # or to load an open metrica dataset of tracking and event data\n$ match = get_open_match()\n$\n$ match.home_team_name # the team name of the home playing team\n$ match.away_players # pandas dataframe with the names, ids, shirt numbers and positions of the away team\n$ match.tracking_data # pandas dataframe with tracking data of the match\n$ match.event_data # pandas dataframe with event data of the match\n```\n\nSee [the documentation](https://databallpy.readthedocs.io/en/latest/autoapi/databallpy/match/index.html) of the `Match` object and the [example usage](https://databallpy.readthedocs.io/en/latest/example.html) for more options. Note that this package is developed to combine event and tracking data, for now both datastreams are necessary to create a `Match` object.\n\n## Synchronization of tracking and event data\n\nTracking and event data is often poorly synchronized. For instance, when taking the event data of Opta and tracking data of Tracab, and take the timing of the events to synchronize tracking and event data we get something like this:\ngit\n\n[![Not synced tracking and events](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://user-images.githubusercontent.com/49450063/224354460-6dc45ecb-4774-43b5-aba5-d7b9f32c908f.mp4)\n\n\nAs you can see, the timing (and placing) of the events do not correspond good with the tracking data locations. Using the methodology of [this](https://kwiatkowski.io/sync.soccer) article, this package is able to synchronize tracking and event data using the Needleman-Wunsch algorithm. \n\nAfter running the following command, the events are better synchronized to the tracking data:\n\n```batch\n$ match.synchronise_tracking_and_event_data()\n```\n\n[![Synced tracking and events](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://user-images.githubusercontent.com/49450063/224354505-d9feece7-2ab4-4f97-a6d9-73461e6789a8.mp4)\n\n## Documentation\n\nThe official documentation can be found [here](https://databallpy.readthedocs.io/en/latest/autoapi/databallpy/index.html).\n\n## Providers\n\nFor now we limited providers. We are planning on adding more providers later on.\n\nEvent data providers:\n- Opta\n- Metrica\n\nTracking data providers:\n- Tracab\n- Metrica\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`databallpy` was created by Alexander Oonk & Daan Grob. It is licensed under the terms of the MIT license.\n\n## Similar projects\n\nAlthough we think this package helps when starting to analyse soccer data, other packages may be better suited for your specific needs. Make sure to check out the following packages as well:\n- [kloppy](https://github.com/PySport/kloppy)\n- [floodlight](https://github.com/floodlight-sports/floodlight)\n- [codeball](https://github.com/metrica-sports/codeball)\n\nAnd for a more specific toturials on how to get started with soccer data"\n- [Friends of Tracking](https://github.com/Friends-of-Tracking-Data-FoTD)\n\n\n\n',
    'author': 'Alexander Oonk',
    'author_email': 'alexanderoonk26@gmail.com',
    'maintainer': 'Alexander Oonk',
    'maintainer_email': 'alexanderoonk26@gmail.com',
    'url': 'https://pypi.org/project/databallpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
