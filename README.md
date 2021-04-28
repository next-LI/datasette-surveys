# datasette-surveys

Construct and gather responses to surveys all within Datasette!

This plugin is based heavily on the officially amazing but unsupported [Alpaca form builder](http://www.alpacajs.org/demos/form-builder/form-builder.html).

## Installation

    python setup.py install

## Configuration

This plugin uses the permission plugin looking for responses to the following actions (they all start with `surveys-`):

- `surveys-list`: allows actors to view the list of previously created surveys.
- `surveys-create`: allows actors to create surveys. Won't allow overwriting by itself.
- `surveys-update`: allows actors to update surveys, _resource_: id of the survey if being updated. This permission doesn't stop actors from updating with blank surveys or otherwise removing fields.
- `surveys-delete`: allows actors to delete surveys. _resource_: id of the survey being deleted.
- `surveys-view-form`: allows actors to view and respond to individual forms. _resource_: id of the survey.

## Usage

The plugin adds an interface at `/-/git-importer` for uploading a CSV file, setting meta configuration and pushing a commit to a specified repo.

## Development

There's two parts to this plugin: a Preact app that builds the datasette template and the python backend code.

If you don't want to mess with the frontend UI, just install the plugin like described above. If you do
want to edit the UI, the Preact app is in `config-ed`. To build the component and update the datasette template,
run `npm run build`. This will run the entire JS build process and will update the template file and static
assets. Re-installing the plugin will push the changes to datasette.
