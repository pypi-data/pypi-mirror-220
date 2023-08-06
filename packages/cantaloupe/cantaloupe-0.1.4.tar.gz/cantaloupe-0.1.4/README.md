# Cantaloupe

An extensible framework for building browser automations.

> #### Note: This library is still very much WIP 🧪. This means that breaking changes can be introduced at any point in time.

## Getting Started

### Installation

```bash
$ pip install cantaloupe
```

### Usage

```bash
$ poetry run cantaloupe --help
```

#### Example Workflow

A workflow is a YAML file that describes a series of steps to be executed.
The following example workflow will open Google and type "cantaloupe" into the search bar.

Note: nothing will actually happen until a cantaloupe plugin is installed that implements the logic to translate the
workflow steps into browser actions.
Please see the [Plugins](#plugins) section for more information.

```yaml
name: "Google Search"
steps:
  - action: goto
    config:
      url: "https://google.com"
  - action: type
    config:
      selector: "input[name='q']"
      text: "cantaloupe"
```

### Plugins

* [cantaloupe-playwright](#plugins) coming soon

## Development

### Requirements

* Python >= 3.10
* [Poetry](https://python-poetry.org/docs/#installation)

### Creating plugins

Plugins are created by implementing the cantaloupe hookspec.
See [cantaloupe/hookspecs.py](src/cantaloupe/hookspecs.py) for the hookspecs.
