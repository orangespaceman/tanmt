import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default {
  entry: {
    site: "./frontend/js/site.js",
    admin: "./frontend/js/admin.js",
  },
  output: {
    path: path.resolve(__dirname, "frontend/static/js/"),
    filename: "[name].js",
  },
  mode: "production",
};
