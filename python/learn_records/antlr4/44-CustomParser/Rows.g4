grammar Rows;

@parser::members {
    def set_col(self, col: int):
        self.col = col
}

file: (row NL)+;

row
	locals[i=0]: (
		STUFF {
            $i += 1
            if $i == self.col:
                print($STUFF.text)
        }
	)+;

TAB: '\t' -> skip; // match but don't pass to the parser
NL: '\r'? '\n'; // match and pass to the parser
STUFF: ~[\t\r\n]+; // match any chars except tab, newline