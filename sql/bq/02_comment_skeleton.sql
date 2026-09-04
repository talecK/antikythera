-- Full comment graph, no text. n_replies = direct child count (latest state).
CREATE OR REPLACE TABLE `YOUR_GCP_PROJECT.antikythera_hn.comment_skeleton` AS
WITH comments AS (
  SELECT id, parent, `by`, timestamp AS time
  FROM `bigquery-public-data.hacker_news.full`
  WHERE type = 'comment'
    AND NOT COALESCE(deleted, FALSE)
    AND NOT COALESCE(dead, FALSE)
)
SELECT c.id, c.parent, c.time, c.`by`, COALESCE(cc.n, 0) AS n_replies
FROM comments c
LEFT JOIN (SELECT parent, COUNT(*) AS n FROM comments GROUP BY parent) cc
  ON cc.parent = c.id;
