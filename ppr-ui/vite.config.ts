import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import EnvironmentPlugin from 'vite-plugin-environment'
import vuetify from 'vite-plugin-vuetify'
import commonjs from '@rollup/plugin-commonjs'

import fs from 'fs'
import path from 'path'

const packageJson = fs.readFileSync('./package.json')
const appName = JSON.parse(packageJson).appName
const appVersion = JSON.parse(packageJson).version
const sbcName = JSON.parse(packageJson).sbcName
const sbcVersion = JSON.parse(packageJson).dependencies['sbc-common-components']
const aboutText1 = (appName && appVersion) ? `${appName} v${appVersion}` : ''
const aboutText2 = (sbcName && sbcVersion) ? `${sbcName} v${sbcVersion}` : ''

// https://vitejs.dev/config/
export default defineConfig(() => {
  return {
    define: {
      'import.meta.env.ABOUT_TEXT':
        (aboutText1 && aboutText2)
          ? `"${aboutText1}<br>${aboutText2}"`
          : aboutText1
            ? `"${aboutText1}"`
            : aboutText2
              ? `"${aboutText2}"`
              : ''
    },
    envPrefix: 'VUE_APP_', // Need to remove this after fixing vaults. Use import.meta.env with VUE_APP.
    plugins: [
      vue(),
      vuetify(),
      EnvironmentPlugin({
        BUILD: 'web' // Fix for Vuelidate, allows process.env with Vite.
      }),
      commonjs()
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@sbc': path.resolve(__dirname, './node_modules/sbc-common-components/src')
      },
      extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
    },
    build: {},
    server: {
      host: true,
      port: 8080
    },
    test: {
      server: {
        deps: {
          inline: ['vuetify', 'vue-pdf-embed']
        }
      },
      globals: true,
      threads: true,
      environment: 'jsdom',
      setupFiles: './tests/setup.ts',
      onConsoleLog (log) {
        if (log.includes('Vue warn')) return false // Filter out Vue warnings while preserving errors and logs.
      }
    }
  }
})
