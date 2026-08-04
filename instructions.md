# MLVM Instruction Set Architecture

- [Immediate Loads](#immediate-loads)
- [Memory Reads](#memory-reads)
- [Memory Writes](#memory-writes)
- [Register Assignment](#register-assignment)
- [Increment and Decrement](#increment-and-decrement)
- [Arithmetic and Bitwise Operators](#arithmetic-and-bitwise-operators)
- [Comparisons](#comparisons)
- [Jumps](#jumps)
- [Stack and Subroutines](#stack-and-subroutines)
- [Interrupts](#interrupts)
- [System Control](#system-control)

| | `0x_0` | `0x_1` | `0x_2` | `0x_3` | `0x_4` | `0x_5` | `0x_6` | `0x_7` | `0x_8` | `0x_9` | `0x_A` | `0x_B` | `0x_C` | `0x_D` | `0x_E` | `0x_F` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `0x0_` | [**LIA**](#lia)<br>3c | [**LIB**](#lib)<br>3c | [**LIC**](#lic)<br>3c |  | [**LIA8**](#lia8)<br>2c | [**LIB8**](#lib8)<br>2c | [**LIC8**](#lic8)<br>2c |  | [**LIA8S**](#lia8s)<br>2c | [**LIB8S**](#lib8s)<br>2c | [**LIC8S**](#lic8s)<br>2c |  |  |  |  | [**SOF**](#sof)<br>3c |
| `0x1_` | [**RDA**](#rda)<br>3c | [**RDB**](#rdb)<br>3c | [**RDC**](#rdc)<br>3c |  | [**RDA8**](#rda8)<br>2c | [**RDB8**](#rdb8)<br>2c | [**RDC8**](#rdc8)<br>2c |  | [**RDA8S**](#rda8s)<br>2c | [**RDB8S**](#rdb8s)<br>2c | [**RDC8S**](#rdc8s)<br>2c |  |  |  |  |  |
| `0x2_` | [**RSA**](#rsa)<br>5c | [**RSB**](#rsb)<br>5c | [**RSC**](#rsc)<br>5c |  | [**RSA8**](#rsa8)<br>4c | [**RSB8**](#rsb8)<br>4c | [**RSC8**](#rsc8)<br>4c |  | [**RSA8S**](#rsa8s)<br>4c | [**RSB8S**](#rsb8s)<br>4c | [**RSC8S**](#rsc8s)<br>4c |  |  |  |  |  |
| `0x3_` | [**WRA**](#wra)<br>3c | [**WRB**](#wrb)<br>3c | [**WRC**](#wrc)<br>3c |  | [**WRA8**](#wra8)<br>2c | [**WRB8**](#wrb8)<br>2c | [**WRC8**](#wrc8)<br>2c |  |  |  |  |  |  |  |  |  |
| `0x4_` | [**WSA**](#wsa)<br>5c | [**WSB**](#wsb)<br>5c | [**WSC**](#wsc)<br>5c |  | [**WSA8**](#wsa8)<br>4c | [**WSB8**](#wsb8)<br>4c | [**WSC8**](#wsc8)<br>4c |  |  |  |  |  |  |  |  |  |
| `0x5_` | [**RIA**](#ria)<br>5c | [**RIB**](#rib)<br>5c | [**RIC**](#ric)<br>5c |  | [**RIA8**](#ria8)<br>4c | [**RIB8**](#rib8)<br>4c | [**RIC8**](#ric8)<br>4c |  | [**RIA8S**](#ria8s)<br>4c | [**RIB8S**](#rib8s)<br>4c | [**RIC8S**](#ric8s)<br>4c |  |  |  |  |  |
| `0x6_` | [**WIA**](#wia)<br>5c | [**WIB**](#wib)<br>5c | [**WIC**](#wic)<br>5c |  | [**WIA8**](#wia8)<br>4c | [**WIB8**](#wib8)<br>4c | [**WIC8**](#wic8)<br>4c |  |  |  |  |  |  |  | [**WII**](#wii)<br>7c | [**WII8**](#wii8)<br>5c |
| `0x7_` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `0x8_` | [**HLT**](#hlt)<br>1c | [**CLI**](#cli)<br>1c | [**STI**](#sti)<br>1c |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `0x9_` | [**SAB**](#sab)<br>1c | [**SAC**](#sac)<br>1c | [**SAS**](#sas)<br>1c | [**SBA**](#sba)<br>1c | [**SBC**](#sbc)<br>1c | [**SCA**](#sca)<br>1c | [**SCB**](#scb)<br>1c | [**SDC**](#sdc)<br>1c | [**SAD**](#sad)<br>1c | [**SBD**](#sbd)<br>1c | [**SCD**](#scd)<br>1c |  |  |  |  |  |
| `0xA_` | [**INA**](#ina)<br>1c | [**INB**](#inb)<br>1c | [**INC**](#inc)<br>1c | [**DEA**](#dea)<br>1c | [**DEB**](#deb)<br>1c | [**DEC**](#dec)<br>1c | [**INS**](#ins)<br>7c | [**INS8**](#ins8)<br>5c | [**INI**](#ini)<br>7c | [**INI8**](#ini8)<br>5c | [**DES**](#des)<br>7c | [**DES8**](#des8)<br>5c | [**DEI**](#dei)<br>7c | [**DEI8**](#dei8)<br>5c |  |  |
| `0xB_` | [**AND**](#and)<br>1c | [**IOR**](#ior)<br>1c | [**XOR**](#xor)<br>1c | [**NOT**](#not)<br>1c | [**ADD**](#add)<br>1c | [**SUB**](#sub)<br>1c | [**MUL**](#mul)<br>1c | [**RSS**](#rss)<br>1c | [**LSS**](#lss)<br>1c | [**ANL**](#anl)<br>1c | [**MOD**](#mod)<br>1c | [**DIV**](#div)<br>1c | [**NEG**](#neg)<br>1c |  |  |  |
| `0xC_` | [**CMP**](#cmp)<br>1c | [**GTE**](#gte)<br>1c | [**LTE**](#lte)<br>1c | [**GTC**](#gtc)<br>1c | [**LTC**](#ltc)<br>1c | [**SGE**](#sge)<br>1c | [**SLE**](#sle)<br>1c | [**SGT**](#sgt)<br>1c | [**SLT**](#slt)<br>1c | [**NEQ**](#neq)<br>1c |  |  |  |  |  |  |
| `0xD_` | [**JMP**](#jmp)<br>1c | [**JIA**](#jia)<br>1c | [**JIB**](#jib)<br>1c | [**JIC**](#jic)<br>1c | [**JIX**](#jix)<br>1c | [**JIY**](#jiy)<br>1c | [**JIZ**](#jiz)<br>1c | [**JSC**](#jsc)<br>1c | [**JMI**](#jmi)<br>3c | [**JAI**](#jai)<br>3c | [**JBI**](#jbi)<br>3c | [**JCI**](#jci)<br>3c | [**JXI**](#jxi)<br>3c | [**JYI**](#jyi)<br>3c | [**JZI**](#jzi)<br>3c |  |
| `0xE_` | [**SVI**](#svi)<br>14c | [**LDI**](#ldi)<br>14c | [**SRT**](#srt)<br>3c | [**SIA**](#sia)<br>3c | [**SIB**](#sib)<br>3c | [**SIC**](#sic)<br>3c | [**SRI**](#sri)<br>5c | [**RET**](#ret)<br>3c | [**RTI**](#rti)<br>1c | [**PSHI**](#pshi)<br>5c | [**PSHI8**](#pshi8)<br>3c | [**INT**](#int)<br>2c |  |  | [**PSHN**](#pshn)<br>3c | [**PULN**](#puln)<br>3c |
| `0xF_` | [**PSHA**](#psha)<br>3c | [**PSHB**](#pshb)<br>3c | [**PSHC**](#pshc)<br>3c | [**PSHD**](#pshd)<br>3c | [**PULA**](#pula)<br>3c | [**PULB**](#pulb)<br>3c | [**PULC**](#pulc)<br>3c | [**PULD**](#puld)<br>3c | [**PSHA8**](#psha8)<br>2c | [**PSHB8**](#pshb8)<br>2c | [**PSHC8**](#pshc8)<br>2c | [**PSHD8**](#pshd8)<br>2c | [**PULA8**](#pula8)<br>2c | [**PULB8**](#pulb8)<br>2c | [**PULC8**](#pulc8)<br>2c | [**PULD8**](#puld8)<br>2c |

## Immediate Loads

### LIA
> Name: Load Immediate into A  
> Opcode: `0x00`  
> Cycles: 3

Loads a 2 byte immediate value into register A.

1. Fetch the low byte of the immediate value
2. Fetch the high byte of the immediate value
3. Combine both bytes and store the result in A

### LIB
> Name: Load Immediate into B  
> Opcode: `0x01`  
> Cycles: 3

Loads a 2 byte immediate value into register B.

1. Fetch the low byte of the immediate value
2. Fetch the high byte of the immediate value
3. Combine both bytes and store the result in B

### LIC
> Name: Load Immediate into C  
> Opcode: `0x02`  
> Cycles: 3

Loads a 2 byte immediate value into register C.

1. Fetch the low byte of the immediate value
2. Fetch the high byte of the immediate value
3. Combine both bytes and store the result in C

### LIA8
> Name: Load 1 Byte Immediate into A (Zero Extended)  
> Opcode: `0x04`  
> Cycles: 2

Loads a 1 byte immediate into A, zero extended to 2 bytes. One byte in ROM, not two.

1. Fetch the immediate byte
2. Zero-extend the byte and store the result in A

### LIB8
> Name: Load 1 Byte Immediate into B (Zero Extended)  
> Opcode: `0x05`  
> Cycles: 2

Loads a 1 byte immediate into B, zero extended to 2 bytes.

1. Fetch the immediate byte
2. Zero-extend the byte and store the result in B

### LIC8
> Name: Load 1 Byte Immediate into C (Zero Extended)  
> Opcode: `0x06`  
> Cycles: 2

Loads a 1 byte immediate into C, zero extended to 2 bytes.

1. Fetch the immediate byte
2. Zero-extend the byte and store the result in C

### LIA8S
> Name: Load 1 Byte Immediate into A (Sign Extended)  
> Opcode: `0x08`  
> Cycles: 2

Loads a 1 byte immediate into A, sign extended to 2 bytes.

1. Fetch the immediate byte
2. Sign-extend the byte and store the result in A

### LIB8S
> Name: Load 1 Byte Immediate into B (Sign Extended)  
> Opcode: `0x09`  
> Cycles: 2

Loads a 1 byte immediate into B, sign extended to 2 bytes.

1. Fetch the immediate byte
2. Sign-extend the byte and store the result in B

### LIC8S
> Name: Load 1 Byte Immediate into C (Sign Extended)  
> Opcode: `0x0A`  
> Cycles: 2

Loads a 1 byte immediate into C, sign extended to 2 bytes.

1. Fetch the immediate byte
2. Sign-extend the byte and store the result in C

### SOF
> Name: Stack Offset  
> Opcode: `0x0F`  
> Cycles: 3

Computes a stack-pointer-relative address (STACK_START_ADDR + T + imm16) and stores it in C.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Add STACK_START_ADDR, T, and the offset, and store the result in C

## Memory Reads

### RDA
> Name: Read into A  
> Opcode: `0x10`  
> Cycles: 3

Reads 2 bytes at the address in C into A.

1. Read the low byte at address C
2. Read the high byte at address C+1
3. Combine both bytes and store the result in A

### RDB
> Name: Read into B  
> Opcode: `0x11`  
> Cycles: 3

Reads 2 bytes at the address in C into B.

1. Read the low byte at address C
2. Read the high byte at address C+1
3. Combine both bytes and store the result in B

### RDC
> Name: Read into C  
> Opcode: `0x12`  
> Cycles: 3

Reads 2 bytes at the address in C into C.

1. Read the low byte at address C
2. Read the high byte at address C+1
3. Combine both bytes and store the result in C

### RDA8
> Name: Read Byte into A (Zero Extended)  
> Opcode: `0x14`  
> Cycles: 2

Reads 1 byte at the address in C into A, zero extended.

1. Read the byte at address C
2. Zero-extend the byte and store the result in A

### RDB8
> Name: Read Byte into B (Zero Extended)  
> Opcode: `0x15`  
> Cycles: 2

Reads 1 byte at the address in C into B, zero extended.

1. Read the byte at address C
2. Zero-extend the byte and store the result in B

### RDC8
> Name: Read Byte into C (Zero Extended)  
> Opcode: `0x16`  
> Cycles: 2

Reads 1 byte at the address in C into C, zero extended.

1. Read the byte at address C
2. Zero-extend the byte and store the result in C

### RDA8S
> Name: Read Byte into A (Sign Extended)  
> Opcode: `0x18`  
> Cycles: 2

Reads 1 byte at the address in C into A, sign extended.

1. Read the byte at address C
2. Sign-extend the byte and store the result in A

### RDB8S
> Name: Read Byte into B (Sign Extended)  
> Opcode: `0x19`  
> Cycles: 2

Reads 1 byte at the address in C into B, sign extended.

1. Read the byte at address C
2. Sign-extend the byte and store the result in B

### RDC8S
> Name: Read Byte into C (Sign Extended)  
> Opcode: `0x1A`  
> Cycles: 2

Reads 1 byte at the address in C into C, sign extended.

1. Read the byte at address C
2. Sign-extend the byte and store the result in C

### RSA
> Name: Read Stack-Relative into A  
> Opcode: `0x20`  
> Cycles: 5

Reads 2 bytes at (STACK_START_ADDR + T + imm16) into A.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the low byte of the value there
4. Store the low byte in A and read the high byte of the value
5. Combine the high byte into A

### RSB
> Name: Read Stack-Relative into B  
> Opcode: `0x21`  
> Cycles: 5

Reads 2 bytes at (STACK_START_ADDR + T + imm16) into B.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the low byte of the value there
4. Store the low byte in B and read the high byte of the value
5. Combine the high byte into B

### RSC
> Name: Read Stack-Relative into C  
> Opcode: `0x22`  
> Cycles: 5

Reads 2 bytes at (STACK_START_ADDR + T + imm16) into C.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the low byte of the value there
4. Store the low byte in C and read the high byte of the value
5. Combine the high byte into C

### RSA8
> Name: Read Stack-Relative Byte into A (Zero Extended)  
> Opcode: `0x24`  
> Cycles: 4

Reads 1 byte at (STACK_START_ADDR + T + imm16) into A, zero extended.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Zero-extend the byte and store the result in A

### RSB8
> Name: Read Stack-Relative Byte into B (Zero Extended)  
> Opcode: `0x25`  
> Cycles: 4

Reads 1 byte at (STACK_START_ADDR + T + imm16) into B, zero extended.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Zero-extend the byte and store the result in B

### RSC8
> Name: Read Stack-Relative Byte into C (Zero Extended)  
> Opcode: `0x26`  
> Cycles: 4

Reads 1 byte at (STACK_START_ADDR + T + imm16) into C, zero extended.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Zero-extend the byte and store the result in C

### RSA8S
> Name: Read Stack-Relative Byte into A (Sign Extended)  
> Opcode: `0x28`  
> Cycles: 4

Reads 1 byte at (STACK_START_ADDR + T + imm16) into A, sign extended.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Sign-extend the byte and store the result in A

### RSB8S
> Name: Read Stack-Relative Byte into B (Sign Extended)  
> Opcode: `0x29`  
> Cycles: 4

Reads 1 byte at (STACK_START_ADDR + T + imm16) into B, sign extended.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Sign-extend the byte and store the result in B

### RSC8S
> Name: Read Stack-Relative Byte into C (Sign Extended)  
> Opcode: `0x2A`  
> Cycles: 4

Reads 1 byte at (STACK_START_ADDR + T + imm16) into C, sign extended.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Sign-extend the byte and store the result in C

### RIA
> Name: Read Immediate-Address into A  
> Opcode: `0x50`  
> Cycles: 5

Reads 2 bytes at an immediate absolute address into A.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the low byte of the value there
4. Store the low byte in A and read the high byte of the value
5. Combine the high byte into A

### RIB
> Name: Read Immediate-Address into B  
> Opcode: `0x51`  
> Cycles: 5

Reads 2 bytes at an immediate absolute address into B.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the low byte of the value there
4. Store the low byte in B and read the high byte of the value
5. Combine the high byte into B

### RIC
> Name: Read Immediate-Address into C  
> Opcode: `0x52`  
> Cycles: 5

Reads 2 bytes at an immediate absolute address into C.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the low byte of the value there
4. Store the low byte in C and read the high byte of the value
5. Combine the high byte into C

### RIA8
> Name: Read Immediate-Address Byte into A (Zero Extended)  
> Opcode: `0x54`  
> Cycles: 4

Reads 1 byte at an immediate absolute address into A, zero extended.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Zero-extend the byte and store the result in A

### RIB8
> Name: Read Immediate-Address Byte into B (Zero Extended)  
> Opcode: `0x55`  
> Cycles: 4

Reads 1 byte at an immediate absolute address into B, zero extended.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Zero-extend the byte and store the result in B

### RIC8
> Name: Read Immediate-Address Byte into C (Zero Extended)  
> Opcode: `0x56`  
> Cycles: 4

Reads 1 byte at an immediate absolute address into C, zero extended.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Zero-extend the byte and store the result in C

### RIA8S
> Name: Read Immediate-Address Byte into A (Sign Extended)  
> Opcode: `0x58`  
> Cycles: 4

Reads 1 byte at an immediate absolute address into A, sign extended.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Sign-extend the byte and store the result in A

### RIB8S
> Name: Read Immediate-Address Byte into B (Sign Extended)  
> Opcode: `0x59`  
> Cycles: 4

Reads 1 byte at an immediate absolute address into B, sign extended.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Sign-extend the byte and store the result in B

### RIC8S
> Name: Read Immediate-Address Byte into C (Sign Extended)  
> Opcode: `0x5A`  
> Cycles: 4

Reads 1 byte at an immediate absolute address into C, sign extended.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Sign-extend the byte and store the result in C

## Memory Writes

### WRA
> Name: Write A  
> Opcode: `0x30`  
> Cycles: 3

Writes 2 bytes of A to the address in C.

1. Write the low byte of A to address C
2. Write the high byte of A to address C+1
3. Delay one cycle so the write commits

### WRB
> Name: Write B  
> Opcode: `0x31`  
> Cycles: 3

Writes 2 bytes of B to the address in C.

1. Write the low byte of B to address C
2. Write the high byte of B to address C+1
3. Delay one cycle so the write commits

### WRC
> Name: Write C  
> Opcode: `0x32`  
> Cycles: 3

Writes 2 bytes of C to the address in C.

1. Write the low byte of C to address C
2. Write the high byte of C to address C+1
3. Delay one cycle so the write commits

### WRA8
> Name: Write Byte of A  
> Opcode: `0x34`  
> Cycles: 2

Writes the low 1 byte of A to the address in C.

1. Write the low byte of A to address C
2. Delay one cycle so the write commits

### WRB8
> Name: Write Byte of B  
> Opcode: `0x35`  
> Cycles: 2

Writes the low 1 byte of B to the address in C.

1. Write the low byte of B to address C
2. Delay one cycle so the write commits

### WRC8
> Name: Write Byte of C  
> Opcode: `0x36`  
> Cycles: 2

Writes the low 1 byte of C to the address in C.

1. Write the low byte of C to address C
2. Delay one cycle so the write commits

### WSA
> Name: Write Stack-Relative A  
> Opcode: `0x40`  
> Cycles: 5

Writes 2 bytes of A to (STACK_START_ADDR + T + imm16).

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and write the low byte of A there
4. Write the high byte of A
5. Delay one cycle so the write commits

### WSB
> Name: Write Stack-Relative B  
> Opcode: `0x41`  
> Cycles: 5

Writes 2 bytes of B to (STACK_START_ADDR + T + imm16).

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and write the low byte of B there
4. Write the high byte of B
5. Delay one cycle so the write commits

### WSC
> Name: Write Stack-Relative C  
> Opcode: `0x42`  
> Cycles: 5

Writes 2 bytes of C to (STACK_START_ADDR + T + imm16).

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and write the low byte of C there
4. Write the high byte of C
5. Delay one cycle so the write commits

### WSA8
> Name: Write Stack-Relative Byte of A  
> Opcode: `0x44`  
> Cycles: 4

Writes the low 1 byte of A to (STACK_START_ADDR + T + imm16).

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and write the low byte of A there
4. Delay one cycle so the write commits

### WSB8
> Name: Write Stack-Relative Byte of B  
> Opcode: `0x45`  
> Cycles: 4

Writes the low 1 byte of B to (STACK_START_ADDR + T + imm16).

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and write the low byte of B there
4. Delay one cycle so the write commits

### WSC8
> Name: Write Stack-Relative Byte of C  
> Opcode: `0x46`  
> Cycles: 4

Writes the low 1 byte of C to (STACK_START_ADDR + T + imm16).

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and write the low byte of C there
4. Delay one cycle so the write commits

### WIA
> Name: Write Immediate-Address A  
> Opcode: `0x60`  
> Cycles: 5

Writes 2 bytes of A to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and write the low byte of A there
4. Write the high byte of A
5. Delay one cycle so the write commits

### WIB
> Name: Write Immediate-Address B  
> Opcode: `0x61`  
> Cycles: 5

Writes 2 bytes of B to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and write the low byte of B there
4. Write the high byte of B
5. Delay one cycle so the write commits

### WIC
> Name: Write Immediate-Address C  
> Opcode: `0x62`  
> Cycles: 5

Writes 2 bytes of C to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and write the low byte of C there
4. Write the high byte of C
5. Delay one cycle so the write commits

### WIA8
> Name: Write Immediate-Address Byte of A  
> Opcode: `0x64`  
> Cycles: 4

Writes the low 1 byte of A to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and write the low byte of A there
4. Delay one cycle so the write commits

### WIB8
> Name: Write Immediate-Address Byte of B  
> Opcode: `0x65`  
> Cycles: 4

Writes the low 1 byte of B to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and write the low byte of B there
4. Delay one cycle so the write commits

### WIC8
> Name: Write Immediate-Address Byte of C  
> Opcode: `0x66`  
> Cycles: 4

Writes the low 1 byte of C to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and write the low byte of C there
4. Delay one cycle so the write commits

### WII
> Name: Write Immediate Value to Immediate Address  
> Opcode: `0x6E`  
> Cycles: 7

Writes a 2 byte immediate value to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and fetch the low byte of the immediate value
4. Write the low byte of the value to the address
5. Fetch the high byte of the immediate value
6. Write the high byte of the value to address+1
7. Delay one cycle so the write commits

### WII8
> Name: Write Immediate Byte to Immediate Address  
> Opcode: `0x6F`  
> Cycles: 5

Writes a 1 byte immediate value to an immediate absolute address.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and fetch the immediate value byte
4. Write the value byte to the address
5. Delay one cycle so the write commits

## Register Assignment

### SAB
> Name: Set A from B  
> Opcode: `0x90`  
> Cycles: 1

Copies B into A.

1. Set A to the value of B.

### SAC
> Name: Set A from C  
> Opcode: `0x91`  
> Cycles: 1

Copies C into A.

1. Set A to the value of C.

### SAS
> Name: Set A from S  
> Opcode: `0x92`  
> Cycles: 1

Copies the status register S into A.

1. Set A to the value of S.

### SBA
> Name: Set B from A  
> Opcode: `0x93`  
> Cycles: 1

Copies A into B.

1. Set B to the value of A.

### SBC
> Name: Set B from C  
> Opcode: `0x94`  
> Cycles: 1

Copies C into B.

1. Set B to the value of C.

### SCA
> Name: Set C from A  
> Opcode: `0x95`  
> Cycles: 1

Copies A into C.

1. Set C to the value of A.

### SCB
> Name: Set C from B  
> Opcode: `0x96`  
> Cycles: 1

Copies B into C.

1. Set C to the value of B.

### SDC
> Name: Set D from C  
> Opcode: `0x97`  
> Cycles: 1

Copies C into D.

1. Set D to the value of C.

### SAD
> Name: Set A from D  
> Opcode: `0x98`  
> Cycles: 1

Copies D into A.

1. Set A to the value of D.

### SBD
> Name: Set B from D  
> Opcode: `0x99`  
> Cycles: 1

Copies D into B.

1. Set B to the value of D.

### SCD
> Name: Set C from D  
> Opcode: `0x9A`  
> Cycles: 1

Copies D into C.

1. Set C to the value of D.

## Increment and Decrement

### INA
> Name: Increment A  
> Opcode: `0xA0`  
> Cycles: 1

Increments A by 1, wrapping at 0xFFFF.

1. Increment A.

### INB
> Name: Increment B  
> Opcode: `0xA1`  
> Cycles: 1

Increments B by 1, wrapping at 0xFFFF.

1. Increment B.

### INC
> Name: Increment C  
> Opcode: `0xA2`  
> Cycles: 1

Increments C by 1, wrapping at 0xFFFF.

1. Increment C.

### DEA
> Name: Decrement A  
> Opcode: `0xA3`  
> Cycles: 1

Decrements A by 1, wrapping at 0xFFFF.

1. Decrement A.

### DEB
> Name: Decrement B  
> Opcode: `0xA4`  
> Cycles: 1

Decrements B by 1, wrapping at 0xFFFF.

1. Decrement B.

### DEC
> Name: Decrement C  
> Opcode: `0xA5`  
> Cycles: 1

Decrements C by 1, wrapping at 0xFFFF.

1. Decrement C.

### INS
> Name: Increment Stack-Relative  
> Opcode: `0xA6`  
> Cycles: 7

Increments the 2 byte value at (STACK_START_ADDR + T + imm16) by 1.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the low byte of the value there
4. Store the low byte in A and read the high byte of the value
5. Combine and increment the value, then write the low byte back
6. Write the high byte back
7. Delay one cycle so the write commits

### INS8
> Name: Increment Stack-Relative Byte  
> Opcode: `0xA7`  
> Cycles: 5

Increments the 1 byte value at (STACK_START_ADDR + T + imm16) by 1.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Increment the value and write it back
5. Delay one cycle so the write commits

### INI
> Name: Increment Immediate-Address  
> Opcode: `0xA8`  
> Cycles: 7

Increments the 2 byte value at an immediate absolute address by 1.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the low byte of the value there
4. Store the low byte in A and read the high byte of the value
5. Combine and increment the value, then write the low byte back
6. Write the high byte back
7. Delay one cycle so the write commits

### INI8
> Name: Increment Immediate-Address Byte  
> Opcode: `0xA9`  
> Cycles: 5

Increments the 1 byte value at an immediate absolute address by 1.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Increment the value and write it back
5. Delay one cycle so the write commits

### DES
> Name: Decrement Stack-Relative  
> Opcode: `0xAA`  
> Cycles: 7

Decrements the 2 byte value at (STACK_START_ADDR + T + imm16) by 1.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the low byte of the value there
4. Store the low byte in A and read the high byte of the value
5. Combine and decrement the value, then write the low byte back
6. Write the high byte back
7. Delay one cycle so the write commits

### DES8
> Name: Decrement Stack-Relative Byte  
> Opcode: `0xAB`  
> Cycles: 5

Decrements the 1 byte value at (STACK_START_ADDR + T + imm16) by 1.

1. Fetch the low byte of the offset immediate
2. Fetch the high byte of the offset immediate
3. Compute the stack-relative address and read the value byte there
4. Decrement the value and write it back
5. Delay one cycle so the write commits

### DEI
> Name: Decrement Immediate-Address  
> Opcode: `0xAC`  
> Cycles: 7

Decrements the 2 byte value at an immediate absolute address by 1.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the low byte of the value there
4. Store the low byte in A and read the high byte of the value
5. Combine and decrement the value, then write the low byte back
6. Write the high byte back
7. Delay one cycle so the write commits

### DEI8
> Name: Decrement Immediate-Address Byte  
> Opcode: `0xAD`  
> Cycles: 5

Decrements the 1 byte value at an immediate absolute address by 1.

1. Fetch the low byte of the address
2. Fetch the high byte of the address
3. Combine the address and read the value byte there
4. Decrement the value and write it back
5. Delay one cycle so the write commits

## Arithmetic and Bitwise Operators

### AND
> Name: Bitwise AND  
> Opcode: `0xB0`  
> Cycles: 1

C = A & B.

1. Set C to A bitwise AND B

### IOR
> Name: Bitwise OR  
> Opcode: `0xB1`  
> Cycles: 1

C = A | B.

1. Set C to A bitwise OR B

### XOR
> Name: Bitwise XOR  
> Opcode: `0xB2`  
> Cycles: 1

C = A ^ B.

1. Set C to A bitwise XOR B

### NOT
> Name: Bitwise NOT  
> Opcode: `0xB3`  
> Cycles: 1

C = ~A. B is not used.

1. Set C to the bitwise complement of A

### ADD
> Name: Addition  
> Opcode: `0xB4`  
> Cycles: 1

C = A + B. Sets the carry status bit if the result overflowed 2 bytes.

1. Add A and B into C, updating the carry flag

### SUB
> Name: Subtraction  
> Opcode: `0xB5`  
> Cycles: 1

C = A - B, computed via two's complement. Sets the carry status bit if the result overflowed.

1. Subtract B from A into C, updating the carry flag

### MUL
> Name: Multiplication  
> Opcode: `0xB6`  
> Cycles: 1

C = (A * B), truncated to 2 bytes. There is no wide/high-half result.

1. Multiply A by B, truncate to 2 bytes, and store the result in C

### RSS
> Name: Right Shift  
> Opcode: `0xB7`  
> Cycles: 1

C = A >> B.

1. Shift A right by B bits and store the result in C

### LSS
> Name: Left Shift  
> Opcode: `0xB8`  
> Cycles: 1

C = A << B, truncated to 2 bytes.

1. Shift A left by B bits and store the result in C

### ANL
> Name: Logical AND  
> Opcode: `0xB9`  
> Cycles: 1

C = 1 if both A and B are nonzero, else 0.

1. Set C to the logical AND of A and B

### MOD
> Name: Modulo  
> Opcode: `0xBA`  
> Cycles: 1

C = A % B.

1. Set C to A modulo B

### DIV
> Name: Integer Division  
> Opcode: `0xBB`  
> Cycles: 1

C = A // B.

1. Set C to A divided by B, rounded down

### NEG
> Name: Negate  
> Opcode: `0xBC`  
> Cycles: 1

C = -A, two's complement. B is not used.

1. Set C to the two's complement negation of A

## Comparisons

### CMP
> Name: Equals  
> Opcode: `0xC0`  
> Cycles: 1

C = 1 if A == B, else 0.

1. Compare A and B for equality and store the result in C

### GTE
> Name: Unsigned Greater Than or Equal  
> Opcode: `0xC1`  
> Cycles: 1

C = 1 if A >= B (unsigned), else 0.

1. Compare A and B as unsigned values and store the result in C

### LTE
> Name: Unsigned Less Than or Equal  
> Opcode: `0xC2`  
> Cycles: 1

C = 1 if A <= B (unsigned), else 0.

1. Compare A and B as unsigned values and store the result in C

### GTC
> Name: Unsigned Greater Than  
> Opcode: `0xC3`  
> Cycles: 1

C = 1 if A > B (unsigned), else 0.

1. Compare A and B as unsigned values and store the result in C

### LTC
> Name: Unsigned Less Than  
> Opcode: `0xC4`  
> Cycles: 1

C = 1 if A < B (unsigned), else 0.

1. Compare A and B as unsigned values and store the result in C

### SGE
> Name: Signed Greater Than or Equal  
> Opcode: `0xC5`  
> Cycles: 1

C = 1 if A >= B, comparing both as two's complement signed values, else 0.

1. Compare A and B as signed values and store the result in C

### SLE
> Name: Signed Less Than or Equal  
> Opcode: `0xC6`  
> Cycles: 1

C = 1 if A <= B, comparing both as two's complement signed values, else 0.

1. Compare A and B as signed values and store the result in C

### SGT
> Name: Signed Greater Than  
> Opcode: `0xC7`  
> Cycles: 1

C = 1 if A > B, comparing both as two's complement signed values, else 0.

1. Compare A and B as signed values and store the result in C

### SLT
> Name: Signed Less Than  
> Opcode: `0xC8`  
> Cycles: 1

C = 1 if A < B, comparing both as two's complement signed values, else 0.

1. Compare A and B as signed values and store the result in C

### NEQ
> Name: Not Equal  
> Opcode: `0xC9`  
> Cycles: 1

C = 1 if A != B, else 0.

1. Compare A and B for inequality and store the result in C

## Jumps

### JMP
> Name: Jump  
> Opcode: `0xD0`  
> Cycles: 1

Jumps to the address in C.

1. Set P to C minus 1, so the next fetch lands on C

### JIA
> Name: Jump if A  
> Opcode: `0xD1`  
> Cycles: 1

Jumps to the address in C if A is nonzero.

1. Jump to C if A is nonzero

### JIB
> Name: Jump if B  
> Opcode: `0xD2`  
> Cycles: 1

Jumps to the address in C if B is nonzero.

1. Jump to C if B is nonzero

### JIC
> Name: Jump if C  
> Opcode: `0xD3`  
> Cycles: 1

Jumps to the address in C if C is nonzero.

1. Jump to C if C is nonzero

### JIX
> Name: Jump if not A  
> Opcode: `0xD4`  
> Cycles: 1

Jumps to the address in C if A is zero.

1. Jump to C if A is zero

### JIY
> Name: Jump if not B  
> Opcode: `0xD5`  
> Cycles: 1

Jumps to the address in C if B is zero.

1. Jump to C if B is zero

### JIZ
> Name: Jump if not C  
> Opcode: `0xD6`  
> Cycles: 1

Jumps to the address in C if C is zero.

1. Jump to C if C is zero

### JSC
> Name: Jump if Carry  
> Opcode: `0xD7`  
> Cycles: 1

Jumps to the address in C if the carry status bit is set.

1. Jump to C if the carry flag is set

### JMI
> Name: Jump Immediate  
> Opcode: `0xD8`  
> Cycles: 3

Jumps to an immediate address. The address is staged in the internal scratch byte, not a general register, so it never disturbs A/B/C.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. Set P to the target address minus 1

### JAI
> Name: Jump Immediate if A  
> Opcode: `0xD9`  
> Cycles: 3

Jumps to an immediate address if A is nonzero.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. If A is nonzero, set P to the target address minus 1

### JBI
> Name: Jump Immediate if B  
> Opcode: `0xDA`  
> Cycles: 3

Jumps to an immediate address if B is nonzero.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. If B is nonzero, set P to the target address minus 1

### JCI
> Name: Jump Immediate if C  
> Opcode: `0xDB`  
> Cycles: 3

Jumps to an immediate address if C is nonzero.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. If C is nonzero, set P to the target address minus 1

### JXI
> Name: Jump Immediate if not A  
> Opcode: `0xDC`  
> Cycles: 3

Jumps to an immediate address if A is zero.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. If A is zero, set P to the target address minus 1

### JYI
> Name: Jump Immediate if not B  
> Opcode: `0xDD`  
> Cycles: 3

Jumps to an immediate address if B is zero.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. If B is zero, set P to the target address minus 1

### JZI
> Name: Jump Immediate if not C  
> Opcode: `0xDE`  
> Cycles: 3

Jumps to an immediate address if C is zero.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. If C is zero, set P to the target address minus 1

## Stack and Subroutines

### SRT
> Name: Jump to Subroutine  
> Opcode: `0xE2`  
> Cycles: 3

Pushes the return address and jumps to the address in C.

1. Push the low byte of the return address P onto the stack, checking for overflow
2. Push the high byte of the return address, checking for overflow
3. Jump to C

### SIA
> Name: Jump to Subroutine if A  
> Opcode: `0xE3`  
> Cycles: 3

Pushes the return address and jumps to the address in C, only if A is nonzero.

1. If A is nonzero, push the low byte of the return address, checking for overflow
2. If A is nonzero, push the high byte of the return address, checking for overflow
3. If A is nonzero, jump to C

### SIB
> Name: Jump to Subroutine if B  
> Opcode: `0xE4`  
> Cycles: 3

Pushes the return address and jumps to the address in C, only if B is nonzero.

1. If B is nonzero, push the low byte of the return address, checking for overflow
2. If B is nonzero, push the high byte of the return address, checking for overflow
3. If B is nonzero, jump to C

### SIC
> Name: Jump to Subroutine if C  
> Opcode: `0xE5`  
> Cycles: 3

Pushes the return address and jumps to the address in C, only if C is nonzero.

1. If C is nonzero, push the low byte of the return address, checking for overflow
2. If C is nonzero, push the high byte of the return address, checking for overflow
3. If C is nonzero, jump to C

### SRI
> Name: Jump to Subroutine, Immediate  
> Opcode: `0xE6`  
> Cycles: 5

Pushes the return address and jumps to an immediate address.

1. Fetch the low byte of the target address
2. Fetch the high byte of the target address
3. Combine the address and push the low byte of the return address, checking for overflow
4. Push the high byte of the return address, checking for overflow
5. Jump to the target address

### RET
> Name: Return from Subroutine  
> Opcode: `0xE7`  
> Cycles: 3

Pops the return address pushed by a subroutine call and resumes there.

1. Check for underflow, pop the low byte of the return address
2. Check for underflow, pop the high byte of the return address
3. Combine both bytes and set P to the return address

### RTI
> Name: Return from Interrupt  
> Opcode: `0xE8`  
> Cycles: 1

Restores P, A, B, C, D, S, and T from the pending interrupt frame and resumes execution there. See SVI/LDI for how that frame can be swapped before this runs.

1. Restore the saved frame and resume execution

### PSHI
> Name: Push Immediate  
> Opcode: `0xE9`  
> Cycles: 5

Pushes a 2 byte immediate value directly onto the stack without touching any register. One cycle cheaper than the equivalent LIx <imm>; PSHx pair, since the second byte's fetch overlaps the first byte's stack write.

1. Fetch the low byte of the immediate value
2. Fetch the high byte of the immediate value
3. Push the low byte, checking for overflow, and stash the high byte
4. Push the high byte, checking for overflow
5. Delay one cycle so the write commits

### PSHI8
> Name: Push Immediate Byte  
> Opcode: `0xEA`  
> Cycles: 3

Pushes a 1 byte immediate value directly onto the stack. One byte in ROM, not two.

1. Fetch the immediate byte
2. Push the byte, checking for overflow
3. Delay one cycle so the write commits

### PSHN
> Name: Bulk Reserve  
> Opcode: `0xEE`  
> Cycles: 3

T += imm16, without touching memory. Bulk equivalent of imm16/2 PSHes.

1. Fetch the low byte of the count
2. Fetch the high byte of the count
3. Check for overflow and add the count to T

### PULN
> Name: Bulk Release  
> Opcode: `0xEF`  
> Cycles: 3

T -= imm16, without touching memory. Bulk equivalent of imm16/2 PULs.

1. Fetch the low byte of the count
2. Fetch the high byte of the count
3. Check for underflow and subtract the count from T

### PSHA
> Name: Push A  
> Opcode: `0xF0`  
> Cycles: 3

Pushes A onto the stack.

1. Push the low byte of A, checking for overflow
2. Push the high byte of A, checking for overflow
3. Delay one cycle so the write commits

### PSHB
> Name: Push B  
> Opcode: `0xF1`  
> Cycles: 3

Pushes B onto the stack.

1. Push the low byte of B, checking for overflow
2. Push the high byte of B, checking for overflow
3. Delay one cycle so the write commits

### PSHC
> Name: Push C  
> Opcode: `0xF2`  
> Cycles: 3

Pushes C onto the stack.

1. Push the low byte of C, checking for overflow
2. Push the high byte of C, checking for overflow
3. Delay one cycle so the write commits

### PSHD
> Name: Push D  
> Opcode: `0xF3`  
> Cycles: 3

Pushes D onto the stack.

1. Push the low byte of D, checking for overflow
2. Push the high byte of D, checking for overflow
3. Delay one cycle so the write commits

### PULA
> Name: Pull into A  
> Opcode: `0xF4`  
> Cycles: 3

Pops the top of the stack (2 bytes) into A.

1. Check for underflow, pop the low byte
2. Check for underflow, pop the high byte
3. Combine both bytes and store the result in A

### PULB
> Name: Pull into B  
> Opcode: `0xF5`  
> Cycles: 3

Pops the top of the stack (2 bytes) into B.

1. Check for underflow, pop the low byte
2. Check for underflow, pop the high byte
3. Combine both bytes and store the result in B

### PULC
> Name: Pull into C  
> Opcode: `0xF6`  
> Cycles: 3

Pops the top of the stack (2 bytes) into C.

1. Check for underflow, pop the low byte
2. Check for underflow, pop the high byte
3. Combine both bytes and store the result in C

### PULD
> Name: Pull into D  
> Opcode: `0xF7`  
> Cycles: 3

Pops the top of the stack (2 bytes) into D.

1. Check for underflow, pop the low byte
2. Check for underflow, pop the high byte
3. Combine both bytes and store the result in D

### PSHA8
> Name: Push Byte of A  
> Opcode: `0xF8`  
> Cycles: 2

Pushes the low byte of A onto the stack.

1. Push the low byte of A, checking for overflow
2. Delay one cycle so the write commits

### PSHB8
> Name: Push Byte of B  
> Opcode: `0xF9`  
> Cycles: 2

Pushes the low byte of B onto the stack.

1. Push the low byte of B, checking for overflow
2. Delay one cycle so the write commits

### PSHC8
> Name: Push Byte of C  
> Opcode: `0xFA`  
> Cycles: 2

Pushes the low byte of C onto the stack.

1. Push the low byte of C, checking for overflow
2. Delay one cycle so the write commits

### PSHD8
> Name: Push Byte of D  
> Opcode: `0xFB`  
> Cycles: 2

Pushes the low byte of D onto the stack.

1. Push the low byte of D, checking for overflow
2. Delay one cycle so the write commits

### PULA8
> Name: Pull Byte into A  
> Opcode: `0xFC`  
> Cycles: 2

Pops the top of the stack (1 byte) into A, zero extended.

1. Check for underflow, pop the byte
2. Zero-extend the byte and store the result in A

### PULB8
> Name: Pull Byte into B  
> Opcode: `0xFD`  
> Cycles: 2

Pops the top of the stack (1 byte) into B, zero extended.

1. Check for underflow, pop the byte
2. Zero-extend the byte and store the result in B

### PULC8
> Name: Pull Byte into C  
> Opcode: `0xFE`  
> Cycles: 2

Pops the top of the stack (1 byte) into C, zero extended.

1. Check for underflow, pop the byte
2. Zero-extend the byte and store the result in C

### PULD8
> Name: Pull Byte into D  
> Opcode: `0xFF`  
> Cycles: 2

Pops the top of the stack (1 byte) into D, zero extended.

1. Check for underflow, pop the byte
2. Zero-extend the byte and store the result in D

## Interrupts

### SVI
> Name: Save Interrupt Frame  
> Opcode: `0xE0`  
> Cycles: 14

Writes the pending interrupt-return frame (P, A, B, C, D, S, T - what a plain RTI would restore) to memory starting at the address in C, 1 byte per cycle. This is the primitive a preemptive scheduler needs: on interrupt entry A/B/C/D/T are already live with the interrupted process's values, so only P needs saving out of a register.

1. Write the low byte of P to [C+0]
2. Write the high byte of P to [C+1]
3. Write the low byte of A to [C+2]
4. Write the high byte of A to [C+3]
5. Write the low byte of B to [C+4]
6. Write the high byte of B to [C+5]
7. Write the low byte of C to [C+6]
8. Write the high byte of C to [C+7]
9. Write the low byte of D to [C+8]
10. Write the high byte of D to [C+9]
11. Write S to [C+10]
12. Write the low byte of T to [C+11]
13. Write the high byte of T to [C+12]
14. Delay one cycle so the last write commits

### LDI
> Name: Load Interrupt Frame  
> Opcode: `0xE1`  
> Cycles: 14

Reads a frame previously written by SVI back from memory at the address in C, replacing the pending interrupt frame, so the RTI that follows resumes into whatever was saved there instead of the process that was actually interrupted.

1. Reset the frame buffer and read the low byte of P from [C+0]
2. Store the low byte of P and read the high byte of P from [C+1]
3. Store the high byte of P and read the low byte of A from [C+2]
4. Store the low byte of A and read the high byte of A from [C+3]
5. Store the high byte of A and read the low byte of B from [C+4]
6. Store the low byte of B and read the high byte of B from [C+5]
7. Store the high byte of B and read the low byte of C from [C+6]
8. Store the low byte of C and read the high byte of C from [C+7]
9. Store the high byte of C and read the low byte of D from [C+8]
10. Store the low byte of D and read the high byte of D from [C+9]
11. Store the high byte of D and read S from [C+10]
12. Store S and read the low byte of T from [C+11]
13. Store the low byte of T and read the high byte of T from [C+12]
14. Store the high byte of T and replace the pending interrupt frame with the collected bytes

### INT
> Name: Software Interrupt  
> Opcode: `0xEB`  
> Cycles: 2

Raises IRQ <imm8> immediately, exactly as if a peripheral had called bus.irq() this cycle - same deferral rules apply (blocked by CLI, STATUS_IN_IRQ, or STATUS_IN_NMI). Lets software voluntarily trigger an IRQ handler instead of only reacting to real hardware timing.

1. Fetch the immediate IRQ id
2. Raise that IRQ

## System Control

### HLT
> Name: Halt  
> Opcode: `0x80`  
> Cycles: 1

Stops processing.

1. Set the halt status bit

### CLI
> Name: Disable Interrupts  
> Opcode: `0x81`  
> Cycles: 1

Sets the CLI status bit, blocking IRQs and NMIs.

1. Set the CLI status bit

### STI
> Name: Enable Interrupts  
> Opcode: `0x82`  
> Cycles: 1

Clears the CLI status bit, allowing IRQs and NMIs.

1. Clear the CLI status bit
