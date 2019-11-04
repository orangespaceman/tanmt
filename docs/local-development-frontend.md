# TANMT - Local development - Backend

[&laquo; Back](../README.md)

How to start the app locally for day-to-day development work.

## Run the app

* Install any new front-end dependencies:

  ```
  npm install
  ```

* Watch for front-end file changes during development:

  ```
  npm run watch
  ```

## Development

All CSS/JS code should sit in the `/frontend` directory.

Anything in the `/frontend/static` directory will be served by the app


### Components

CSS and JS has been built with a component-led focus.

### CSS

CSS is built with [PostCSS](https://postcss.org/).

CSS follows the [SuitCSS naming conventions](https://github.com/suitcss/suit/blob/master/doc/naming-conventions.md).

### JS

JS is built with [webpack](https://webpack.js.org/).


### Linting

Linting with [Stylelint](https://stylelint.io/) for CSS and [ESLint](https://eslint.org/) for JS, along with [Prettier](https://prettier.io/) on the git pre-commit hook.

To manually lint the frontend code:

```
npm run lint
```


### VS Code

Prettier is set up to run automatically if you use VS Code.
