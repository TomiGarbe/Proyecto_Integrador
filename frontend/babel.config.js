module.exports = {
  presets: [
    '@babel/preset-env',
    '@babel/preset-react',
  ],
  env: {
    test: {
      plugins: [
        [
          'istanbul',
          {
            exclude: [
              '**/*.test.js',
              '**/*.test.jsx',
              '**/tests/**',
              '**/cypress/**',
            ],
          },
        ],
      ],
    },
  },
};