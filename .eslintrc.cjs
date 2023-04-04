module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: ["airbnb-base", "prettier"],
  plugins: ["prettier", "jest"],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: "module",
  },
  rules: {
    "prettier/prettier": [
      "error",
      {
        semi: true,
        singleQuote: false,
        tabWidth: 2,
        useTabs: false,
        trailingComma: "all",
      },
    ],
    camelcase: "off",
    "func-names": "off",
    eqeqeq: "error",
    "no-underscore-dangle": "off",
    "lines-between-class-members": "off",
    "import/prefer-default-export": "off",
  },
};
