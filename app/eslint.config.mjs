import globals from 'globals';
import eslintJs from '@eslint/js'; // Import CommonJS module for eslint:recommended
import vue from 'eslint-plugin-vue';
import prettierPlugin from 'eslint-plugin-prettier';
import vueScopedCss from 'eslint-plugin-vue-scoped-css';
import vueEslintParser from 'vue-eslint-parser';

// Use a simpler config approach
export default [
  // Basic eslint recommended rules
  eslintJs.configs.recommended,

  // Vue files specific configuration
  {
    files: ['**/*.vue'],
    plugins: {
      vue,
    },
    languageOptions: {
      parser: vueEslintParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    rules: {
      // Common Vue rules that should be present in most versions
      'vue/multi-word-component-names': 'off',
      'vue/no-v-html': 'off',
      'vue/no-v-text-v-html-on-component': 'off',
      'vue/no-deprecated-slot-attribute': 'error',
      'vue/no-unused-components': 'error',
      'vue/require-v-for-key': 'error',
      'vue/no-use-v-if-with-v-for': 'error',
    },
  },

  // General JS/Vue configuration
  {
    files: ['**/*.js', '**/*.vue'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.mocha,
        window: 'readonly',
        document: 'readonly',
        navigator: 'readonly',
        location: 'readonly',
        history: 'readonly',
        getComputedStyle: 'readonly',
        console: 'readonly',
        module: 'readonly',
        require: 'readonly',
        process: 'readonly',
        __dirname: 'readonly',
        Audio: 'readonly',
      },
    },
    plugins: {
      vue,
      prettier: prettierPlugin,
      'vue-scoped-css': vueScopedCss,
    },
    rules: {
      // Basic rules
      'no-console': 'error',
      'no-debugger': 'error',
      'no-unused-vars': 'error',

      // Prettier rule
      'prettier/prettier': 'error',
    },
  },

  // Files to ignore
  {
    ignores: [
      // Dependencies
      'node_modules/**',
      '.pnp.*',
      '.yarn/*',
      '!.yarn/patches',
      '!.yarn/releases',
      '!.yarn/plugins',
      '!.yarn/sdks',
      '!.yarn/versions',

      // Build outputs
      'dist/**',
      'build/**',
      'coverage/**',
      'www/**',
      'static/**',
      'static_export/**',

      // Auto-generated files
      '*.min.js',
      '*.bundle.js',
      'webpack-stats.json',
      'auto-imports.d.ts',
      'components.d.ts',

      // Test outputs
      'tests/e2e/videos/**',
      'tests/e2e/screenshots/**',

      // Configuration files (already checked separately)
      '*.config.js',
      '*.config.mjs',
      '*.config.ts',

      // Third-party
      'vendor/**',

      // Mobile platforms
      'ios/**',
      'android/**',
    ],
  },
];
