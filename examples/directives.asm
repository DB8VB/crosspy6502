; Code shows how differnt directives work

.const TEST $CCCC

.byte $AA, $BB, $CC
.word 0, $00     
.org $7
.byte $AA, $BB
.word TEST
.res 1

; Hex output: AA BB CC 00 00 00 00 AA BB CC 00
