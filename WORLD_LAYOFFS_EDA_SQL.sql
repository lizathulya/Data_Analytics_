use  world_layoffs;

select * from layoffs;
-- always make a copy of your table befor you start tp work with and work on the copy
create table layoffs_staging
like layoffs;

select * from layoffs_staging;

insert layoffs_staging
select * from layoffs;

select * from layoffs_staging;

-- removing duplicates
Select *,row_number()over(
partition by company, location,industry,total_laid_off,percentage_laid_off,"date",
stage,country,funds_raised_millions) 
 as row_num
 from layoffs_staging; 
 
 with duplicate_cte as
 (
 Select *,row_number()over(
partition by company, location,industry,total_laid_off,percentage_laid_off,"date",
stage,country,funds_raised_millions) 
 as row_num
 from layoffs_staging 
 )
Select * 
 from duplicate_cte
 where row_num >1;
 
 CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` INT)
  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
  
  select * from layoffs_staging2;
  insert into layoffs_staging2
  Select *,row_number()over(
partition by company, location,industry,total_laid_off,percentage_laid_off,"date",
stage,country,funds_raised_millions) 
 as row_num
 from layoffs_staging; 
 
select * from layoffs_staging2;
 
select * from layoffs_staging2 where row_num>1;
-- turn of the safe mode to run the delete statement
SET SQL_SAFE_UPDATES = 0;

DELETE FROM layoffs_staging2 WHERE row_num > 1;

select * from layoffs_staging2 where row_num>1;
-- turning on the safe mode after running the delete statement
SET SQL_SAFE_UPDATES = 1;

-- Standarzing the data

select distinct(company) from layoffs_staging2;
-- turn of the safe mode to run the updae statement
SET SQL_SAFE_UPDATES = 0;

update layoffs_staging2 set company=trim(company);
-- turning on the safe mode after running the update statement
SET SQL_SAFE_UPDATES = 1;
-- turn of the safe mode to run the updae statement
SET SQL_SAFE_UPDATES = 0;
update layoffs_staging2 set industry='crypto' where industry like 'crypto%';
-- turning on the safe mode after running the update statement
SET SQL_SAFE_UPDATES = 1;
select industry from layoffs_staging2 order by 1;
select distinct country from layoffs_staging2 order by 1;
-- removing the . from United states
select distinct country,trim(trailing '.' from country) from layoffs_staging2  order by 1;
SET SQL_SAFE_UPDATES = 0;
update layoffs_staging2 set country=trim(trailing '.' from country)
 where industry like "United States%";
 
 select distinct country from layoffs_staging2;
 SELECT `date`, STR_TO_DATE(`date`, '%m/%d/%y') AS formatted_date 
FROM layoffs_staging2;

UPDATE layoffs_staging2 
SET `date` = STR_TO_DATE(`date`, '%m/%d/%Y');

alter table layoffs_staging2  modify column `date` date;
select * from layoffs_staging2 where total_laid_off is null;

select *from layoffs_staging2 where industry is null or industry ='';

UPDATE layoffs_staging2
SET industry = NULL
WHERE TRIM(industry) = '';


select t1.industry,t2.industry 
from  layoffs_staging2 t1 
join layoffs_staging2 t2 
on t1.company=t2.company 
where (t1.industry is  null )
and t2.industry is not null;

update layoffs_staging2 t1 
join layoffs_staging2 t2 
on t1.company=t2.company 
set t1.industry=t2.industry
where (t1.industry is  null )
and t2.industry is not null;

select * from layoffs_staging2
where company='Airbnb';

select * from layoffs_staging2;

select * from layoffs_staging2 where total_laid_off is null 
and  percentage_laid_off is null;

delete from layoffs_staging2 where total_laid_off is null 
and  percentage_laid_off is null;

select * from layoffs_staging2;

-- done with data cleaning starting EDA

-- Exploratory Data Analysis


select * from layoffs_staging2;

select max(total_laid_off),min(total_laid_off)from layoffs_staging2;

select * from layoffs_staging2 where  percentage_laid_off =1
order by total_laid_off desc;

select * from layoffs_staging2 where  percentage_laid_off =1
order by total_laid_off desc;

select * from layoffs_staging2 where  percentage_laid_off =1
order by funds_raised_millions desc;

select company,sum(total_laid_off) from layoffs_staging2 group by company
order by 2 desc;

select industry,
sum(total_laid_off) from layoffs_staging2 group by industry
order by 2 desc;

select year(`date`) ,sum(total_laid_off) from layoffs_staging2 group by year(`date`)
order by 1 desc;

select company,
sum(percentage_laid_off) from layoffs_staging2 group by company
order by 2 desc;

select substring(`date`,6,2) as`month `,sum(total_laid_off)
from layoffs_staging2
group by `month `;

select substring(`date`,1,7) as`month `,sum(total_laid_off) FROM layoffs_staging2 
group by `month `
order by 1 asc;

WITH Rolling_total AS (
    SELECT 
        SUBSTRING(`date`, 1, 7) AS `month`, 
        SUM(total_laid_off) AS total_off
    FROM layoffs_staging2
    WHERE SUBSTRING(`date`, 1, 7) IS NOT NULL
    GROUP BY `month`
    ORDER BY 1 ASC
)
SELECT 
    `month`, 
    SUM(total_off) OVER (ORDER BY `month`) AS rolling_total
FROM Rolling_total;


select company,
sum(total_laid_off) from layoffs_staging2 group by company
order by 2 desc;

select company,year(`date`),
sum(total_laid_off) from layoffs_staging2 group by company,year(`date`)
order by 3 desc;

WITH Company_year (company, years, total_laid_off) AS (
    SELECT 
        company,
        YEAR(`date`) AS years,
        SUM(total_laid_off) AS total_laid_off
    FROM layoffs_staging2
    GROUP BY company, YEAR(`date`)
),Company_year_rank as 
(
SELECT *,
       DENSE_RANK() OVER (PARTITION BY years ORDER BY total_laid_off DESC) AS Ranking
FROM Company_year
WHERE years IS NOT NULL
)
select * from Company_year_rank;

WITH Company_year (company, years, total_laid_off) AS (
    SELECT 
        company,
        YEAR(`date`) AS years,
        SUM(total_laid_off) AS total_laid_off
    FROM layoffs_staging2
    GROUP BY company, YEAR(`date`)
),Company_year_rank as 
(
SELECT *,
       DENSE_RANK() OVER (PARTITION BY years ORDER BY total_laid_off DESC) AS Ranking
FROM Company_year
WHERE years IS NOT NULL
)
select * from Company_year_rank
where Ranking<=5;



