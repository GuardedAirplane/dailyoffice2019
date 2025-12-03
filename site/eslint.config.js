module.exports = [
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
    ],
  },
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser: require('babel-eslint'),
      globals: {
        window: 'readonly',
        document: 'readonly',
      },
    },
    rules: {
      'arrow-parens': [0, 'as-needed'],
      'comma-dangle': [0, 'never'],
      'no-mixed-spaces-and-tabs': 1,
    },
  },
];
