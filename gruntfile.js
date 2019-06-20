//gruntfile.js
module.exports = function(grunt) {

  grunt.initConfig({
    watch: {
      test: {
        files: ['**/*.py'],
        tasks: ['shell:test'],
        options: {
          cwd: {
            files: 'demand_acep/'
          }
        }
      },
      doc: {
        files: ['**/*.rst'],
        tasks: ['shell:make'],
        options: {
          cwd: {
            files: 'doc/'
          }
        }

      }
    },
    shell: {
      test: {
        command: 'coverage run --source=demand_acep -m pytest . --disable-warnings -s'
      },
      make: {
        command: 'cd doc && make html'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-shell');

  grunt.registerTask('default', ['watch:test']);
  grunt.registerTask('doc', ['watch:doc']);

};

// Add task called 'pylint', different from 'default' to perform pylint on saving
// try this : https://stackoverflow.com/a/52336149/1328232