Downloaded supplmentar tables from here https://www.nature.com/articles/nature08514#Sec11, which had peaks in the tables. Did some wrangling in `41586_2009_BFnature08514_MOESM11_ESM.xls` and moved peaks manually to BED file. 

Moved to hg38 for each with the command
`liftOver OCT4.raw.bed ../GSE36570/hg18ToHg38.over.chain OCT4.hg38.bed unmapped.OCT4`
