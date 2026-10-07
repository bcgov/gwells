/*
This file is unused. Jest (the node module) has been deleted
from the project for now, as it was already broken and the old
packages had breaking security updates.
The test commands were also removed from package.json to prevent
confusion. But the commands were:
"test:unit": "jest",
"test:coverage": "jest --coverage",
"test:unit:update": "jest -u",
*/

module.exports = {
  moduleFileExtensions: ["js", "jsx", "json", "vue"],
  transform: {
    "^.+\\.vue$": "vue-jest",
    "^.+\\.jsx?$": "babel-jest",
  },
  transformIgnorePatterns: ["/node_modules/"],
  moduleNameMapper: {
    ".+\\.(css|styl|less|sass|scss|svg|png|jpg|ttf|woff|woff2)$": "babel-jest",
    "^@/(.*)$": "<rootDir>/src/$1",
  },
  snapshotSerializers: ["jest-serializer-vue"],
  setupFiles: ["<rootDir>/tests/unit/setup"],
  testMatch: [
    "**/tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx)",
  ],
  testURL: "http://localhost/",
  watchPlugins: [
    "jest-watch-typeahead/filename",
    "jest-watch-typeahead/testname",
  ],
};
