-- CANONICAL filter spec (pre-registered). Source: bigquery-public-data.hacker_news.full
CREATE OR REPLACE TABLE `pricemole-g4a.antikythera_hn.stories_filtered` AS
SELECT id, timestamp AS time, `by`, title, url, text, score, descendants
FROM `bigquery-public-data.hacker_news.full`
WHERE type = 'story'
  AND NOT COALESCE(deleted, FALSE)
  AND NOT COALESCE(dead, FALSE)
  AND (score >= 5 OR descendants >= 3);
