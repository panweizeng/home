<?php
require_once('TwitterOAuth.php');
require_once('config.php');

$to = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET);
if(file_exists($idLog)){
	$lastid = intval(file_get_contents($idLog));
	$params = array('count' => 5, 'since_id' => $lastid);
} else {
    touch($idLog);
	$params = array('count' => 1);
}

$ret = $to->OAuthRequest('https://twitter.com/statuses/user_timeline.json', $params, 'GET');
$tweets = json_decode($ret, true);
if(empty($tweets) || empty($tweets[0]['id'])) exit;
file_put_contents($idLog, $tweets[0]['id']);
while($t = array_pop($tweets)){
	$status = $t['text'];
    if(strpos($status,'@') !== 0){
		$ret = exec('curl -s -u '.$sinaAuth.' -d "source='.$source.'&status='.urlencode($status).'" http://api.t.sina.com.cn/statuses/update.json');
		file_put_contents($statusesLog, $status. "\n", FILE_APPEND);
    }
}

