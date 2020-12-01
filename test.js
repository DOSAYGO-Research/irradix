import {irradix} from './index.js';

console.log(irradix);

for( let i = 0; i < 1024; i ++ ) {
  console.log(`${i} in base pi`, irradix(i, Math.PI));
}
