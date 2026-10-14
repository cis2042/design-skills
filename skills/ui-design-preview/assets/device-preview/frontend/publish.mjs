// 在构建并验收 dist 后调用；保留既有历史资产，不递归删除目标目录。
import {cp,readFile,writeFile} from 'node:fs/promises';
const root=new URL('../',import.meta.url);
for(const file of ['index.html','review.html','assets'])await cp(new URL('dist/'+file,import.meta.url),new URL(file,root),{recursive:true});
console.log('Published static index.html, review.html and bundled assets.');
