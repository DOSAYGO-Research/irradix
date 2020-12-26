import {irradix, derradix, VALS, encode, decode} from './index.js';

const rep = irradix('234232142312342342314213123321', VALS.BigPHI);
const num = derradix(rep, VALS.BigPHI);

console.log(rep,num.toFixed());

