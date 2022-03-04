```
assume that fields = (LEFT, WIDTH, RIGHT, X)

assume that MATCH is (True, False, False) or (LEFT, None, None)

FINAL_FRAME:
    x: -1000
    y: -1000
    w: -1000
    h: -1000
    
FINAL_FRAME.x = Layout.get_value(LEFT, CURRENT VIEW)

class Layout:
    
    def get_value(self, key: str, view: View) -> Number | Size | None:
        # Check if the 
```