// FM25Q16A

{$readUID} // Read Unique ID
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  SPIWrite(0, 5, $4B, 0,0,0,0);
  SPIReadToEditor(1, 8);

  SPIExitProgMode();
end

{$eraseSS} // Erase Security Sector
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  SPIWrite(1, 1, $06); // Write Enable
  SPIWrite(0, 4, $44, 0,0,0);

  //Busy?
  sreg := 0;
  repeat
    SPIWrite(0, 1, $05);
    SPIRead(1, 1, sreg);
  until((sreg and 1) <> 1);

  SPIExitProgMode();
end

{$readSS} // Read Security Sector
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  PageSize := 256;
  SectorSize := 1024;
  ProgressBar(0, (SectorSize / PageSize)-1, 0);

  for i:=0 to (SectorSize / PageSize)-1 do
  begin
    SPIWrite(0, 5, $48, 0,0,i,0);
    SPIReadToEditor(1, PageSize);
    ProgressBar(1);
  end;

  ProgressBar(0, 0, 0);
  SPIExitProgMode();
end

{$writeSS} // Write Security Sector
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  PageSize := 256;
  SectorSize := 1024;
  ProgressBar(0, (SectorSize / PageSize)-1, 0);

  for i:=0 to (SectorSize / PageSize)-1 do
  begin
    SPIWrite(1, 1, $06); // Write Enable
    SPIWrite(0, 4, $42, 0,0,i);
    SPIWriteFromEditor(1, PageSize, i*PageSize); // Write Data

    //Busy?
    sreg := 0;
    repeat
      SPIWrite(0, 1, $05);
      SPIRead(1, 1, sreg);
    until((sreg and 1) <> 1);

    ProgressBar(1);
  end;

  ProgressBar(0, 0, 0);
  SPIExitProgMode();
end