## Useful Node snippets
https://nodejs.org/dist/latest-v16.x/docs/api/

### Path Examples 
```javascript
const path = require('path');

// Get Filename
const filename = path.basename(__filename);

// Get Directory name
const dirname = path.dirname(__filename);

// Get Parent Directory name
const parentDirname = path.dirname(__dirname);

// Get File extension
const extn = path.extname(__filename);

// Create path object
const pathObj = path.parse(__filename)
// The above returns a break up of the entire path with the following keys -  root, dir, base, ext, name

// Get the base (filename from the above)
const filename = path.parse(__filename).base;

// Concatenate or join paths
const newPath = path.join(__dirname, 'test', 'test1.html');
// Here newPath would be equal to <current_dir_path>/test/test1.html 
```

## FileSystem examples
```javascript
const fs = require('fs');
const path = require('path');

// Create Folder
// The following will create a folder called 'test' in the current directory
fs.mkdir(path.join(__dirname), '/test', {}, err => {
  if(err) throw err;
  console.log("Folder created.")
})

// Create and write to file
// The following will create a file called test.txt in the current directory and write 'hello' in it
fs.writeFile(path.join(__dirname), 'test.txt', 'hello', err => {
  if(err) throw err;
  console.log("File created.")
})
```