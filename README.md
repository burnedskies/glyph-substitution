# Glyph Substitution

This is an attempt at a proof-of-concept of the Glyph Substitution
obfuscation method discussed in a Huntress [blog post](https://www.huntress.com/blog/gootloader-threat-detection-woff2-obfuscation) 
on GOOTLOADER (November 2025).

For this proof-of-concept we take a font file, apply a simple substitution cipher (ROT13) to its glyph data, and load the modified font in a demo page. When that font is applied to page elements, text encoded with ROT13 (for example Uryyb Jbeyq!) is visually rendered as the decoded string (Hello World!).