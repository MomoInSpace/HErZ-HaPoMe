# UHH CL51 data repository

Data from the two Ceilometers (Vaisala CL51) of Universität Hamburg.

Two sets of test files contain sample data from Wettermast and Geomatikum for three days (29 Apr 2024 to 31 Apr 2024).

![sample plot](WMH_CL51_Plot.png)

To use the data, you have to load the DAT files. These files are generated from the Vaisala software "CL-View". See the CL51 manual for more information (p. 61, data message No. 2). The backscatter data are coded in hex numbers (5th line). Snippet of a read function:

HexLine := HexLine + StringOfChar('0',7700-Length(HexLine));  // add multiple '0' to get a length of 7700 chars
FOR j := 1 TO 1540 DO   // loop through 1540 height levels
  BEGIN
    h := Copy(HexLine,5*(j-1)+1,5);  // take 5 chars starting at pos 5*(j-1)+1 (first pos is 1)
    w := StrToUL(h);  // convert hex string h to unsigned long w
    // store w somewhere
  END;
