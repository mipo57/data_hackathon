/*
DELETE FROM szkolyAdresy where RSPO = 122941 OR RSPO = 129025;
DELETE FROM [dbo].[OLE DB Destination] where [Nr RSPO] = 122941 OR [Nr RSPO] = 129025
*/



-------------------------------------------
-------------------------------------------
-------------------------------------------
WITH T1 AS (
SELECT CAST([Nr RSPO] AS int) 'RSPO' , [Nazwa szko³y, placówki] 'Nazwa', [Nazwa typu] 'Typ', [Patron],
CASE 
	WHEN CAST([Kateg# uczniów] AS int)=2 THEN 'Dzieci lub m³odzie¿'
	WHEN CAST([Kateg# uczniów] AS int)=1 THEN 'Doroœli'
	ELSE 'Bez kategorii'
END AS 'KatUczniow',
CASE 
	WHEN CAST([Spec# szko³y] AS int)=1 THEN 1
	ELSE 0
END AS 'CzySpecjalna',
CASE 
	WHEN [Publicznoœæ]='1' THEN 1
	ELSE 0
END AS 'CzyPubliczna',
CAST([Oddzia³y] AS int) 'LOddzialow',
CASE 
	WHEN [Uczniowie, wychow#, s³uchacze]<3000 THEN CAST([Uczniowie, wychow#, s³uchacze] AS int)
	ELSE 84
END AS 'LUczniow',
CAST([w tym dziewczêta] AS int) 'LDziewczat',
CAST([Nauczyciele pe³nozatrudnieni] AS int) 'LNauczPelenEtat',
CAST([Nauczyciele niepe³nozatrudnieni (stos#pracy)] AS int) 'LNauczNpelenEtat',
[Nauczyciele niepe³nozatrudnieni (w etatach)]+CAST([Nauczyciele pe³nozatrudnieni] AS int) 'LEtatatowNauczycieli'
FROM [dbo].[OLE DB Destination]
INNER JOIN szkolyAdresy --join, ¿eby by³o tyle rekordów ile w szkolyAdresy
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
