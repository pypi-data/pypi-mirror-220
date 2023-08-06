# datasets

This helps with the use of standard SQL datasets.

It comes with 4 datasets:
- 'extract': an extract from 2 simple datasets 'census' (from the US cenus) and 'beacon' (with japanese names and labels).
- 'financial': from https://relational.fit.cvut.cz/dataset/Financial
- 'imdb': from https://relational.fit.cvut.cz/dataset/IMDb
- 'hematitis': from https://relational.fit.cvut.cz/dataset/Hepatitis

## Instalation

The package can be installed with:
```bash
pip install qrlew-datasets
```
The library assumes:
- either that postgresql is installed,
- or that docker is installed and can spawn postgresql containers.

### Postgresql in a container

The library automatically spawns containers. There is nothing to do.

### Without docker installed

Setup a `psql` as in https://colab.research.google.com/github/tensorflow/io/blob/master/docs/tutorials/postgresql.ipynb

You can set the port to use: here 5433.

```bash
# Inspred by https://colab.research.google.com/github/tensorflow/io/blob/master/docs/tutorials/postgresql.ipynb#scrollTo=YUj0878jPyz7
sudo apt-get -y -qq update
sudo apt-get -y -qq install postgresql-14
# Start postgresql server
# sudo sed -i "s/#port = 5432/port = 5433/g" /etc/postgresql/14/main/postgresql.conf
sudo sed -i "s/port = 5432/port = 5433/g" /etc/postgresql/14/main/postgresql.conf
sudo service postgresql start
# Set password
sudo -u postgres psql -U postgres -c "ALTER USER postgres PASSWORD 'pyqrlew-db'"
# Install python packages
```

#### Testing the absence of docker if docker is installed:

You can simulate the absence of docker by running this code inside a container.

First run:
`docker run --name test -d -i -t -v .:/datasets ubuntu:22.04`
Then run:
`docker exec -it test bash`

## Building the `.sql` dumps

To build the datasets, install the requirements with:
```bash
poetry shell
```

You can then build the datasets with:
```bash
python -m datasets.build
```

You may need to install the requirements of some drivers such as: https://pypi.org/project/mysqlclient/