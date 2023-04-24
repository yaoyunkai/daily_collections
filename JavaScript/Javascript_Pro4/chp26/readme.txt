Javascript module

-------------------------------------------------------------------------------
1. 导出 export

可以放在变量开头:
export const name = "square";

可以在末尾导出
export { name, draw, reportArea, reportPerimeter };

export { function1 as newFunctionName, function2 as anotherNewFunctionName };

-------------------------------------------------------------------------------
2. import
import { name, draw, reportArea, reportPerimeter } from "./modules/square.js";

import { name as squareName, draw } from "./shapes/square.js";
import { name as circleName } from "https://example.com/shapes/circle.js";

import { default as randomSquare } from "./modules/square.js";

import {
  function1 as newFunctionName,
  function2 as anotherNewFunctionName,
} from "./modules/module.js";

import * as Module from "./modules/module.js";

-------------------------------------------------------------------------------
3. import maps
能力检测:
if (HTMLScriptElement.supports?.("importmap")) {
  console.log("Browser supports import maps.");
}

<script type="importmap">
  {
    "imports": {
      "shapes": "./shapes/square.js",
      "shapes/square": "./modules/shapes/square.js",
      "https://example.com/shapes/": "/shapes/square/",
      "https://example.com/shapes/square.js": "./shapes/square.js",
      "../shapes/square": "./shapes/square.js"
    }
  }
</script>

-------------------------------------------------------------------------------
4. 应用模块
<script type="module" src="main.js"></script>

区别:
模块使用严格模式
模块只执行一次，即使它们在多个<script>标签中被引用
模块特性被导入到单个脚本的作用域中 全局作用域不可见


-------------------------------------------------------------------------------
5. 聚合模块

export { Square } from "./shapes/square.js";
export { Triangle } from "./shapes/triangle.js";
export { Circle } from "./shapes/circle.js";

-------------------------------------------------------------------------------
6. 动态模块加载

import("./modules/myModule.js").then((module) => {
  // Do something with the module.
});
