; A simple "Hello World" program for the C64.
; The program calls a subroutine to change the background colors to red
; We start with a BASIC program that jumps to our assembly code
.org $07FF
.byte $01, $08
.byte $0C, $08
.byte $0A, $00        
.byte $9E, $20        
.byte $32, $30, $36, $34 
.byte $00 
.word $0000

start:
    lda #$00          ; Clear the screen
    jsr $E544         ; Call the KERNAL routine to clear the screen
    ldx #$00          ; Initialize X register to 0
    ldy #$00          ; Initialize Y register to 0
    jsr change_bg

print_loop:
    lda message,x     ; Load the character from the message
    beq done          ; If the character is 0 (end of string), jump to done
    jsr $FFD2         ; Call the KERNAL routine to print the character
    inx               ; Increment X register
    bne print_loop    ; Loop until the end of the string

done:
    rts               ; Return to BASIC

message:
.text "HELLO, WORLD!"
.byte $00

change_bg:
    LDA #$02              ; Load the value 2 into the accumulator (sets red color).
    STA $D020             ; Store the value in $D020 (screen border color register).
    STA $D021             ; Store the value in $D021 (screen background color register).
    RTS                   ; Return from subroutine (ends execution of the machine code).
