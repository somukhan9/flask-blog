const path = require('path')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    path.join(process.cwd(), 'src/project/templates/**/*.html'),
    path.join(process.cwd(), 'src/project/apps/user/templates/**/*.html'),
    path.join(process.cwd(), 'src/project/apps/blog/templates/**/*.html'),
    path.join(process.cwd(), 'src/project/static/js/**/*.js'),
    path.join(process.cwd(), 'src/project/apps/user/static/js/**/*.js'),
    path.join(process.cwd(), 'src/project/apps/blog/static/js/**/*.js'),
  ],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
}
