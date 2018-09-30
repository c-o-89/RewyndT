SELECT *
FROM rewyndapp_tweet t
WHERE t.episode_id = 1 AND t.is_retweet IS FALSE AND t.favorites > 3
ORDER BY 8 DESC, 7 DESC
