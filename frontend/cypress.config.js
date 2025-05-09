const { defineConfig } = require("cypress");
require('dotenv').config();

module.exports = defineConfig({
  reporter: 'mocha-junit-reporter',
  reporterOptions: {
    mochaFile: 'cypress/results-[hash].xml'
  },
  e2e: {
    baseUrl: process.env.VITE_FRONTEND_URL,
    setupNodeEvents(on, config) {
    }
  },
  experimentalStudio: true
});