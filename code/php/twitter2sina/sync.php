<?php
# 用户名:密码
$twitterAuth = 'test:123456';
$sinaAuth = 'test@sina.com:123456';
$source = 'your app key';

$url = 'http://'.$twitterAuth.'@twitter.com/statuses/user_timeline.json?';
$idLog = 'id.log';
$statusesLog = 'statuses.log';

if(file_exists($idLog)){
	$lastid = file_get_contents($idLog);
	$url .= 'count=100&since_id='.intval($lastid);
} else {
    touch($idLog);
	$url .= 'count=1';
}
 
$tweets = json_decode(file_get_contents($url), true);
if(empty($tweets) || empty($tweets[0]['id'])) exit;
file_put_contents($idLog, $tweets[0]['id']);
while($t = array_pop($tweets)){
	$status = $t['text'];
    if(strpos($status,'@') !== 0){
		$ret = exec('curl -s -u '.$sinaAuth.' -d "source='.$source.'&status='.urlencode($status).'" http://api.t.sina.com.cn/statuses/update.json');
		file_put_contents($statusesLog, $status. "\n", FILE_APPEND);
    }
}

