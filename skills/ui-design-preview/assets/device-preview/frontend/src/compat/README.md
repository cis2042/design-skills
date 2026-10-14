# iframe portal compatibility

The preview renders React portals into same-origin device documents. rc-util
5.44.4 checks DOM nodes against constructors from the outer window. Consequently
rc-trigger cannot resolve a device Select anchor and leaves its popup at
`-1000vw / -1000vh`.

The Vite aliases replace only DOM recognition and visibility helpers, using each
node's owner document. They preserve nativeElement refs and React 18 component
fallbacks. No globals or installed dependencies are patched.

When upgrading rc-util, review these aliases and run `verify_select_popup.py`
and `verify_select_matrix.py` against the static build before removing them.
