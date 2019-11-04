module.exports = {
  map: false,
  plugins: [
    require("postcss-easy-import")({
      glob: true
    }),
    require("postcss-custom-media")(),
    require("postcss-custom-properties")(),
    require("postcss-calc")(),
    require("autoprefixer")(),
    require("cssnano")()
  ]
};
