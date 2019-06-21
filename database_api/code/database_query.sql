/*
DELETE FROM szkolyAdresy where RSPO = 122941 OR RSPO = 129025;
DELETE FROM [dbo].[OLE DB Destination] where [Nr RSPO] = 122941 OR [Nr RSPO] = 129025
*/



-------------------------------------------
-------------------------------------------
-------------------------------------------
WITH T1 AS (
SELECT CAST([Nr RSPO] AS int) 'RSPO' , [Nazwa szko�y, plac�wki] 'Nazwa', [Nazwa typu] 'Typ', [Patron],
CASE 
	WHEN CAST([Kateg# uczni�w] AS int)=2 THEN 'Dzieci lub m�odzie�'
	WHEN CAST([Kateg# uczni�w] AS int)=1 THEN 'Doro�li'
	ELSE 'Bez kategorii'
END AS 'KatUczniow',
CASE 
	WHEN CAST([Spec# szko�y] AS int)=1 THEN 1
	ELSE 0
END AS 'CzySpecjalna',
CASE 
	WHEN [Publiczno��]='1' THEN 1
	ELSE 0
END AS 'CzyPubliczna',
CAST([Oddzia�y] AS int) 'LOddzialow',
CASE 
	WHEN [Uczniowie, wychow#, s�uchacze]<3000 THEN CAST([Uczniowie, wychow#, s�uchacze] AS int)
	ELSE 84
END AS 'LUczniow',
CAST([w tym dziewcz�ta] AS int) 'LDziewczat',
CAST([Nauczyciele pe�nozatrudnieni] AS int) 'LNauczPelenEtat',
CAST([Nauczyciele niepe�nozatrudnieni (stos#pracy)] AS int) 'LNauczNpelenEtat',
[Nauczyciele niepe�nozatrudnieni (w etatach)]+CAST([Nauczyciele pe�nozatrudnieni] AS int) 'LEtatatowNauczycieli'
FROM [dbo].[OLE DB Destination]
INNER JOIN szkolyAdresy --join, �eby by�o tyle rekord�w ile w szkolyAdresy
ON [dbo].[OLE DB Destination].[Nr RSPO] = szkolyAdresy.RSPO
)
SELECT * INTO szkolyPlacowki FROM T1;

ALTER TABLE [dbo].[szkolyPlacowki] ALTER COLUMN [RSPO] INTEGER NOT NULL;
ALTER TABLE [dbo].[szkolyPlacowki] ADD CONSTRAINT pk_szkpl PRIMARY KEY([RSPO]);

-------------------------------------------
-------------------------------------------
-------------------------------------------


SELECT COUNT(*) FROM [dbo].[szkolyAdresy];
SELECT COUNT(*) FROM [dbo].[szkolyPlacowki];
SELECT szkolyPlacowki.RSPO, KodPocztowy, Miejscowosc, Nazwa, Typ FROM szkolyAdresy
INNER JOIN szkolyPlacowki ON szkolyAdresy.RSPO = szkolyPlacowki.RSPO
