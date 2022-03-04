
```
if START
    COORD   on FRAME    is  (GETVAL(START on VIEW)**)
    SIZE    on FRAME    is  SIZE    on LAYOUT
    
if START and SIZE
    COORD   on FRAME    is  (GETVAL(START on VIEW)**)
    SIZE    on FRAME    is  (GETVAL(SIZE on VIEW)**)
    
if SIZE
    COORD   on FRAME    is  (1/2 SIZE on CONTAINER minus 1/2 SIZE on VIEW)
    SIZE    on FRAME    is  (GETVAL(SIZE on VIEW)**)
    
if SIZE and END
    COORD   on FRAME    is  ((SIZE on CONTAINER) minus (GETVAL(END on VIEW)** on LAYOUT) minus (SIZE on VIEW))
    SIZE    on FRAME    is  SIZE    on VIEW
    
if END
    COORD   on FRAME    is  ((SIZE on CONTAINER) minus (GETVAL(END on VIEW)** on LAYOUT))
    SIZE    on FRAME    is  SIZE    on LAYOUT
    
if START and END
    COORD   on FRAME    is  (GETVAL(START on VIEW)**)
    SIZE    on FRAME    is  ((SIZE on CONTAINER) minus (GETVAL(START on VIEW)**) minus (GETVAL(END on VIEW)**))
    
    
** GETVAL(key, view) -> GETTYPE(key)
    if TYPE is CONSTANT:
        RETURN key from LAYOUT
        
    elif TYPE is INTRINSIC:
        if key is WIDTH:
        elif key is HEIGHT:
            
    elif TYPE is FRAME:
        if key is LEFT:
        elif key is TOP:
        elif key is RIGHT:
        elif key is BOTTOM:
        elif key is WIDTH:
        elif key is HEIGHT:
        
    elif TYPE is FRACTION:
         if key is LEFT or WIDTH or RIGHT:
         elif key is TOP or HEIGHT or BOTTOM:
```
