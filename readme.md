# Python to GPSS source-to-source translator
Peace source code not indentation dependent. Each line should contain one statement. Peace not checking validity of GPSS code. Peace checking validity of used names for device blocks, operators and expressions (now across whole code, in future - scope dependent).

## How to use?
**Minimum python version - 3.8.**
```bash
python main.py <path to .pce>
```
Interpreter will generate output .gpss file in the same folder with .pce.
### Blocks
* Main block
  ```
  main {...}
  ```
  Is used to declare body of the GPSS program: SIMULATE and END.
  
* Device block
  ```
  devicename {...}
  ```
  Used **inside main** block. Will be translated to SEIZE and RELEASE operators.

  Inside expression it's allowed to add "@" after device name. This syntax add expression occurrence number after each device name.

* Expression block
  ```
  exprname {...}
  ```
  Used **outside main** block. This block declares expression which be translated to inner representation which can be used across programm inside *main* or another *expression* block. Expression name should be unique across file, but can be the same with name of device or queue. 
  
  Allowed to use inside expression block special characters which will be replaced with arguments passed to this expression in call place. "@" parameter refers to number of certain expression was called. Positional arguments can be inserted by "@" sign with followed number of argument (f.e. @1, @10). Positional parameter get such type, in what place it first used.
  
### Operators
* ADVANCE
  ```
  delay(number[, number])
  ADVANCE number[, number]
  ```
* GENERATE
  ```
  gen("params")
  GENERATE params
  ```
* QUEUE
  ```
  q(word)
  QUEUE word
  ```
* DEPART
  ```
  dq(word)
  DEPART word
  ```
* SAVEVALUE
  ```
  changevar("params")
  SAVEVALUE params
  ```
* INITIAL
  ```
  var("params")
  INITIAL params
  ```
* TERMINATE
  ```
  destroy([number])
  TERMINATE [number]
  ```
* START
  ```
  init(number)
  START number
  ```
* TEST
  ```
  compare(word, "params")
  TEST word    params
  ```
* TRANSFER
  ```
  goto("params")
  TRANSFER params
  ```
* SPLIT
  ```
  copy("params")
  SPLIT params
  ```
* LINK
  ```
  link("params")
  LINK params
  ```
* UNLINK
  ```
  unlink("params")
  UNLINK params
  ```

### Labels
Labels can be added with such syntax:
```
labelname:
```
They can be at the same line with next statement or lines before.

Inside expression it's allowed to add "@" after label name. This syntax add expression occurrence number after each label. 

### Comments
Comments specifying with **#** symbol. Comment lasts to the end of line. They has no affect to the output code and just will be ignored by translator.
```
# Comment example
```

## Goals
- [x] Make a tree-based intermediate representation
- [x] Implement expressions
- [x] Implement expressions with substitutions
- [ ] Make scope dependent naming
- [ ] More familiar syntax with high-level languages
