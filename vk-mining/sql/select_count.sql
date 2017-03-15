SELECT Groups.gid, Groups.name, Groups.type, Groups.is_closed, Groups.description, Group_count.count, COUNT(Groups_members.user_id)
	FROM Groups
		JOIN Group_count ON Groups.gid = Group_count.group_id
		JOIN Groups_members ON Groups.gid = Groups_members.group_id
	WHERE Groups.gid <> 38532412
		GROUP BY Groups_members.group_id
		ORDER BY COUNT(Groups_members.user_id) DESC