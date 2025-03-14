import tseslintPlugin from '@typescript-eslint/eslint-plugin'
import tseslintParser from '@typescript-eslint/parser'
import pluginVue from 'eslint-plugin-vue'

export default [
  {
    languageOptions: {
      parser: tseslintParser,
      sourceType: 'module',
      ecmaVersion: 2020,
    },
  },
  tseslintPlugin.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    name: 'custom-rules',
    rules: {
      'vue/multi-word-component-names': 'off',
      'vue/no-multiple-template-root': 'off',
      'vue/no-unused-vars': 'warn',
      '@typescript-eslint/no-unused-vars': ['error'],
      '@typescript-eslint/explicit-module-boundary-types': 'off',
    },
  },
]
