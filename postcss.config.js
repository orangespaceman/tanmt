import postcssEasyImport from "postcss-easy-import";
import postcssCustomMedia from "postcss-custom-media";
import postcssCustomProperties from "postcss-custom-properties";
import postcssCalc from "postcss-calc";
import autoprefixer from "autoprefixer";
import cssnano from "cssnano";

export default {
  map: false,
  plugins: [
    postcssEasyImport({
      glob: true,
    }),
    postcssEasyImport(),
    postcssCustomMedia(),
    postcssCustomProperties(),
    postcssCalc(),
    autoprefixer(),
    cssnano(),
  ],
};
