; Code shows how differnt directives work

.byte $AA, $BB, $CC
.word 0, $00     
.org $7
.byte $AA, $BB

.include "inc_directives.asm"

; Hex output: AA BB CC 00 00 00 00 AA BB CC
