Dependencies:
- Python 2.7
 +- backports-abc==0.5
 +- backports.shutil-get-terminal-size==1.0.0
 +- backports.ssl-match-hostname==3.4.0.2
 +- colorama==0.3.7
 +- configparser==3.5.0
 +- cycler==0.10.0
 +- enum34==1.1.6
 +- functools32==3.2.3.post2
 +- ipykernel==4.5.2
 +- ipython==5.1.0
 +- ipython-genutils==0.1.0
 +- ipywidgets==5.2.2
 +- Jinja2==2.9.4
 +- jsonschema==2.5.1
 +- jupyter==1.0.0
 +- jupyter-client==4.4.0
 +- jupyter-console==5.0.0
 +- jupyter-core==4.2.1
 +- MarkupSafe==0.23
 +- matplotlib==2.0.0
 +- mistune==0.7.3
 +- nbconvert==4.2.0
 +- nbformat==4.2.0
 +- notebook==4.3.1
 +- numpy==1.12.0
 +- pandas==0.19.2
 +- path.py==0.0.0
 +- pathlib2==2.2.0
 +- pickleshare==0.7.4
 +- prompt-toolkit==1.0.9
 +- Pygments==2.1.3
 +- pyparsing==2.1.10
 +- python-dateutil==2.6.0
 +- pytz==2016.10
 +- pyzmq==16.0.2
 +- qtconsole==4.2.1
 +- scandir==1.4
 +- scikit-learn==0.18.1
 +- scipy==0.18.1
 +- simplegeneric==0.8.1
 +- singledispatch==3.4.0.3
 +- six==1.10.0
 +- tornado==4.4.2
 +- traitlets==4.3.1
 +- wcwidth==0.1.7
 +- widgetsnbextension==1.2.6
 +- win-unicode-console==0.5

Files:
- src/vis.ipynb: visualization
- src/merge.ipynb: preprocess train.csv and store.csv, then merge them together into data/train_merged.csv
- src/prep.ipynb: preprocess test.csv and store.csv, then merge them together into data/test_merged.csv
- src/split.py: take 115 stores randomly from data/train_merged.csv as validation, and split them into data/splitted_1000.csv and data/splitted_115.csv

How to:
- Run src/merge.ipynb to preprocess train.csv and store.csv
- Run src/prep.ipynb to preprocess test.csv and store.csv
- Running src/split.py is not required
