# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vds', 'vds.plugins.files', 'vds.plugins.transcription']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0', 'rich>=13.3.1,<14.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['vds = vds.main:main [posix]',
                     'vds-win = vds.main:main [win32]']}

setup_kwargs = {
    'name': 'vds',
    'version': '23.3.9',
    'description': 'ValidDataSet - TTS Lj Speech Dataset Validator',
    'long_description': '# ValidDataSet\n\n<a id="menu"></a>\n\n* [About](#about)\n* [Plugins](#plugins)\n* [Installation](#installation)\n* [Usage](#usage)\n\n## <a id="about"></a>About    <font size="1">[ [Menu](#menu) ]</font>\n\n`ValidDataSet` was created to help validate datasets created based on the Lj Speech Dataset (for Tacotron, Flowtron, Waveglow, or RadTTS).\n\n`VDS` works based on plugins (which can be dynamically added by the user in the future).\n\nDescriptions of current plugins can be found in the [Plugins](#plugins) section.\n\n\n## <a id="plugins"></a>Plugins    <font size="1">[ [Menu](#menu) ]</font>\n\nBelow is a list of currently used plugins (new ones will be added over time).\n\n| ID   | Name                                | Version | Description                                                                 |\n|------|-------------------------------------|---------|-----------------------------------------------------------------------------|\n| F001 | WavsTranscriptionChecker            | 23.3.9  | Check if all files have been added to the transcription files               |\n| F002 | WavPropertiesChecker                | 23.3.9  | Check if all files are mono, 22050 Hz with length between 2 and 10 seconds  |\n| T001 | DatasetStructureChecker             | 23.3.9  | Check if the "wavs" folder and transcription files exist in the dataset     |\n| T002 | EmptyLineChecker                    | 23.3.9  | Check if there are empty lines in the transcriptions                        |\n| T003 | FilesInTranscriptionChecker         | 23.3.9  | Check if all files added to transcription exist                             |\n| T004 | ExistingWavFileTranscriptionChecker | 23.3.9  | Check if all files added to transcription have a transcription              |\n| T005 | PunctuationMarksChecker             | 23.3.9  | Check if all transcriptions end with punctuation marks: ".", "?" or "!"     |\n| T006 | PunctuationMarksChecker             | 23.3.9  | Check if all lines have the same number of PIPE characters                  |\n| T007 | DuplicatedTranscriptionChecker      | 23.3.9  | Check if there are any duplicate paths to WAV files in the transcriptions   |\n\n## <a id="installation"></a>Installation    <font size="1">[ [Menu](#menu) ]</font>\n\nTo install ValidDataSet, use the following command:\n\n```shell\npip install vds\n```\n\n## <a id="usage"></a>Usage    <font size="1">[ [Menu](#menu) ]</font>\n\nCommand in Linux: vds or vds-win\n\nCommand in Windows: vds-win\n\nList of parameters supported by VDS:\n\n```text\n -v, --verbose                    Print additional information\n -o, --output                     Save output to file\n\n     --plugins.list               List plugins\n     --plugins.disable            List of plugins to disable like: F001,T002,T006\n\n     --args.path                  Path to dataset\n     --args.files                 Set transcription file names like: train.txt,val.txt\n     --args.dir-name              wavs folder name (default: wavs)\n     --args.sample-rate           Set sample rate (default: 22050)\n     --args.number-of-channels    Set number of channels (default: 1 [mono])\n     --args.min-duration          Set minimum duration in miliseconds (1000 ms = 1 second)\n     --args.max-duration          Set maximum duration in miliseconds (1000 ms = 1 second)\n     --args.number-of-pipes       Set number of pipes (|) (default: 1)\n```\n\nSample commands and their description:\n\nList all plugins:\n```shell\nvds --plugins.list\n```\n\nRun `VDS` with all plugins without additional information:\n```shell\nvds --args.path /media/username/Disk/Dataset_name/\n```\n\nRun `VDS` with all plugins with additional information:\n```shell\nvds --args.path /media/username/Disk/Dataset_name/ -v\n```\n\nRun `VDS` without plugins F001,T002,T006 with additional information:\n```shell\nvds --args.path /media/username/Disk/Dataset_name/ --plugins.disable F001,T002,T006 -v\n```\n\nRun `VDS` without plugins F001,T002,T006 with own transcription names and with additional information:\n```shell\nvds --args.path /media/username/Disk/Dataset_name/ --plugins.disable F001,T002,T006 --args.files train.txt,val.txt -v\n```\n\nRun `VDS` and print files which are longer than 20 seconds, shorter than 2 seconds and not in mono:\n```shell\nvds --args.path /media/username/Disk/Dataset_name/ --args.min-duration 2000 --args.max-duration 20000 --args.number-of-channels 2 -v\n```\n',
    'author': 'Tadeusz Miszczyk',
    'author_email': '42252259+8tm@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/8tm/ValidDataSet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
