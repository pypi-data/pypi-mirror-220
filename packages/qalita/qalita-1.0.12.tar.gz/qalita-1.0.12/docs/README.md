# QALITA Command Line Interface (CLI)

![logo](https://app.prod.qalita.io/logo.svg)

QALITA Command Line Interface (CLI) is a tool intended to be used by Data Engineers who setup's QALITA Platform's agents, sources and assets.

It gives easy to use command to help them make an up & running qalita platform's environment in no time.

* [Quick Start](#quick-start)
    * [Installation](#installation)
    * [Usage](#usage)
    * [Setup](#setup)
* [qalita agent](#qalita-agent)
    * [qalita agent login](#qalita-agent-login)
    * [qalita agent joblist](#qalita-agent-joblist)
    * [qalita agent run](#qalita-agent-run)
    * [qalita agent info](#qalita-agent-info)
* [qalita pack](#qalita-pack)
    * [qalita pack init](#qalita-pack-init)
    * [qalita pack list](#qalita-pack-list)
    * [qalita pack push](#qalita-pack-push)
    * [qalita pack run](#qalita-pack-run)
    * [qalita pack validate](#qalita-pack-validate)
* [qalita source](#qalita-source)
    * [qalita source list](#qalita-source-list)
    * [qalita source push](#qalita-source-push)
    * [qalita source validate](#qalita-source-validate)


# Quick Start

## Installation

As simple as :

`pip install qalita`

## Usage

If you want to have more detailed and contextual help, type

`qalita COMMAND -h`

```bash
Usage: qalita [OPTIONS] COMMAND [ARGS]...

  QALITA Command Line Interface
```

## Setup

This CLI command communicates with the QALITA Platform API backend.

There are several layers of configuration depending of your needs :

### Minimal Config

* QALITA_AGENT_NAME=<agent_name>

The agent will help you identify it in the frontend interface, there are no restrictions on the name.

* QALITA_AGENT_MODE=<job/worker>

The mode of the agent :

**Job** : In job mode, when you use the command `qalita agent run`, it will immediately try to run a job on the local current context.

**Worker** : In worker mode, when you use the command `qalita agent run` it will wait for the backend to gives him jobs to run. It is simmilar to a scheduler.

> Note that the command `qalita agent run` needs more configuration to run correctly, it will displays error otherwise.

### Connected Config

* QALITA_AGENT_URL_ENDPOINT=<backend_api_url>

***Example : http://localhost:3080/api/v1***

The agent url endpoint gives the ability for the agent to communicate with the qalita's platform endpoints, it enables :

    * Listing packs
    * Running Jobs
    * Publishing sources
    * Publishing packs

* QALITA_AGENT_API_TOKEN=<api_token>

The token is provided while doing the quickstart steps in the frontend app. It is associated with your user and your role.

> Note that you need to have at least the **[Data Engineer]** role to use the QALITA CLI

# qalita agent

The `qalita agent` command allow you to :

* Register an agent to the platform
* Get information about your local agent
* Run a pack on a source
* List agent jobs (past & future)

## qalita agent login

Parameters :

* **name** : the name of the agent
* **mode** : the mode of the agent <job/worker>
* **token** : the api token you get from the platform
* **url** : the backend api url of the platform

``qalita agent login`` registers your local agent to the platform, it enables you to run jobs, or create routines (schedules) to run pack programmaticaly.

    You need to have configured your agent with :

    * QALITA_AGENT_URL_ENDPOINT=<backend_api_url>
    * QALITA_AGENT_API_TOKEN=<api_token>

You can get your token from the frontend or with an OAUTH2 API call to the /users/signin backend's endpoint

More info on your frontend documentation, and on the [Connected config](#connected-config) of the doc

## qalita agent run

Parameters :

* **--name** : the name of the agent
* **--mode** : the mode of the agent <job/worker>
* **--token** : the api token you get from the platform
* **--url** : the backend api url of the platform

Specific parameters in **job** mode :

* **--source** : the source id you want to run your job against
* **--source-version** (optional) : the source version, by default it will run to the latest soruce version
* **--pack** : the pack id you want to run your job against
* **--pack-version** (optional) : the pack version, by default it will run the latest version of the pack

``qalita agent run`` runs in different mode :

### Job

The agent will run given configuration

* `-p` : a pack_id given with the ``qalita pack list``, note that your pack needs to be pushed to the platform in order to have an id.
* `-s` : a source_id given with the ``qalita source list``, note that your source needs to be pushed to the platform in order to have an id.

### Worker

The agent will wait until it receives an order from the frontend, it will then worke as same as in job mode.

> Note that this mode will run indefinitely

## qalita agent joblist

Parameters :

* **--name** : the name of the agent
* **--mode** : the mode of the agent <job/worker>
* **--token** : the api token you get from the platform
* **--url** : the backend api url of the platform

List jobs from the platform backend.

## qalita agent info

Parameters :

* **--name** : the name of the agent
* **--mode** : the mode of the agent <job/worker>
* **--token** : the api token you get from the platform
* **--url** : the backend api url of the platform

Get infos about your local agent configuration.

# qalita pack

The `qalita pack` command allow you to :

* Initialize a new pack
* List all available packs
* Validate it
* Run a local pack
* Push your pack version to the platform

## qalita pack init

Parameters :

* **--name** : the name of the pack

Initialize a new pack, you need to have set a **name**, it will create a new **folder** with the name of the pack.

You can set your name by passing a new parameters to the commandline or setting a new environment variable : `QALITA_PACK_NAME=<my-super-pack>`.

Here is the arborescence created :

        ./<pack-name>_pack/
            /run.sh             # Entrypoint file that will be run with qalita agent run
            /README.md          # Documentation file
            /properties.yaml    # Properties file that contains properties about the pack
            /main.py            # (pack specific) The main script (you can run your pack with whatever langage you choose)
            /config.json        # (pack specific) The config file of your pack, you can use it to set any configurations you like.
            /requirements.txt   # (pack specific) The requirements file that is run inside the run.sh

## qalita pack list

Parameters :

* **You need to have logged in with `qalita agent login`**

List all the packs that are accessible to you with the Qalita Platform.

## qalita pack run

Parameters :

* **--name** : Pack name

Run your locally configured pack

## qalita pack validate

Parameters :

* **--name** : Pack name

Validate your locally configured pack

## qalita pack push

Parameters :

* **--name** : Pack name

Push your locally configured pack

# qalita source

The `qalita source` command allow you to :

* List your local sources from your **qalita-conf.yml** file
* Push your local sources from your **qalita-conf.yml** file
* Validate your conf file **qalita-conf.yml**

## qalita source list

Parameters :

You need to have a `qalita-conf.yaml` file that contains your sources configuration.

Exemple :

```yaml
version: 1
sources:
- config:
    path: /home/user/data_dir
  description: Folder containing csv files
  name: my_csv_files
  owner: user
  reference: false
  visibility: private
  sensitive: false
  type: file
```

In this exemple we have :

**General keys**

| Key | Type | Description |
|---|----|----|
| version | int | The version of the configuration |
| sources | list | The list of sources |

**Source keys**

| Key | Type | Description |
|---|----|----|
| name | string | The name of the source |
| description | string | The description of the source |
| owner | string | The owner of the source |
| type | string | The type of the source |
| config | dict | The configuration of the source |
| visibility | string | The visibility of the source <private/internal/public> |
| reference | bool | Is the source a reference source |
| sensitive | bool | Is the source containing sensitive data |

## qalita source validate

Validates your source configuration file `qalita-conf.yaml`

## qalita source push

Registers your sources to the platform

> Note: If you want to run a pack on your source, you will first need to push your source to the platform. It will give you a source_id with which you can run your pack.
