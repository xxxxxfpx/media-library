/* eslint-env node */
module.exports = {
  root: true,
  env: {
    browser: true,
    es2022: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-essential',
    'prettier',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  ignorePatterns: ['dist/', 'node_modules/', 'public/', 'tests/'],
  rules: {
    // 单文件组件命名允许单单词（如 Home.vue / Media.vue）
    'vue/multi-word-component-names': 'off',
    // 未使用变量仅警告，不阻断 CI
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
    // 允许 console（项目内含调试输出）
    'no-console': 'off',
  },
};
