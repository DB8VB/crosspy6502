; A simple "Hello World" program for the C64.
; We start with a BASIC program that jumps to our assembly code
.org $07FF
.byte $01, $08
.byte $0C, $08
.byte $0A, $00        
.byte $9E, $20        
.byte $32, $30, $36, $34 
.byte $00 
.byte $00, $00

start:
    lda #$00          ; Clear the screen
    jsr $E544         ; Call the KERNAL routine to clear the screen
    ldx #$00          ; Initialize X register to 0
    ldy #$00          ; Initialize Y register to 0

print_loop:
    lda message,x     ; Load the character from the message
    beq done          ; If the character is 0 (end of string), jump to done
    jsr $FFD2         ; Call the KERNAL routine to print the character
    inx               ; Increment X register
    bne print_loop    ; Loop until the end of the string

done:
    rts               ; Return to BASIC

message:
    .byte $48, $45, $4C, $4C, $4F, $2C, $20, $57, $4F, $52, $4C, $44, $21, $00  ; "HELLO, WORLD!" null-terminated