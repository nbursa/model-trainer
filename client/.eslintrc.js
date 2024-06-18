export default {
  root: true,
  env: {
    node: true,
  },
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  rules: {
    // Add your custom rules here
    'vue/no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': ['error'],
    '@typescript-eslint/explicit-module-boundary-types': 'off',
  },
}
