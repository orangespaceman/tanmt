module.exports = {
  extends: ["eslint:recommended", "prettier"],
  env: {
    browser: true,
    node: true
  },
  globals: {
    Promise: true
  }
};
