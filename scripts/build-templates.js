#!/usr/bin/env node

/**
 * Copy assets into static folder
 */

import cpx from "cpx2";
import clc from "cli-color";
import { deleteAsync } from "del";

const cwd = process.cwd();
const componentDir = "frontend/components";
const targetDir = "tanmt/templates/components";

function start() {
  deleteAsync([targetDir + "**/*"]).then((paths) => {
    paths.forEach((path) => {
      console.log(clc.green("Deleted: " + path.replace(cwd, "")));
    });
    copyFiles();
  });
}

function copyFiles() {
  cpx.copy(`${componentDir}/**/*+(.html|.json)`, `${targetDir}`, {}, report);
}

function report(error, files) {
  if (!error) {
    files.copied.forEach((file) => {
      console.log(clc.green(`Copied: ${file.output}`));
    });
  } else {
    throw error;
  }
}

start();
