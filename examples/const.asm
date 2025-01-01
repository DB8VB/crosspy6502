; Code shows how differnt directives work

; Important: Constant are not case-sensitive and must not have the same names as labels
.const TEST $CCCC

.byte $AA, $BB, $CC
.word 0, $00     
.org $7
.byte $AA, $BB
.word test

; Hex output: AA BB CC 00 00 00 00 AA BB CC CC
