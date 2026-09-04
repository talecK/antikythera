-- Top ~20 comments per filtered story (CANONICAL doc spec).
-- Ranking (pre-registered): TOP-LEVEL comments (parent = story id) by direct
-- child count desc, then time asc; take 20. No comment scores exist in any
-- HN dump; reply count is the engagement proxy.
-- Window (pre-registered): comment.time <= story.time + 90 days, per story
-- (cleaner than the playground mirror's year+90d window; mirrors may differ
-- marginally at the window edge).
CREATE OR REPLACE TABLE `YOUR_GCP_PROJECT.antikythera_hn.comments_top20` AS
WITH stories AS (
  SELECT id, timestamp AS s_time
  FROM `bigquery-public-data.hacker_news.full`
  WHERE type = 'story'
    AND NOT COALESCE(deleted, FALSE)
    AND NOT COALESCE(dead, FALSE)
    AND (score >= 5 OR descendants >= 3)
),
comments AS (
  SELECT id, parent, `by`, timestamp AS time, text
  FROM `bigquery-public-data.hacker_news.full`
  WHERE type = 'comment'
    AND NOT COALESCE(deleted, FALSE)
    AND NOT COALESCE(dead, FALSE)
),
ranked AS (
  SELECT
    c.parent AS story_id, c.id, c.time, c.`by`, c.text,
    COALESCE(cc.n, 0) AS n_replies,
    ROW_NUMBER() OVER (
      PARTITION BY c.parent
      ORDER BY COALESCE(cc.n, 0) DESC, c.time ASC
    ) AS rn
  FROM comments c
  JOIN stories s
    ON c.parent = s.id
   AND c.time <= TIMESTAMP_ADD(s.s_time, INTERVAL 90 DAY)
  LEFT JOIN (SELECT parent, COUNT(*) AS n FROM comments GROUP BY parent) cc
    ON cc.parent = c.id
)
SELECT story_id, id, time, `by`, text, n_replies
FROM ranked
WHERE rn <= 20;
