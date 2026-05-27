# CMSC 132 Final Project - ISA Simulator

This project is a Python-based Instruction Set Architecture (ISA) simulator for CMSC 132. It demonstrates how high-level assembly-like instructions can be converted into binary instruction codes, stored in simulated memory, and executed through a simplified computer architecture.

The system models the major stages of instruction processing:

1. Converting values to and from a custom half-precision binary format
2. Managing simulated memory, registers, and named variables
3. Resolving operands through different addressing modes
4. Compiling readable instructions into 32-bit instruction codes
5. Fetching, decoding, executing, and writing results during program execution

## Developers

- John Clyde Aparicio
- Kent Francis Genilo
- Christian Jave Hulleza

## Project Overview

The simulator is designed around a small custom ISA. Each instruction is represented as a 32-bit binary string containing an operation code, addressing mode bits, operand addresses, and extra bits used by selected addressing formats.

The program flow follows this structure:

```text
Source Instructions
        |
        v
Compiler
        |
        v
32-bit Instruction Codes
        |
        v
Memory and Registers
        |
        v
Program Runner
        |
        v
Executed Results
```

## Core Components

### `bin_convert.py`

This file contains the binary conversion utilities used throughout the simulator.

Main classes:

- `Length` - stores fixed bit lengths and helper methods for padding and rounding values
- `BinaryFraction` - converts decimal fractions to binary fractions and binary fractions back to decimal
- `HalfPrecision` - converts decimal numbers to the project's custom half-precision binary format and back

Important functionality:

- Converts decimal values into 16-bit half-precision binary strings
- Converts half-precision binary strings back into decimal values
- Pads binary strings with leading or trailing zeroes
- Rounds decimal results to the configured number of decimal places

### `storage.py`

This file defines the simulated storage system of the ISA.

Main class:

- `Storage` - manages address-value pairs using a dictionary-based storage structure

Created storage objects:

- `memory` - simulates main memory with 128 slots
- `register` - simulates register storage with 32 slots
- `variable` - maps readable names such as `PC`, `IR`, `BR`, `R1`, `A`, and `B1` to their corresponding storage addresses

Memory layout:

```text
0       Special storage
1-8     Variables A-H
9-56    Instructions
57-64   Main blocks B1-B8
65-68   Function blocks F1-F4
69-76   Function parameters P1-P8
77-100  Arrays
101-116 Indirect addresses
117-127 Extra memory storage
```

Register layout:

```text
0       Special register
1-8     General registers R1-R8
9       Base Register (BR)
10      Index Register (XR)
11      Accumulator (ACC)
12      Instruction Register (IR)
13      Program Counter (PC)
14      Jump Register (JR)
15      Call Register (CR)
21-31   Extra register storage
```

### `addressing.py`

This component handles operand access and addressing mode resolution aspects.

Classes Implemented:

- `Access` - provides helper functions for following storage access flow through `variable`, `memory`, and `register`, and also for writing to `register` or `memory` storage flows
- `AddressingMode` - implements the Instruction Set Architecture (ISA) addressing modes

Supported addressing modes:

- Immediate addressing
- Relative addressing
- Based addressing
- Indexed addressing
- Register addressing
- Register indirect addressing
- Direct addressing
- Indirect addressing
- Auto-increment addressing
- Auto-decrement addressing

This file is important because the main or runner file needs it to determine the actual value, effective address, and storage location of each operand.

`Other Files to be implemented yet.`

## Instruction Format

Each instruction uses a 32-bit format:

```text
Bits 0-4    Operation code
Bit 5       Immediate bit
Bits 6-8    Operand 1 addressing mode
Bits 9-15   Operand 1 address
Bit 16      Relative or based bit
Bits 17-19  Operand 2 addressing mode
Bits 20-26  Operand 2 address
Bits 27-31  Extra bits
```

## Supported Operations

The ISA supports arithmetic, data movement, comparison, branching, function, input/output, and program control operations.

Arithmetic operations:

- `ADD`
- `SUB`
- `MUL`
- `DIV`
- `MOD`

Data movement and comparison:

- `MOV`
- `CMP`
- `ADDPC`

Branching operations:

- `JMP`
- `JEQ`
- `JNE`
- `JLT`
- `JLE`
- `JGT`
- `JGE`

Block and function operations:

- `CB`
- `CF`
- `CALL`
- `RET`
- `FUNC`

Input/output and control:

- `SCAN`
- `PRNT`
- `EOP`

## Prerequisites

To work on this project, you should have:

- Python 3 installed
- Basic understanding of Python classes and static methods
- Basic knowledge of binary numbers
- Basic understanding of memory, registers, and instruction execution
- Familiarity with simple assembly-like instructions

No external Python packages are required for the core simulator.

## Setup

Clone or download the project, then open the project folder:

On Windows:
```powershell
cd "C:\Users\username\Downloads\CMSC132-Final-Project"
```
On Mac:
```powershell
cd "/Users/username/Downloads/CMSC132-Final-Project"
```
On Linux:
```powershell
cd "/home/username/Downloads/CMSC132-Final-Project"
```
Or (also for Mac):
```powershell
cd ~/Downloads/CMSC132-Final-Project
```

Check that Python is available:

```powershell
python --version
```

Test the provided conversion and storage files:

## Development Order

The recommended implementation order is:

1. Verify `bin_convert.py`
2. Verify `storage.py`
3. Some files to be implemented yet.

## Sample Test Program

A simple program may look like this:

```text
MOV R1 5
MOV R2 3
ADD R1 R2
EOP
```

This should move values into registers, add them, and stop the program.

## Notes

- The instruction PDF is used as the project specification and does not need to be committed if it is only a reference file.
- Python may automatically create a `__pycache__` folder when files are imported. This folder is safe to ignore in Git.
- The simulator should be tested in small parts before running larger instruction files.
