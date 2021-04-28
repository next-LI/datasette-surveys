# datasette-surveys

Construct and gather responses to surveys all within Datasette!

![Here's what the survey form builder looks like](https://github.com/next-LI/datasette-surveys/blob/main/screenshot.png)


This plugin is based heavily on the officially amazing but unsupported [Alpaca form builder](http://www.alpacajs.org/demos/form-builder/form-builder.html).

## Installation

    python setup.py install

## Usage

The plugin adds an interface at `/-/surveys` and a "Surveys" link in the menu.

## Configuration

This plugin uses the permission plugin looking for responses to the following actions (they all start with `surveys-`):

- `surveys-list`: allows actors to view the list of previously created surveys.
- `surveys-create`: allows actors to create surveys. Won't allow overwriting by itself.
- `surveys-update`: allows actors to update surveys, _resource_: id of the survey if being updated. This permission doesn't stop actors from updating with blank surveys or otherwise removing fields.
- `surveys-delete`: allows actors to delete surveys. _resource_: id of the survey being deleted.
- `surveys-view-form`: allows actors to view and respond to individual forms. _resource_: id of the survey.

## Development

The form builder borrows heavily from [Alpaca's form builder](http://www.alpacajs.org/demos/form-builder/form-builder.html) and the front end build also comes from the Alpaca repo.

To pull the dependencies for the plugin, use bower:

    bower install

And if you don't have bower, run this first: `npm install -g bower`

The form builder is found in `datasette_surveys/static/form-builder.js`. It's a modified version of the Alpaca one.

Running `python setup.py install` will reinstall the plugin.
