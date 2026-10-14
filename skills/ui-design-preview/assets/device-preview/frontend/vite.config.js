import {defineConfig} from 'vite';
export default defineConfig({
  base:'./',
  resolve:{alias:[
    {find:/^rc-util\/(?:es|lib)\/Dom\/isVisible(?:\.js)?$/,replacement:new URL('./src/compat/is_visible.js',import.meta.url).pathname},
    {find:/^rc-util\/(?:es|lib)\/Dom\/findDOMNode(?:\.js)?$/,replacement:new URL('./src/compat/find_dom_node.js',import.meta.url).pathname},
  ]},
  build:{rollupOptions:{input:{index:'index.html',review:'review.html'}},chunkSizeWarningLimit:1800}
});
