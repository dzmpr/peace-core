# Python to GPSS source-to-source translator

## How to use? Syntax.
Source code not indentation dependent. Each line should contain one statement. Peace not cheching validity of GPSS code i.e. program from Peace can be translated to GPSS without SIMULATE and END blocks if *main* statement isn't used. Peace checking validity of used names for device blocks, operators and expressions (now across whole code, in future - scope dependent).
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

* Expression block
  ```
  exprname {...}
  ```
  Used **outside main** block. This block declares expression which be translated to inner representation which can be used across programm inside *main* or another *expression* block. Expression name should be unique across file, but can be the same with name of device or queue. Allowed to use inside expression block special characters which will be replaced with arguments passed to this expression in call place (*not implemented yet*).
  
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
  compare("params")
  TEST params
  ```
* TRANSFER
  ```
  goto("params")
  TRANSFER params
  ```

### Labels
Labels can be added with such syntax:
```
labelname:
```
They can be at the same line with next statement or lines before.

### Comments
Comments specifying with **#** symbol. Comment lasts to the end of line. They has no affect to the output code and just will be ignored by translator.
```
# Comment example
```

## Goals
- [x] Make a tree-based intermediate representation
- [ ] Make scope dependent naming
- [x] Implement expressions
- [ ] Implement expressions with substitutions
- [ ] Limit naming according GPSS rules
