import { irradix, derradix, VALS } from './index.js'

let val = 10n;
for( let i = 0; i < 200; i++ ) {
  const basePhi = irradix(val, VALS.BigPHI);
  const regular = derradix(basePhi, VALS.BigPHI);
  if ( regular != val ) {
    console.log(`Divergence at ${i+2}-digit random value.`);
    const vs = val.toString();
    const rs = regular.toString();
    const track = [];
    for(let j = 0; j < Math.min(vs.length, rs.length); j++) {
      if ( vs[j] != rs[j] ) {
        console.log(`Values differ at the ${j+1}th place:`);
        track.push('^');
      } else {
        track.push(' ');
      }
    }
    console.log(`Original:  ${vs}`);
    console.log(`Recovered: ${rs}`);
    console.log(`           ${track.join('')}`);
  } else {
    console.log(`${i+2}-digit values match: ${regular}`);
  }

  const digit =  BigInt(Math.round(Math.random()*10));
  val *= 10n;
  val += digit;
}

