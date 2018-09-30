SELECT e.episode_name, e.season_num, e.episode_num, count(*) AS all, 
	count(*) FILTER (WHERE t.is_retweet IS FALSE) AS all_no_rt,
	count(*) FILTER (WHERE t.is_retweet IS FALSE AND t.favorites > 1) AS "all_no_rt_1+", 
	count(*) FILTER (WHERE t.is_retweet IS FALSE AND t.favorites > 2) AS "all_no_rt_2+"
FROM rewyndapp_tweet t
JOIN rewyndapp_episode e ON e.id = t.episode_id
GROUP BY 1,2,3
ORDER BY 2,3
